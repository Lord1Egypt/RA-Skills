#!/usr/bin/env python3
"""
example_create_dataset.py — Template for the provenance script that ships
with each dataset. Copy this file into the dataset root as `create_dataset.py`
and adapt it to your dataset's actual data sources.

A good provenance script:
1. Reads raw inputs (URLs, files, generators) from publicly-available sources.
2. Applies all transforms and filters (with explicit random seeds for sampling).
3. Builds the parquet shards (matching the published files exactly).
4. Prints the same statistics that ended up in the YAML.

UltraFeedback Binarized and Argilla's DPO pairs both ship a script like this.
Reproducibility is what makes a dataset trustworthy.

This script is **self-contained**: it embeds the minimal parquet-writing and
stat-computing pipeline inline (no `import produce_dataset`), so it works
even when shipped alongside the dataset without the skill's scripts directory.

USAGE (once adapted)
--------------------
    python create_dataset.py

Reads from raw sources, writes to ./data/, prints stats. Re-runnable.
"""

import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# These are the only deps needed. They are listed in the dataset's
# `requirements.txt` (or the user installs with `pip install datasets pyarrow`).
from datasets import Dataset, Features, Value, Sequence, ClassLabel


# ─── Constants (EDIT THESE) ────────────────────────────────────────────────

DATASET_NAME = "my_dataset"            # change to your dataset's slug
RAW_SOURCES = [                          # list all upstream sources here
    # {"type": "url", "url": "https://...", "format": "jsonl"},
    # {"type": "file", "path": "raw/source1.jsonl"},
    # {"type": "generator", "name": "llm-generation", "model": "..."},
    # {"type": "huggingface", "repo_id": "tatsu-lab/alpaca"},
]
SEED = 42                                # global random seed for reproducibility
SPLITS = {"train": 0.9, "test": 0.1}     # split fractions (must sum to 1.0)
SHARD_SIZE_BYTES = 500 * 1024 * 1024    # 500 MB target shard size
LICENSE = "cc-by-4.0"
LANGUAGES = ["en"]
TASK_CATEGORIES = ["text-generation"]


# ─── Feature schema (EDIT THIS) ─────────────────────────────────────────────
#
# Define your feature schema here. See the skill's references/schemas.md for
# canonical schemas for instruction-tuning, chat, preference/DPO, pretraining,
# benchmark MCQ, and benchmark QA. The schema below is the Alpaca-style
# instruction-tuning schema.

FEATURES = Features({
    "instruction": Value("string"),
    "input":       Value("string"),
    "output":      Value("string"),
})

# Feature keys, computed once at module level BEFORE any function that uses
# them (previously this was defined after collect_rows, which worked only
# because collect_rows ran at main() time — fragile if imported as a library).
FEATURE_KEYS = list(FEATURES.keys())

# String fields that quality filters should inspect (all Value("string") fields).
STRING_FIELDS = [k for k, f in FEATURES.items()
                 if isinstance(f, Value) and f.dtype == "string"]


# ─── Minimal self-contained pipeline (do NOT edit unless you know why) ────
#
# These functions are a stripped-down copy of produce_dataset.py's pipeline.
# Keeping them inline means this script works as a standalone artifact in the
# dataset repo, without requiring the skill's scripts/ directory.

def _split_rows(rows: List[Dict[str, Any]], splits: Dict[str, float],
                seed: int = 42) -> Dict[str, List[Dict[str, Any]]]:
    """Shuffle rows with a fixed seed, then partition by fractions."""
    rng = random.Random(seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    result: Dict[str, List[Dict[str, Any]]] = {}
    start = 0
    names = list(splits.keys())
    for i, (name, frac) in enumerate(splits.items()):
        if i == len(names) - 1:
            result[name] = shuffled[start:]
        else:
            count = int(round(n * frac))
            result[name] = shuffled[start:start + count]
            start += count
    return result


def _shard_rows(rows: List[Dict[str, Any]], shard_size_bytes: int) -> List[List[Dict[str, Any]]]:
    """Greedy sharding: pack rows into shards until each is ~shard_size_bytes.

    Uses a bytes-safe size estimator so Image/Audio features (raw `bytes`)
    don't crash the json.dumps call.
    """
    if not rows:
        return [[]]
    def _default(o):
        if isinstance(o, (bytes, bytearray, memoryview)):
            return f"<{len(o)} bytes>"
        return repr(o)
    sample = rows[:100]
    sample_bytes = sum(len(json.dumps(r, ensure_ascii=False, default=_default).encode("utf-8")) for r in sample)
    avg_row_bytes = max(1, sample_bytes // max(1, len(sample)))
    rows_per_shard = max(1, shard_size_bytes // avg_row_bytes)
    n_shards = max(1, math.ceil(len(rows) / rows_per_shard))
    rows_per_shard = math.ceil(len(rows) / n_shards)
    return [rows[i:i + rows_per_shard] for i in range(0, len(rows), rows_per_shard)]


def _rows_to_dataset(rows: List[Dict[str, Any]], features: Features) -> Dataset:
    """Build a Dataset from rows using the explicit Features schema."""
    columnar: Dict[str, List[Any]] = {name: [] for name in features}
    for row in rows:
        for name, feat in features.items():
            val = row.get(name)
            if isinstance(feat, ClassLabel) and isinstance(val, str):
                try:
                    val = feat.str2int(val)
                except Exception:
                    pass
            columnar[name].append(val)
    return Dataset.from_dict(columnar, features=features)


def _write_shards(rows: List[Dict[str, Any]], features: Features,
                  split_name: str, out_dir: Path,
                  shard_size_bytes: int) -> Tuple[List[Path], int]:
    """Write rows as sharded parquet. Returns (file paths, total arrow bytes)."""
    shards = _shard_rows(rows, shard_size_bytes)
    n_shards = len(shards)
    paths: List[Path] = []
    total_nbytes = 0
    for i, shard_rows_list in enumerate(shards):
        ds = _rows_to_dataset(shard_rows_list, features)
        fname = f"{split_name}-{i:05d}-of-{n_shards:05d}.parquet"
        fpath = out_dir / fname
        ds.to_parquet(str(fpath))
        try:
            arrow_nbytes = ds.data.table.nbytes
        except Exception:
            try:
                import pyarrow.parquet as pq
                arrow_nbytes = pq.read_table(str(fpath)).nbytes
            except Exception:
                arrow_nbytes = fpath.stat().st_size
        total_nbytes += arrow_nbytes
        paths.append(fpath)
        print(f"  Wrote {fpath.name}  ({len(shard_rows_list)} rows, "
              f"{fpath.stat().st_size:,} bytes, {arrow_nbytes:,} arrow bytes)")
    return paths, total_nbytes


def _size_bucket(n: int) -> str:
    """Map a row count to a HF size_categories bucket."""
    if n < 1_000:         return "n<1K"
    if n < 10_000:        return "1K<n<10K"
    if n < 100_000:       return "10K<n<100K"
    if n < 1_000_000:     return "100K<n<1M"
    if n < 10_000_000:    return "1M<n<10M"
    if n < 100_000_000:   return "10M<n<100M"
    if n < 1_000_000_000: return "100M<n<1B"
    if n < 10_000_000_000: return "1B<n<10B"
    if n < 100_000_000_000: return "10B<n<100B"
    if n < 1_000_000_000_000: return "100B<n<1T"
    return "n>1T"


def build_dataset(rows: List[Dict[str, Any]], features: Features,
                  splits: Dict[str, float], out_dir: Path,
                  shard_size_bytes: int, seed: int = 42) -> Dict[str, Any]:
    """End-to-end: split rows, shard, write parquet, compute stats, save stats.json."""
    out_dir.mkdir(parents=True, exist_ok=True)
    split_rows_map = _split_rows(rows, splits, seed=seed)
    print(f"Split {len(rows)} rows into: "
          + ", ".join(f"{k}={len(v)}" for k, v in split_rows_map.items()))

    split_stats: Dict[str, Any] = {}
    for split_name, split_rows_list in split_rows_map.items():
        print(f"\nWriting split '{split_name}' ({len(split_rows_list)} rows)...")
        shard_paths, arrow_nbytes = _write_shards(
            split_rows_list, features, split_name, out_dir, shard_size_bytes
        )
        split_stats[split_name] = {
            "num_examples": len(split_rows_list),
            "num_bytes": arrow_nbytes if arrow_nbytes > 0 else sum(p.stat().st_size for p in shard_paths),
            "download_size": sum(p.stat().st_size for p in shard_paths),
            "shards": [str(p.name) for p in shard_paths],
        }

    total_examples = sum(s["num_examples"] for s in split_stats.values())
    total_download = sum(s["download_size"] for s in split_stats.values())
    total_bytes = sum(s["num_bytes"] for s in split_stats.values())

    stats = {
        "splits": split_stats,
        "total_examples": total_examples,
        "total_download_size": total_download,
        "total_dataset_size": total_bytes,
        "size_categories": _size_bucket(total_examples),
        "shard_size": f"{shard_size_bytes}",
        "features": features.to_dict(),
    }

    # Save stats.json next to the parquet files (in the dataset root, not data/)
    stats_path = out_dir.parent / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nStats written to: {stats_path}")
    return stats


# ─── Data collection (EDIT THIS) ───────────────────────────────────────────

def collect_rows() -> list:
    """Read raw sources, build a list of row dicts matching FEATURES.

    Replace the placeholder logic below with your actual collection code.
    Each row must have keys matching FEATURES (missing fields will be set to None).

    Common patterns:
      - From local JSONL: read file line by line, parse each line as JSON
      - From URLs: use the web-reader skill (z-ai function -n page_reader)
      - From another HF dataset: from datasets import load_dataset
      - From LLM generation: use the LLM skill
    """
    random.seed(SEED)
    rows = []

    # === REPLACE THIS BLOCK WITH YOUR ACTUAL COLLECTION LOGIC ===
    # Example: hand-curated placeholder rows
    sample_rows = [
        {"instruction": "What is 2 + 2?", "input": "", "output": "4"},
        {"instruction": "Translate 'hello' to French.", "input": "", "output": "Bonjour"},
        {"instruction": "Summarize the following text.", "input": "Lorem ipsum...", "output": "Lorem ipsum summarized."},
    ]
    rows.extend(sample_rows)
    # === END REPLACE BLOCK ===

    # Add stable IDs if your schema has one
    for i, row in enumerate(rows):
        if "id" in FEATURE_KEYS and "id" not in row:
            row["id"] = f"{DATASET_NAME}_{i:06d}"

    return rows


# ─── Filters (EDIT THIS) ────────────────────────────────────────────────────

def apply_filters(rows: list) -> tuple:
    """Apply quality filters. Returns (kept_rows, dropped_count).

    Document each filter's drop count below — FineWeb and Dolma publish these
    in their READMEs as 'Summary Statistics' tables.

    The filters below are schema-aware: they iterate the schema's string
    fields (STRING_FIELDS) instead of hard-coding field names, so they keep
    working when you swap in the chat/DPO/pretraining schema.
    """
    n_in = len(rows)
    print(f"Filter input: {n_in} rows")

    # Filter 1: drop rows where any required string field is empty/missing.
    # (Fields that are legitimately optional — e.g. instruction-tuning's
    # `input` — should be removed from this check.)
    required = [f for f in STRING_FIELDS if f in ("instruction", "output", "text",
                                                  "question", "prompt", "context")]
    rows = [r for r in rows if all(r.get(f) for f in required)]
    n_after_1 = len(rows)
    print(f"  After 'drop empty required fields': {n_after_1} (dropped {n_in - n_after_1})")

    # Filter 2: drop extreme lengths (>100k chars in any string field)
    rows = [r for r in rows if all(
        len(str(r.get(f, ""))) < 100_000 for f in STRING_FIELDS
    )]
    n_after_2 = len(rows)
    print(f"  After 'drop extreme lengths': {n_after_2} (dropped {n_after_1 - n_after_2})")

    # Add more filters here (PII, dedup, language ID, etc.) as needed.
    # For PII/dedup/contamination, run the skill's `validate.py` first;
    # for exact dedup at build time, see produce_dataset.py --drop-duplicates.

    return rows, n_in - len(rows)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    print(f"=== Building dataset: {DATASET_NAME} ===\n")

    # 1. Collect rows
    print("Step 1: Collecting raw rows...")
    rows = collect_rows()
    print(f"  Collected {len(rows)} rows\n")

    # 2. Apply filters
    print("Step 2: Applying quality filters...")
    rows, dropped = apply_filters(rows)
    print(f"  Kept {len(rows)} rows (dropped {dropped})\n")

    # 3. Set up output directory (data/ subdir of the script's location)
    out_dir = Path(__file__).parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 4. Build parquet shards + compute stats
    print("Step 3: Building parquet shards and computing stats...")
    stats = build_dataset(
        rows=rows,
        features=FEATURES,
        splits=SPLITS,
        out_dir=out_dir,
        shard_size_bytes=SHARD_SIZE_BYTES,
        seed=SEED,
    )

    # 5. Print final stats
    print("\n=== Production complete ===")
    print(f"Total examples:  {stats['total_examples']:,}")
    print(f"Download size:   {stats['total_download_size']:,} bytes")
    print(f"Dataset size:    {stats['total_dataset_size']:,} bytes")
    print(f"Size bucket:     {stats['size_categories']}")
    print(f"\nSplits:")
    for name, s in stats["splits"].items():
        print(f"  {name}: {s['num_examples']:,} rows, {len(s['shards'])} shard(s)")

    print(f"\nNext steps:")
    print(f"  1. Run make_card.py to generate README.md from stats.json + features.json")
    print(f"  2. Copy a LICENSE file matching '{LICENSE}' into the dataset root")
    print(f"  3. Verify with: python -c \"from datasets import load_dataset; print(load_dataset('{out_dir.parent}'))\"")


if __name__ == "__main__":
    main()

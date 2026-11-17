#!/usr/bin/env python3
"""
produce_dataset.py — End-to-end dataset production pipeline.

Reads raw data (JSONL / JSON / CSV / TSV / Python list), validates against a
Features spec, builds sharded parquet files using the canonical HF naming
convention, and writes a stats.json with split sizes for use by make_card.py.

USAGE
-----
As a CLI:

    python produce_dataset.py \
        --input raw.jsonl \
        --features features.json \
        --splits train:0.9,test:0.1 \
        --out /home/z/my-project/download/my_dataset/data/ \
        --shard-size 500MB

As a library:

    from produce_dataset import produce_dataset
    produce_dataset(
        rows=[{"instruction": "...", "output": "..."}, ...],
        features_json="features.json",
        splits={"train": 0.9, "test": 0.1},
        out_dir="data/",
        shard_size="500MB",
    )

FEATURES SPEC
-------------
The --features file is JSON with this shape (mirrors HF Features):

    {
      "instruction": {"_type": "Value", "dtype": "string"},
      "input":       {"_type": "Value", "dtype": "string"},
      "output":      {"_type": "Value", "dtype": "string"},
      "messages":    {"_type": "Sequence", "feature": {
                        "_type": "struct",
                        "fields": {
                          "role":    {"_type": "Value", "dtype": "string"},
                          "content": {"_type": "Value", "dtype": "string"}
                        }
                      }}
    }

For convenience, you can also pass a YAML-style dict via Python directly when
using as a library. `Features.to_dict()` output is also accepted — both
`_type: "Sequence"` and `_type: "List"` are recognized (HF rewrites Sequence
to List in some code paths).

SPLITS
------
--splits accepts a comma-separated list of name:fraction pairs (fractions must
sum to 1.0). Examples:
  --splits train:0.9,test:0.1
  --splits train:0.8,validation:0.1,test:0.1
  --splits train:1.0                     (single split)

Split modes (--split-mode):
  random     — random shuffle, then partition (default; uses --seed)
  temporal   — assume rows are in chronological order; first N% → first split
               (no shuffle; preserves order)
  stratified — for ClassLabel-bearing schemas, balance each class across splits
               (requires a ClassLabel field; uses --stratify-field)

SHARD NAMING
------------
Output files follow the canonical HF pattern:
  <split>-<NNNNN>-of-<NNNNN>.parquet

This is what the HF loader recognizes for auto-inference of splits. Empty
splits still produce a single empty shard so the README's `data_files` glob
always matches a file.
"""

import argparse
import hashlib
import json
import os
import sys
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    from datasets import Dataset, Features, Value, Sequence, ClassLabel
except ImportError as e:
    print(f"ERROR: missing dependency: {e}", file=sys.stderr)
    print("Install with:  pip install datasets pyarrow pyyaml", file=sys.stderr)
    sys.exit(1)


# ─── Feature spec parsing ───────────────────────────────────────────────────

def _parse_feature_spec(spec: Dict[str, Any]):
    """Convert a JSON/dict feature spec into a datasets.Features-compatible object.

    Accepts the dict form produced by Features.to_dict(). Both `_type: "Sequence"`
    and `_type: "List"` are handled (HF rewrites Sequence→List in some code paths).
    Media features (`Image`, `Audio`, `Video`) are accepted in either the long
    form (`{"_type": "Image"}`) or the short form (`"Image"`) that older
    Features.to_dict() versions emit.

    Examples:
      {"_type": "Value", "dtype": "string"}                      -> Value("string")
      {"_type": "Sequence", "feature": <scalar spec>}            -> Sequence(<scalar>)
      {"_type": "List", "feature": <scalar spec>}                 -> Sequence(<scalar>)
      {"_type": "List", "feature": <struct spec>}                 -> [struct_dict]
      {"_type": "ClassLabel", "names": ["A","B","C"]}             -> ClassLabel(names=[...])
      {"_type": "struct", "fields": {name: spec, ...}}           -> {name: spec, ...}
      {"_type": "Image"} or "Image"                                -> Image()
      {"_type": "Audio", "sampling_rate": 16000}                  -> Audio(sampling_rate=16000)
    """
    # Short-form media types (a bare string like "Image")
    if isinstance(spec, str):
        if spec == "Image":
            from datasets import Image
            return Image()
        if spec == "Audio":
            from datasets import Audio
            return Audio()
        if spec == "Video":
            from datasets import Video
            return Video()
        raise ValueError(f"Unknown feature spec: {spec!r}")

    if not isinstance(spec, dict):
        raise ValueError(f"Feature spec must be a dict, got {type(spec).__name__}: {spec!r}")

    t = spec.get("_type")
    if t == "Value":
        return Value(spec["dtype"])
    if t == "ClassLabel":
        return ClassLabel(names=spec.get("names", []))
    if t == "Image":
        from datasets import Image
        return Image()
    if t == "Audio":
        from datasets import Audio
        return Audio(sampling_rate=spec.get("sampling_rate")) if spec.get("sampling_rate") else Audio()
    if t == "Video":
        from datasets import Video
        return Video()
    if t in ("Sequence", "List"):
        inner = spec.get("feature", {})
        # Inner could be a scalar Value, a struct (with _type="struct"), or a
        # bare dict of fields (HF's `Features.to_dict()` drops the `_type: "struct"`
        # wrapper in some versions).
        if isinstance(inner, dict) and inner.get("_type") == "Value":
            return Sequence(_parse_feature_spec(inner))
        if isinstance(inner, dict) and inner.get("_type") in ("struct", "dict"):
            fields = inner.get("fields", inner)
            return [{name: _parse_feature_spec(s) for name, s in fields.items()}]
        if isinstance(inner, dict) and "_type" not in inner:
            # Bare dict of fields (Features.to_dict() output for Sequence of struct)
            return [{name: _parse_feature_spec(s) for name, s in inner.items()}]
        # Fallback: treat as scalar sequence
        return Sequence(_parse_feature_spec(inner))
    if t in ("struct", "dict"):
        return {name: _parse_feature_spec(s) for name, s in spec.get("fields", spec).items()}
    # Fallback: assume it's a nested dict of features (e.g. the top-level
    # features.json or a struct-flattened field from Features.to_dict()).
    if "dtype" not in spec and "feature" not in spec and "names" not in spec:
        return {name: _parse_feature_spec(s) for name, s in spec.items()}
    raise ValueError(f"Unknown feature spec: {spec!r}")


def load_features(path_or_dict: Union[str, Dict]) -> Features:
    """Load a Features object from a JSON file path or a dict."""
    if isinstance(path_or_dict, dict):
        spec = path_or_dict
    else:
        with open(path_or_dict) as f:
            spec = json.load(f)
    parsed = {name: _parse_feature_spec(s) for name, s in spec.items()}
    return Features(parsed)


# ─── Input loading ──────────────────────────────────────────────────────────

def _coerce_csv_value(val: str, dtype: Optional[str]):
    """Coerce a CSV/TSV string cell to the declared dtype. Returns None for empty cells.

    CSV readers return every cell as a string, so a `token_count` column arrives
    as "42". Without coercion, validate.py flags every numeric CSV field as a
    schema violation and Arrow may reject the column. Coercion only applies to
    CSV/TSV sources — JSON/JSONL values are used as-is so real type errors in
    structured data still surface.
    """
    if val is None:
        return None
    if not isinstance(val, str):
        return val
    if val == "":
        # Empty cell = missing value for non-string types; keep "" for strings
        return None if (dtype and dtype not in ("string", "binary")) else val
    if dtype in ("int32", "int64", "uint32", "uint64"):
        try:
            return int(val)
        except ValueError:
            return val  # let schema validation report it
    if dtype in ("float32", "float64"):
        try:
            return float(val)
        except ValueError:
            return val
    if dtype == "bool":
        if val.lower() in ("true", "1", "yes"):
            return True
        if val.lower() in ("false", "0", "no"):
            return False
        return val
    return val


def _coerce_csv_rows(rows: List[Dict[str, Any]], features: Features) -> List[Dict[str, Any]]:
    """Coerce all CSV/TSV rows against the declared features (where field names overlap)."""
    value_dtypes: Dict[str, Optional[str]] = {}
    for name, feat in features.items():
        dtype = getattr(feat, "dtype", None)
        if isinstance(feat, ClassLabel):
            dtype = None  # handled by str2int downstream; keep strings
        value_dtypes[name] = dtype
    for row in rows:
        for name in list(row.keys()):
            if name in value_dtypes and value_dtypes[name] not in ("string", None):
                row[name] = _coerce_csv_value(row[name], value_dtypes[name])
    return rows


def load_rows(input_path: str, features: Optional[Features] = None) -> List[Dict[str, Any]]:
    """Load rows from JSONL, JSON (array), CSV, or TSV file.

    JSON files may be a top-level array, or an object with a `rows` or `data`
    key containing the array. For CSV/TSV inputs, pass `features` so string
    cells can be coerced to the declared numeric/bool dtypes (see
    `_coerce_csv_value` for why this is CSV-only).
    """
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    suffix = p.suffix.lower()
    if suffix == ".jsonl":
        rows = []
        with open(p, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON on line {line_no}: {e}")
        return rows
    if suffix == ".json":
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # Accept either {"rows": [...]} or {"data": [...]} for flexibility
            for key in ("rows", "data", "examples"):
                if key in data and isinstance(data[key], list):
                    return data[key]
        raise ValueError(
            'JSON input must be an array of objects, or {"rows": [...]} / {"data": [...]}'
        )
    if suffix in (".csv", ".tsv"):
        import csv
        with open(p, "r", encoding="utf-8", newline="") as f:
            delim = "\t" if suffix == ".tsv" else ","
            reader = csv.DictReader(f, delimiter=delim)
            rows = [dict(row) for row in reader]
        if features is not None:
            rows = _coerce_csv_rows(rows, features)
        return rows
    raise ValueError(
        f"Unsupported input format: {suffix} (supported: .jsonl, .json, .csv, .tsv)"
    )


# ─── Dedup (exact, canonical-JSON hash) ─────────────────────────────────────

def canonical_row_hash(row: Dict[str, Any]) -> str:
    """Stable hash of a row, ignoring key order (same as validate.py's check)."""
    return hashlib.sha256(
        json.dumps(row, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def drop_duplicate_rows(rows: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Exact-dedup on the canonical JSON hash. Returns (unique_rows, n_dropped)."""
    seen: set = set()
    unique: List[Dict[str, Any]] = []
    for row in rows:
        h = canonical_row_hash(row)
        if h in seen:
            continue
        seen.add(h)
        unique.append(row)
    return unique, len(rows) - len(unique)


# ─── Approximate token estimate ─────────────────────────────────────────────

def estimate_tokens(rows: List[Dict[str, Any]], features: Features) -> int:
    """Rough token estimate for a set of rows: total chars across string fields / 4.

    This is a quick sampling-budget heuristic (~4 chars/token for English text;
    CJK and code can differ by 2-3x). Use a real tokenizer when exact counts
    matter — for pretraining corpora, store the exact per-row `token_count`
    column instead (see references/schemas.md, pretraining family).
    """
    string_fields = [name for name, feat in features.items()
                     if isinstance(feat, Value) and feat.dtype == "string"]
    total_chars = 0
    for row in rows:
        for name in string_fields:
            v = row.get(name)
            if isinstance(v, str):
                total_chars += len(v)
    return total_chars // 4


# ─── Splitting ──────────────────────────────────────────────────────────────

def parse_splits(spec: str) -> Dict[str, float]:
    """Parse 'train:0.9,test:0.1' -> {"train": 0.9, "test": 0.1}."""
    parts = [s.strip() for s in spec.split(",") if s.strip()]
    if not parts:
        raise ValueError(f"Invalid splits spec: {spec!r}")
    splits = {}
    for part in parts:
        if ":" not in part:
            # Single split name with no fraction → take all
            splits[part] = 1.0
        else:
            name, frac = part.split(":", 1)
            splits[name.strip()] = float(frac.strip())
    total = sum(splits.values())
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"Split fractions must sum to 1.0, got {total}: {splits}")
    return splits


def split_rows_random(rows: List[Dict[str, Any]], splits: Dict[str, float],
                     seed: int = 42) -> Dict[str, List[Dict[str, Any]]]:
    """Shuffle and partition rows into named splits. Last split gets remainder."""
    rng = random.Random(seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    result: Dict[str, List[Dict[str, Any]]] = {}
    start = 0
    names = list(splits.keys())
    for i, (name, frac) in enumerate(splits.items()):
        if i == len(names) - 1:
            # Last split: take the remainder to avoid off-by-one
            result[name] = shuffled[start:]
        else:
            count = int(round(n * frac))
            result[name] = shuffled[start:start + count]
            start += count
    return result


def split_rows_temporal(rows: List[Dict[str, Any]], splits: Dict[str, float]) -> Dict[str, List[Dict[str, Any]]]:
    """Temporal split: assume rows are in chronological order. First N% → first split.

    Use this for time-series or any data where order matters (e.g. logs sorted by
    timestamp). The last split is the most recent; the first split is the oldest.
    """
    n = len(rows)
    result: Dict[str, List[Dict[str, Any]]] = {}
    start = 0
    names = list(splits.keys())
    for i, (name, frac) in enumerate(splits.items()):
        if i == len(names) - 1:
            result[name] = rows[start:]
        else:
            count = int(round(n * frac))
            result[name] = rows[start:start + count]
            start += count
    return result


def split_rows_stratified(rows: List[Dict[str, Any]], splits: Dict[str, float],
                         stratify_field: str, features: Features,
                         seed: int = 42) -> Dict[str, List[Dict[str, Any]]]:
    """Stratified split: balance ClassLabel values across splits.

    Useful for benchmarks (preserve answer balance) and classification
    datasets. Requires the schema to have a ClassLabel field named by
    `stratify_field`. Falls back to random split if the field is missing
    or not a ClassLabel.
    """
    if stratify_field not in features:
        raise ValueError(
            f"stratify_field {stratify_field!r} not in features. "
            f"Available: {list(features.keys())}"
        )
    feat = features[stratify_field]
    if not isinstance(feat, ClassLabel):
        raise ValueError(
            f"stratify_field {stratify_field!r} must be a ClassLabel, "
            f"got {type(feat).__name__}"
        )

    rng = random.Random(seed)
    # Group row indices by class label
    by_class: Dict[Any, List[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        val = row.get(stratify_field)
        if isinstance(val, str):
            try:
                val = feat.str2int(val)
            except Exception:
                pass  # Leave as-is; will be caught by validate.py
        by_class[val].append(i)

    # Shuffle each class's indices, then split each class according to fractions
    n = len(rows)
    split_indices: Dict[str, List[int]] = {name: [] for name in splits}
    names = list(splits.keys())
    for cls, idxs in by_class.items():
        rng.shuffle(idxs)
        m = len(idxs)
        start = 0
        for i, (name, frac) in enumerate(splits.items()):
            if i == len(names) - 1:
                split_indices[name].extend(idxs[start:])
            else:
                count = int(round(m * frac))
                split_indices[name].extend(idxs[start:start + count])
                start += count

    # Shuffle the final per-split index lists so the result isn't grouped by class
    result: Dict[str, List[Dict[str, Any]]] = {}
    for name, idxs in split_indices.items():
        rng.shuffle(idxs)
        result[name] = [rows[i] for i in idxs]
    return result


def split_rows(rows: List[Dict[str, Any]], splits: Dict[str, float],
               mode: str = "random", seed: int = 42,
               stratify_field: Optional[str] = None,
               features: Optional[Features] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Dispatch to the requested split mode."""
    if mode == "random":
        return split_rows_random(rows, splits, seed=seed)
    if mode == "temporal":
        return split_rows_temporal(rows, splits)
    if mode == "stratified":
        if not features:
            raise ValueError("stratified split requires `features` to find the ClassLabel field")
        if not stratify_field:
            # Auto-detect: use the first ClassLabel field
            cls_fields = [name for name, f in features.items() if isinstance(f, ClassLabel)]
            if not cls_fields:
                raise ValueError(
                    "stratified split requested but schema has no ClassLabel field; "
                    "use --split-mode random or temporal instead"
                )
            stratify_field = cls_fields[0]
            print(f"  Auto-detected stratify field: {stratify_field}")
        return split_rows_stratified(rows, splits, stratify_field, features, seed=seed)
    raise ValueError(f"Unknown split mode: {mode!r} (use 'random', 'temporal', or 'stratified')")


# ─── Sharding ──────────────────────────────────────────────────────────────

def parse_size(size_str: str) -> int:
    """Parse '500MB', '1GB', '100KB' -> bytes."""
    size_str = size_str.strip().upper()
    # Order matters: check longer suffixes first so 'KB' doesn't match before 'B'
    multipliers = [
        ("TB", 1024**4),
        ("GB", 1024**3),
        ("MB", 1024**2),
        ("KB", 1024),
        ("B",  1),
    ]
    for suffix, mult in multipliers:
        if size_str.endswith(suffix):
            num_str = size_str[:-len(suffix)].strip()
            if not num_str:
                continue
            try:
                num = float(num_str)
            except ValueError:
                continue
            return int(num * mult)
    # No suffix: assume bytes
    return int(float(size_str))


def _row_size_bytes(row: Dict[str, Any]) -> int:
    """Estimate a row's serialized size without crashing on non-JSON values.

    Image/Audio features carry raw `bytes`, which json.dumps rejects. For size
    estimation, bytes contribute their length; other non-JSON objects (PIL
    images, np arrays) contribute their repr length. Exactness doesn't matter
    here — this only feeds the shard-count heuristic.
    """
    def _default(o):
        if isinstance(o, (bytes, bytearray, memoryview)):
            return f"<{len(o)} bytes>"
        return repr(o)
    return len(json.dumps(row, ensure_ascii=False, default=_default).encode("utf-8"))


def shard_rows(rows: List[Dict[str, Any]], shard_size_bytes: int) -> List[List[Dict[str, Any]]]:
    """Greedy sharding: pack rows into shards until each is ~shard_size_bytes.

    For small datasets where individual rows are small, falls back to a single shard.
    Always returns at least one shard (possibly empty if `rows` is empty).
    """
    if not rows:
        return [[]]
    # Estimate average row size from first 100 rows (or all rows if fewer)
    sample = rows[:100]
    sample_bytes = sum(_row_size_bytes(r) for r in sample)
    avg_row_bytes = max(1, sample_bytes // max(1, len(sample)))
    rows_per_shard = max(1, shard_size_bytes // avg_row_bytes)
    n_shards = max(1, math.ceil(len(rows) / rows_per_shard))
    # Recompute rows_per_shard for even distribution
    rows_per_shard = math.ceil(len(rows) / n_shards)
    return [rows[i:i + rows_per_shard] for i in range(0, len(rows), rows_per_shard)]


# ─── Parquet writing ────────────────────────────────────────────────────────

def _rows_to_dataset(rows: List[Dict[str, Any]], features: Features) -> Dataset:
    """Build a `Dataset` from a list of row dicts using the given Features.

    Missing keys are filled with `None` (which `datasets` treats as null for
    nullable types — all HF Value types are nullable by default). ClassLabel
    string values are converted to ints so `from_dict` accepts them.
    """
    columnar: Dict[str, List[Any]] = {name: [] for name in features}
    for row in rows:
        for name, feat in features.items():
            val = row.get(name)
            # Convert ClassLabel string values to int (HF stores labels as ints)
            if isinstance(feat, ClassLabel) and isinstance(val, str):
                try:
                    val = feat.str2int(val)
                except Exception:
                    # Leave as-is; schema validation will flag it
                    pass
            columnar[name].append(val)
    return Dataset.from_dict(columnar, features=features)


def write_shards(rows: List[Dict[str, Any]], features: Features, split_name: str,
                 out_dir: Path, shard_size_bytes: int,
                 quiet: bool = False) -> Tuple[List[Path], int]:
    """Write rows as sharded parquet for one split.

    Returns (list of file paths, total in-memory num_bytes from Arrow tables).
    Always writes at least one shard — for an empty split, writes a single
    empty parquet file so the README's `data_files` glob still matches.
    """
    shards = shard_rows(rows, shard_size_bytes)
    n_shards = len(shards)
    paths: List[Path] = []
    total_nbytes = 0

    for i, shard_rows_list in enumerate(shards):
        # Build a Dataset for this shard with the explicit Features
        ds = _rows_to_dataset(shard_rows_list, features)
        fname = f"{split_name}-{i:05d}-of-{n_shards:05d}.parquet"
        fpath = out_dir / fname
        # Suppress tqdm progress bars from `to_parquet`
        if quiet:
            import contextlib
            import io
            with contextlib.redirect_stderr(io.StringIO()), \
                 contextlib.redirect_stdout(io.StringIO()):
                ds.to_parquet(str(fpath))
        else:
            ds.to_parquet(str(fpath))
        # Compute the in-memory Arrow byte count for this shard
        try:
            arrow_nbytes = ds.data.table.nbytes
        except Exception:
            # Fallback: estimate via Arrow table from parquet
            try:
                arrow_nbytes = pq.read_table(str(fpath)).nbytes
            except Exception:
                arrow_nbytes = fpath.stat().st_size
        total_nbytes += arrow_nbytes
        paths.append(fpath)
        if not quiet:
            print(f"  Wrote {fpath.name}  ({len(shard_rows_list)} rows, "
                  f"{fpath.stat().st_size:,} bytes, {arrow_nbytes:,} arrow bytes)")
    return paths, total_nbytes


# ─── Statistics ─────────────────────────────────────────────────────────────

def compute_stats(rows: List[Dict[str, Any]], features: Features,
                  shard_paths: List[Path], arrow_nbytes: int) -> Dict[str, Any]:
    """Compute num_examples, num_bytes, download_size for a split.

    - num_examples: row count
    - num_bytes: in-memory Arrow decoded bytes (>= download_size for compressed
      parquet; this is what HF YAML `dataset_size` expects)
    - download_size: on-disk bytes (sum of parquet file sizes; this is what HF
      YAML `download_size` expects)
    """
    num_examples = len(rows)
    download_size = sum(p.stat().st_size for p in shard_paths)
    num_bytes = arrow_nbytes if arrow_nbytes > 0 else download_size
    return {
        "num_examples": num_examples,
        "num_bytes": num_bytes,
        "download_size": download_size,
        "shards": [str(p.name) for p in shard_paths],
    }


# ─── size_categories bucketing ──────────────────────────────────────────────

def size_bucket(n: int) -> str:
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


# ─── Main pipeline ──────────────────────────────────────────────────────────

def produce_dataset(
    rows: List[Dict[str, Any]],
    features: Features,
    splits: Dict[str, float],
    out_dir: Union[str, Path],
    shard_size: str = "500MB",
    seed: int = 42,
    split_mode: str = "random",
    stratify_field: Optional[str] = None,
    quiet: bool = False,
    drop_duplicates: bool = False,
    token_estimate: bool = False,
) -> Dict[str, Any]:
    """End-to-end: split rows, shard, write parquet, compute stats.

    Args:
        drop_duplicates: exact-dedup rows (canonical JSON hash) before splitting.
            The drop count is recorded in stats.json as `duplicates_dropped`.
        token_estimate: add a heuristic chars/4 token estimate per split to
            stats.json (`estimated_tokens`) — approximate, for sampling budgets
            only; use a real tokenizer for exact counts.

    Returns a stats dict:
        {
          "splits": {<name>: {"num_examples", "num_bytes", "download_size", "shards"}},
          "total_examples": int,
          "total_download_size": int,
          "total_dataset_size": int,
          "size_categories": str,
          "shard_size": str,
          "features": <features-as-dict>,
          "duplicates_dropped": int,            # only when drop_duplicates=True
          "estimated_tokens": {<split>: int},   # only when token_estimate=True
        }
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    shard_size_bytes = parse_size(shard_size)

    # Optional exact dedup before splitting (validate.py reports the rate;
    # this flag actually drops them)
    duplicates_dropped = 0
    if drop_duplicates:
        rows, duplicates_dropped = drop_duplicate_rows(rows)
        if not quiet:
            print(f"Dropped {duplicates_dropped} exact duplicate rows "
                  f"({len(rows)} unique rows remain)")

    # Split rows
    split_rows_map = split_rows(
        rows, splits, mode=split_mode, seed=seed,
        stratify_field=stratify_field, features=features,
    )
    if not quiet:
        print(f"Split {len(rows)} rows into: "
              + ", ".join(f"{k}={len(v)}" for k, v in split_rows_map.items()))

    # Write each split as sharded parquet
    split_stats: Dict[str, Any] = {}
    for split_name, split_rows_list in split_rows_map.items():
        if not quiet:
            print(f"\nWriting split '{split_name}' ({len(split_rows_list)} rows)...")
        shard_paths, arrow_nbytes = write_shards(
            split_rows_list, features, split_name, out_dir, shard_size_bytes, quiet=quiet
        )
        split_stats[split_name] = compute_stats(
            split_rows_list, features, shard_paths, arrow_nbytes
        )

    total_examples = sum(s["num_examples"] for s in split_stats.values())
    total_download = sum(s["download_size"] for s in split_stats.values())
    total_bytes = sum(s["num_bytes"] for s in split_stats.values())

    stats = {
        "splits": split_stats,
        "total_examples": total_examples,
        "total_download_size": total_download,
        "total_dataset_size": total_bytes,
        "size_categories": size_bucket(total_examples),
        "shard_size": shard_size,
        "features": features_to_dict(features),
    }
    if drop_duplicates:
        stats["duplicates_dropped"] = duplicates_dropped
    if token_estimate:
        stats["estimated_tokens"] = {
            name: estimate_tokens(rows_list, features)
            for name, rows_list in split_rows_map.items()
        }
        stats["estimated_tokens"]["_method"] = "heuristic: total string-field chars / 4 (approximate; not a tokenizer count)"

    # Save stats.json next to the parquet files (i.e., in the parent of out_dir,
    # which is typically the dataset root, not the data/ subdir).
    stats_path = out_dir.parent / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
    if not quiet:
        print(f"\nStats written to: {stats_path}")

    return stats


def features_to_dict(features: Features) -> Dict[str, Any]:
    """Serialize Features to the dict form used in features.json."""
    return features.to_dict()


# ─── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="End-to-end dataset production pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input", required=True,
                        help="Path to input file (.jsonl / .json / .csv / .tsv)")
    parser.add_argument("--features", required=True,
                        help="Path to features.json (JSON feature spec)")
    parser.add_argument("--splits", required=True,
                        help="Split spec, e.g. 'train:0.9,test:0.1'")
    parser.add_argument("--out", required=True,
                        help="Output directory (will be created; parquet files go here)")
    parser.add_argument("--shard-size", default="500MB",
                        help="Target shard size (e.g. '500MB', '1GB', '100KB'). Default: 500MB")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for shuffling before splitting. Default: 42")
    parser.add_argument("--split-mode", choices=["random", "temporal", "stratified"],
                        default="random",
                        help="random (default), temporal (preserve order, first N% → first split), "
                             "or stratified (balance ClassLabel values across splits)")
    parser.add_argument("--stratify-field", default=None,
                        help="ClassLabel field name for stratified split. If omitted, the "
                             "first ClassLabel field in the schema is auto-detected.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress bars and per-shard log lines")
    parser.add_argument("--drop-duplicates", action="store_true",
                        help="Drop exact-duplicate rows (canonical JSON hash) before "
                             "splitting. The drop count is recorded in stats.json. "
                             "validate.py reports the duplicate rate; this flag drops them.")
    parser.add_argument("--token-estimate", action="store_true",
                        help="Add a heuristic token estimate (string chars / 4) per split "
                             "to stats.json. Approximate — use a real tokenizer for exact counts.")
    args = parser.parse_args()

    if not args.quiet:
        print(f"Loading features from: {args.features}")
    features = load_features(args.features)

    if not args.quiet:
        print(f"Loading rows from: {args.input}")
    # Pass features so CSV/TSV cells get coerced to the declared dtypes
    rows = load_rows(args.input, features=features)
    if not args.quiet:
        print(f"  Loaded {len(rows)} rows")

    if not args.quiet:
        print(f"Parsing splits: {args.splits}")
    splits = parse_splits(args.splits)

    if not args.quiet:
        print(f"Producing dataset in: {args.out}")
    stats = produce_dataset(
        rows=rows,
        features=features,
        splits=splits,
        out_dir=args.out,
        shard_size=args.shard_size,
        seed=args.seed,
        split_mode=args.split_mode,
        stratify_field=args.stratify_field,
        quiet=args.quiet,
        drop_duplicates=args.drop_duplicates,
        token_estimate=args.token_estimate,
    )

    if not args.quiet:
        print("\n=== Production complete ===")
    print(f"Total examples:  {stats['total_examples']:,}")
    print(f"Download size:   {stats['total_download_size']:,} bytes "
          f"({stats['total_download_size']/1024/1024:.1f} MB)")
    print(f"Dataset size:    {stats['total_dataset_size']:,} bytes "
          f"({stats['total_dataset_size']/1024/1024:.1f} MB)")
    print(f"Size bucket:     {stats['size_categories']}")
    if "estimated_tokens" in stats:
        est = stats["estimated_tokens"]
        total_est = sum(v for k, v in est.items() if not k.startswith("_"))
        print(f"Est. tokens:     ~{total_est:,} (heuristic chars/4 — approximate)")
    if "duplicates_dropped" in stats and stats["duplicates_dropped"]:
        print(f"Dupes dropped:   {stats['duplicates_dropped']:,}")
    print(f"\nSplits:")
    for name, s in stats["splits"].items():
        print(f"  {name}: {s['num_examples']:,} rows, "
              f"{len(s['shards'])} shard(s), "
              f"{s['download_size']:,} bytes (arrow: {s['num_bytes']:,})")


if __name__ == "__main__":
    main()

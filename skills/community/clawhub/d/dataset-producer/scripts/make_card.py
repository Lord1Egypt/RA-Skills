#!/usr/bin/env python3
"""
make_card.py — Generate README.md (YAML frontmatter + dataset card body)
for a HuggingFace dataset.

USAGE
-----
    python make_card.py \
        --name "My Dataset" \
        --license cc-by-4.0 \
        --language en \
        --task text-generation \
        --features features.json \
        --stats stats.json \
        --example example_row.json \
        --summary "A dataset of 5K instruction-following examples..." \
        --curators "Jane Doe (jane@example.org)" \
        --citation-key doe2024mydataset \
        --citation-author "Jane Doe" \
        --citation-year 2024 \
        --out /home/z/my-project/download/my_dataset/README.md

Inputs:
  --features features.json   — the same feature spec used by produce_dataset.py
  --stats stats.json         — the stats.json produced by produce_dataset.py
  --example example_row.json — a single JSON object representing one row
                               (or omit and pass --auto-example to extract the
                               first row from a parquet shard)

The script writes a complete README.md following the canonical HF dataset card
template. Edit the resulting file to fill in any sections that need
human-written prose (Curation Rationale, Annotations, Biases, etc.).
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

try:
    import yaml
except ImportError:
    print("ERROR: install pyyaml:  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Reuse the feature loader
sys.path.insert(0, str(Path(__file__).parent))
try:
    from produce_dataset import load_features, features_to_dict
    from datasets import Features, Value, Sequence, ClassLabel
except ImportError as e:
    print(f"ERROR: cannot import from produce_dataset.py: {e}", file=sys.stderr)
    sys.exit(1)


# ─── YAML frontmatter builder ──────────────────────────────────────────────
#
# We build the YAML frontmatter as direct string output rather than via
# `yaml.dump`, because the HF `class_label` block needs a specific nested
# shape (`dtype: class_label: names: '0': A`) that's fiddly to render via
# PyYAML's default dumper. Direct string building gives full control over
# the output and is easy to inspect by reading the code.

def _feature_to_yaml_lines(name: str, spec: Any, indent: int = 6) -> List[str]:
    """Render a single feature field as YAML lines.

    `spec` is the dict form produced by `Features.to_dict()`, i.e. it has
    `_type` keys for each level. We handle:
      - Value            -> `- name: <name>\n  dtype: <dtype>`
      - ClassLabel       -> `- name: <name>\n  dtype:\n    class_label:\n      names:\n        '0': A\n...`
      - List/Sequence of Value  -> `- name: <name>\n  sequence: <dtype>`
      - List/Sequence of struct -> `- name: <name>\n  list:\n    - name: <field>\n      dtype: ...`
      - struct/dict     -> `- name: <name>\n  struct:\n    - name: <field>\n      dtype: ...`
      - bare dict (Features.to_dict() drops _type:struct) -> treated as struct
    """
    pad = " " * indent
    lines = [f"{pad}- name: {name}"]

    if not isinstance(spec, dict):
        # Short-form media types that Features.to_dict() emits as bare strings
        if isinstance(spec, str) and spec in ("Image", "Audio", "Video"):
            lines.append(f"{pad}  dtype: {spec.lower()}")
        else:
            lines.append(f"{pad}  dtype: string")
        return lines

    t = spec.get("_type", "")

    if t == "Value":
        lines.append(f"{pad}  dtype: {spec['dtype']}")
        return lines

    # Media features — HF's own DatasetInfo export renders these as
    # `dtype: image` / `dtype: audio` / `dtype: video` (lowercase).
    if t == "Image":
        lines.append(f"{pad}  dtype: image")
        return lines
    if t == "Audio":
        lines.append(f"{pad}  dtype: audio")
        return lines
    if t == "Video":
        lines.append(f"{pad}  dtype: video")
        return lines

    if t == "ClassLabel":
        names = spec.get("names", [])
        lines.append(f"{pad}  dtype:")
        lines.append(f"{pad}    class_label:")
        lines.append(f"{pad}      names:")
        for i, n in enumerate(names):
            # json.dumps double-quotes + escapes the label value. A double-
            # quoted YAML scalar accepts exactly JSON escaping rules, so this
            # is safe for labels containing ': ', '#', quotes, or leading
            # digits like '2024' / 'true' that YAML would otherwise re-type.
            lines.append(f"{pad}        '{i}': {json.dumps(str(n))}")
        return lines

    if t in ("Sequence", "List"):
        inner = spec.get("feature", {})
        if isinstance(inner, dict) and inner.get("_type") == "Value":
            # Scalar sequence: `sequence: <dtype>`
            lines.append(f"{pad}  sequence: {inner['dtype']}")
            return lines
        # Struct sequence: `list:` + nested field blocks
        lines.append(f"{pad}  list:")
        if isinstance(inner, dict) and inner.get("_type") in ("struct", "dict"):
            fields = inner.get("fields", inner)
        elif isinstance(inner, dict) and "_type" not in inner:
            # Features.to_dict() drops _type:struct — bare dict of fields
            fields = inner
        else:
            fields = inner
        for fname, fspec in fields.items():
            lines.extend(_feature_to_yaml_lines(fname, fspec, indent=indent + 4))
        return lines

    if t in ("struct", "dict"):
        lines.append(f"{pad}  struct:")
        fields = spec.get("fields", spec)
        for fname, fspec in fields.items():
            lines.extend(_feature_to_yaml_lines(fname, fspec, indent=indent + 4))
        return lines

    # Fallback: bare dict of fields (no _type). This is how `Features.to_dict()`
    # represents a struct at the top level (e.g. the `answers` field in SQuAD).
    if "_type" not in spec and ("dtype" not in spec):
        lines.append(f"{pad}  struct:")
        for fname, fspec in spec.items():
            lines.extend(_feature_to_yaml_lines(fname, fspec, indent=indent + 4))
        return lines

    # Unknown — fall back to string
    lines.append(f"{pad}  dtype: string")
    return lines


def features_to_yaml_lines(features_dict: Dict[str, Any], indent: int = 6) -> List[str]:
    """Render all features as YAML lines (the `dataset_info.features` block)."""
    lines: List[str] = []
    for name, spec in features_dict.items():
        lines.extend(_feature_to_yaml_lines(name, spec, indent=indent))
    return lines


def build_yaml_frontmatter(
    name: str,
    namespace: Optional[str],
    license: str,
    languages: List[str],
    task_categories: List[str],
    task_ids: List[str],
    features_dict: Dict[str, Any],
    splits_stats: Dict[str, Dict[str, Any]],
    total_download_size: int,
    total_dataset_size: int,
    size_categories: str,
    pretty_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    language_creators: Optional[List[str]] = None,
    annotations_creators: Optional[List[str]] = None,
    source_datasets: Optional[List[str]] = None,
    multilinguality: Optional[List[str]] = None,
    configs: Optional[List[Dict[str, Any]]] = None,
    viewer: Optional[bool] = None,
) -> str:
    """Build the YAML frontmatter block (without the surrounding --- fences).

    Returns a string ready to be sandwiched between `---` lines.
    """
    pretty = pretty_name or name
    namespace = namespace or "local"

    # Build configs block (default to single config pointing at data/<split>-*.parquet)
    if configs is None:
        config_data_files = []
        for split_name in splits_stats.keys():
            config_data_files.append({
                "split": split_name,
                "path": f"data/{split_name}-*.parquet",
            })
        configs = [{
            "config_name": "default",
            "default": True,
            "data_files": config_data_files,
        }]

    # Top-level metadata lines (order matters for HF UI readability)
    lines: List[str] = []
    lines.append(f"license: {license}")
    lines.append("language:")
    for lang in languages:
        lines.append(f"  - {lang}")
    lines.append(f"pretty_name: {pretty}")
    # size_categories is a single string (NOT a list) — wrap in quotes to
    # avoid YAML parser confusion with the `<` characters.
    lines.append(f'size_categories: "{size_categories}"')
    lines.append("task_categories:")
    for task in task_categories:
        lines.append(f"  - {task}")
    if task_ids:
        lines.append("task_ids:")
        for tid in task_ids:
            lines.append(f"  - {tid}")
    if language_creators:
        lines.append("language_creators:")
        for lc in language_creators:
            lines.append(f"  - {lc}")
    if annotations_creators:
        lines.append("annotations_creators:")
        for ac in annotations_creators:
            lines.append(f"  - {ac}")
    if source_datasets:
        lines.append("source_datasets:")
        for sd in source_datasets:
            lines.append(f"  - {sd}")
    if multilinguality:
        lines.append("multilinguality:")
        for m in multilinguality:
            lines.append(f"  - {m}")
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
    if viewer is not None:
        lines.append(f"viewer: {'true' if viewer else 'false'}")

    # configs block
    lines.append("configs:")
    for cfg in configs:
        lines.append(f"  - config_name: {cfg['config_name']}")
        if cfg.get("default"):
            lines.append(f"    default: true")
        lines.append("    data_files:")
        for entry in cfg.get("data_files", []):
            if "split" in entry and "path" in entry:
                lines.append(f"      - split: {entry['split']}")
                lines.append(f"        path: {entry['path']}")
            elif "split" in entry and "paths" in entry:
                lines.append(f"      - split: {entry['split']}")
                lines.append(f"        path:")
                for p in entry["paths"]:
                    lines.append(f"          - {p}")

    # dataset_info block (single-config dict form). For multi-config use list
    # form — but make_card.py only generates single-config; multi-config users
    # edit the README manually.
    lines.append("dataset_info:")
    lines.append("  features:")
    # Append feature lines (already indented to 6 spaces by _feature_to_yaml_lines)
    feat_lines = features_to_yaml_lines(features_dict, indent=6)
    # Strip the leading 6-space indent so they nest under `features:` (4 spaces
    # + 2 spaces = 6 spaces from _feature_to_yaml_lines → need to remove 4 to nest
    # under `features:` which is at 2-space indent)
    for line in feat_lines:
        # Each feature line has 6 spaces; we want 4 spaces under `features:`.
        if line.startswith("      "):
            lines.append(line[2:])  # strip 2 spaces so it's now 4-space indented
        else:
            lines.append(line)

    lines.append("  splits:")
    for split_name, s in splits_stats.items():
        lines.append(f"    - name: {split_name}")
        lines.append(f"      num_bytes: {s.get('num_bytes', 0)}")
        lines.append(f"      num_examples: {s.get('num_examples', 0)}")
    lines.append(f"  download_size: {total_download_size}")
    lines.append(f"  dataset_size: {total_dataset_size}")

    return "\n".join(lines) + "\n"


# ─── Markdown body builder ─────────────────────────────────────────────────

def build_markdown_body(
    name: str,
    namespace: Optional[str],
    pretty_name: str,
    summary: str,
    languages: List[str],
    task_categories: List[str],
    splits_stats: Dict[str, Dict[str, Any]],
    features_dict: Dict[str, Any],
    example_row: Dict[str, Any],
    license: str,
    curators: str,
    citation_key: str,
    citation_author: str,
    citation_year: int,
    homepage: Optional[str] = None,
    repository: Optional[str] = None,
    paper: Optional[str] = None,
    leaderboard: Optional[str] = None,
    contact: Optional[str] = None,
    source_data_description: Optional[str] = None,
    annotations_description: Optional[str] = None,
    pii_description: Optional[str] = None,
    social_impact: Optional[str] = None,
    biases: Optional[str] = None,
    limitations: Optional[str] = None,
) -> str:
    """Build the markdown body (everything after the YAML frontmatter)."""
    pretty = pretty_name or name

    # Languages string
    langs_str = ", ".join(languages) if languages else "N/A"

    # Tasks string
    tasks_str = ", ".join(task_categories) if task_categories else "N/A"

    # Splits table
    splits_table = "| Split | Num Examples | Num Bytes | Shards |\n|---|---|---|---|\n"
    for split_name, s in splits_stats.items():
        n_shards = len(s.get("shards", []))
        splits_table += f"| `{split_name}` | {s.get('num_examples', 0):,} | {s.get('num_bytes', 0):,} | {n_shards} |\n"

    # Data fields bullet list
    fields_md = ""
    for fname, spec in features_dict.items():
        if not isinstance(spec, dict):
            continue
        t = spec.get("_type", "")
        if t == "Value":
            type_str = f"`{spec['dtype']}`"
        elif t == "ClassLabel":
            type_str = f"`ClassLabel` (names: {spec.get('names', [])})"
        elif t in ("Image", "Audio", "Video"):
            type_str = f"`{t}`"
        elif t in ("Sequence", "List"):
            inner = spec.get("feature", {})
            if isinstance(inner, dict) and inner.get("_type") == "Value":
                type_str = f"`list of {inner['dtype']}`"
            else:
                type_str = "`list of structs`"
        elif t in ("struct", "dict"):
            type_str = "`struct`"
        elif "_type" not in spec:
            # Bare dict from Features.to_dict() — likely a struct
            type_str = "`struct`"
        else:
            type_str = "(unknown type)"
        fields_md += f"- `{fname}` ({type_str}): [describe what this field contains]\n"

    # Example row JSON (formatted)
    example_json = json.dumps(example_row, indent=2, ensure_ascii=False)

    # Year
    year = citation_year or datetime.now().year

    # Hub URL — only include if a namespace was provided
    hub_url = f"https://huggingface.co/datasets/{namespace}/{name}" if namespace else None
    # NOTE: single backslash — BibTeX renders `\url` as a LaTeX line break.
    howpublished = f"\\url{{{hub_url}}}" if hub_url else "N/A"

    md = f"""# Dataset Card for {pretty}

## Table of Contents

- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** {homepage or "N/A"}
- **Repository:** {repository or "N/A"}
- **Paper:** {paper or "N/A"}
- **Leaderboard:** {leaderboard or "N/A"}
- **Point of Contact:** {contact or "N/A"}

### Dataset Summary

{summary or "[More Information Needed: write 1–3 paragraphs covering what the dataset is, how many examples, and why it exists.]"}

### Supported Tasks and Leaderboards

{tasks_str}

[More Information Needed: describe which tasks the dataset supports and any leaderboards it appears on.]

### Languages

{langs_str}

[More Information Needed: BCP-47 codes + plain-language description.]

## Dataset Structure

### Data Instances

A single example from the dataset:

```json
{example_json}
```

### Data Fields

{fields_md or "[More Information Needed]"}

### Data Splits

{splits_table}

[More Information Needed: explain the split rationale — random split, temporal split, held-out test set, etc.]

## Dataset Creation

### Curation Rationale

[More Information Needed: why was this dataset built? What gap does it fill? What design choices were made?]

### Source Data

#### Initial Data Collection and Normalization

{source_data_description or "[More Information Needed: where the raw data came from; what cleaning was done.]"}

#### Who are the source language producers?

[More Information Needed: demographics of original authors, or which LLM generated the data, etc.]

### Annotations

#### Annotation process

{annotations_description or "[More Information Needed: how labels/scores were produced.]"}

#### Who are the annotators?

[More Information Needed: annotator demographics, pay, training. For LLM-judged: which model and version.]

### Personal and Sensitive Information

{pii_description or "[More Information Needed: PII scan results, removal-request process.]"}

## Considerations for Using the Data

### Social Impact of Dataset

{social_impact or "[More Information Needed: risks, dual-use concerns, intended-use statement.]"}

### Discussion of Biases

{biases or "[More Information Needed: known biases — gender, racial, cultural, political, linguistic. Don't claim 'no biases' — every dataset has them.]"}

### Other Known Limitations

{limitations or "[More Information Needed: coverage gaps, annotation noise, contamination, temporal drift. Be honest.]"}

## Additional Information

### Dataset Curators

{curators or "[More Information Needed]"}

### Licensing Information

This dataset is released under the `{license}` license. See the [LICENSE](LICENSE) file for the full text.

### Citation Information

If you use this dataset, please cite:

```bibtex
@misc{{{citation_key},
  title         = {{{pretty}}},""" + (f"""
  author        = {{{citation_author}}},""" if citation_author else "") + f"""
  year          = {{{year}}},""" + (f"""
  howpublished  = {{{howpublished}}},""" if hub_url else "") + f"""
}}
```

### Contributions

Thanks to the dataset curators for adding this dataset. To contribute, please open a pull request or issue on the dataset repository.
"""
    return md


# ─── License text lookup ───────────────────────────────────────────────────

# Common SPDX IDs and their short label + URL
LICENSE_INFO = {
    "cc-by-4.0":         ("Creative Commons Attribution 4.0 International", "https://creativecommons.org/licenses/by/4.0/"),
    "cc-by-sa-4.0":      ("Creative Commons Attribution-ShareAlike 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
    "cc-by-nc-4.0":      ("Creative Commons Attribution-NonCommercial 4.0", "https://creativecommons.org/licenses/by-nc/4.0/"),
    "cc-by-nc-sa-4.0":   ("Creative Commons Attribution-NonCommercial-ShareAlike 4.0", "https://creativecommons.org/licenses/by-nc-sa/4.0/"),
    "cc0-1.0":           ("Creative Commons Zero v1.0 Universal (Public Domain)", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "mit":               ("MIT License", "https://opensource.org/licenses/MIT"),
    "apache-2.0":        ("Apache License 2.0", "https://www.apache.org/licenses/LICENSE-2.0"),
    "bsd-3-clause":      ("BSD 3-Clause License", "https://opensource.org/licenses/BSD-3-Clause"),
    "bsd-2-clause":      ("BSD 2-Clause License", "https://opensource.org/licenses/BSD-2-Clause"),
    "gpl-3.0":           ("GNU General Public License v3.0", "https://www.gnu.org/licenses/gpl-3.0.html"),
    "mpl-2.0":           ("Mozilla Public License 2.0", "https://www.mozilla.org/en-US/MPL/2.0/"),
    "odc-by":            ("Open Data Commons Attribution License v1.0", "https://opendatacommons.org/licenses/by/1-0/"),
    "unlicense":         ("The Unlicense", "https://unlicense.org/"),
}


# ─── Auto-extract example row from a parquet shard ────────────────────────

def auto_extract_example_row(data_dir: Path) -> Optional[Dict[str, Any]]:
    """Try to extract the first row from the first parquet shard in `data_dir`.

    Returns the row as a dict, or None if no parquet was found. Used as a
    convenience for `--auto-example` so the user doesn't have to manually
    write an example_row.json.
    """
    if not data_dir.exists() or not data_dir.is_dir():
        return None
    # Find any parquet file in the data dir (prefer a train shard, then any)
    parquet_files = sorted(data_dir.glob("*.parquet"))
    if not parquet_files:
        return None
    # Prefer train shard, then any
    train_shards = [p for p in parquet_files if p.name.startswith("train-")]
    target = train_shards[0] if train_shards else parquet_files[0]
    try:
        from datasets import load_dataset
        # Use split='train' if available, else use the first split
        ds = load_dataset(str(data_dir))
        split_names = list(ds.keys())
        if not split_names:
            return None
        first_split = split_names[0]
        if not ds[first_split].num_rows:
            # Try other splits
            for sn in split_names[1:]:
                if ds[sn].num_rows:
                    first_split = sn
                    break
            else:
                return None
        row = ds[first_split][0]
        # Convert any non-JSON-serializable objects (e.g. PIL images) to repr
        return _serialize_row(row)
    except Exception as e:
        print(f"  Warning: auto-extract failed: {e}", file=sys.stderr)
        return None


def _serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Make a row JSON-serializable by converting non-serializable values to strings."""
    out = {}
    for k, v in row.items():
        try:
            json.dumps(v)
            out[k] = v
        except (TypeError, ValueError):
            out[k] = repr(v) if not isinstance(v, list) else [
                (repr(x) if not _is_jsonable(x) else x) for x in v
            ]
    return out


def _is_jsonable(x: Any) -> bool:
    try:
        json.dumps(x)
        return True
    except (TypeError, ValueError):
        return False


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate README.md for a HuggingFace dataset.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--name", required=True, help="Dataset name (repo name, e.g. 'my_dataset')")
    parser.add_argument("--namespace", default=None,
                        help="HF namespace (org or username). Optional — if omitted, "
                             "the citation block won't include a Hub URL.")
    parser.add_argument("--license", required=True, help="SPDX license ID (e.g. cc-by-4.0)")
    parser.add_argument("--language", required=True, help="Comma-separated ISO 639-1 codes (e.g. 'en,hi')")
    parser.add_argument("--task", required=True, help="Comma-separated task_categories (e.g. 'text-generation')")
    parser.add_argument("--task-ids", default="", help="Comma-separated task_ids (optional)")
    parser.add_argument("--pretty-name", default=None, help="Human-readable name (defaults to --name)")
    parser.add_argument("--features", required=True, help="features.json path")
    parser.add_argument("--stats", required=True, help="stats.json path (from produce_dataset.py)")
    parser.add_argument("--example", default=None, help="example_row.json path (single JSON object)")
    parser.add_argument("--auto-example", action="store_true",
                        help="Auto-extract the first row from a parquet shard in the "
                             "dataset's data/ directory. Looks for the README's parent "
                             "data/ subdir by default (override with --data-dir).")
    parser.add_argument("--data-dir", default=None,
                        help="Path to data/ directory (for --auto-example). Defaults to "
                             "<README parent>/data/")
    parser.add_argument("--summary", default="", help="Dataset summary text (1-3 paragraphs)")
    parser.add_argument("--curators", default="", help="Dataset curators line")
    parser.add_argument("--citation-key", default="", help="BibTeX citation key (e.g. 'doe2024mydataset')")
    parser.add_argument("--citation-author", default="", help="BibTeX author field")
    parser.add_argument("--citation-year", type=int, default=None, help="BibTeX year")
    parser.add_argument("--homepage", default=None)
    parser.add_argument("--repository", default=None)
    parser.add_argument("--paper", default=None)
    parser.add_argument("--leaderboard", default=None)
    parser.add_argument("--contact", default=None)
    parser.add_argument("--source-data", default=None, help="Source data description")
    parser.add_argument("--annotations", default=None, help="Annotations description")
    parser.add_argument("--pii", default=None, help="PII scan results description")
    parser.add_argument("--social-impact", default=None)
    parser.add_argument("--biases", default=None)
    parser.add_argument("--limitations", default=None)
    parser.add_argument("--tags", default="", help="Comma-separated free-form tags")
    parser.add_argument("--out", required=True, help="Output README.md path")
    args = parser.parse_args()

    # Load inputs
    print(f"Loading features from: {args.features}")
    features = load_features(args.features)
    features_dict = features_to_dict(features)

    print(f"Loading stats from: {args.stats}")
    with open(args.stats) as f:
        stats = json.load(f)

    # Get example row
    example_row = None
    if args.example:
        print(f"Loading example row from: {args.example}")
        with open(args.example) as f:
            example_row = json.load(f)
    elif args.auto_example:
        # Auto-extract from parquet
        out_path = Path(args.out)
        data_dir = Path(args.data_dir) if args.data_dir else out_path.parent / "data"
        print(f"Auto-extracting example row from parquet in: {data_dir}")
        example_row = auto_extract_example_row(data_dir)
        if example_row is None:
            print("  Warning: could not auto-extract example row; using a placeholder.",
                  file=sys.stderr)
            example_row = {name: "<example value>" for name in features_dict}
    else:
        # No example provided; use placeholder
        print("  No --example or --auto-example; using placeholder row.", file=sys.stderr)
        example_row = {name: "<example value>" for name in features_dict}

    # Parse lists
    languages = [s.strip() for s in args.language.split(",") if s.strip()]
    task_categories = [s.strip() for s in args.task.split(",") if s.strip()]
    task_ids = [s.strip() for s in args.task_ids.split(",") if s.strip()]
    tags = [s.strip() for s in args.tags.split(",") if s.strip()] if args.tags else None

    # Build YAML
    yaml_str = build_yaml_frontmatter(
        name=args.name,
        namespace=args.namespace,
        license=args.license,
        languages=languages,
        task_categories=task_categories,
        task_ids=task_ids,
        features_dict=features_dict,
        splits_stats=stats["splits"],
        total_download_size=stats["total_download_size"],
        total_dataset_size=stats["total_dataset_size"],
        size_categories=stats["size_categories"],
        pretty_name=args.pretty_name,
        tags=tags,
    )

    # Build markdown body
    md_body = build_markdown_body(
        name=args.name,
        namespace=args.namespace,
        pretty_name=args.pretty_name or args.name,
        summary=args.summary,
        languages=languages,
        task_categories=task_categories,
        splits_stats=stats["splits"],
        features_dict=features_dict,
        example_row=example_row,
        license=args.license,
        curators=args.curators,
        citation_key=args.citation_key or f"{args.name}{datetime.now().year}",
        citation_author=args.citation_author or args.curators,
        citation_year=args.citation_year or datetime.now().year,
        homepage=args.homepage,
        repository=args.repository,
        paper=args.paper,
        leaderboard=args.leaderboard,
        contact=args.contact,
        source_data_description=args.source_data,
        annotations_description=args.annotations,
        pii_description=args.pii,
        social_impact=args.social_impact,
        biases=args.biases,
        limitations=args.limitations,
    )

    # Write
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml_str)
        f.write("---\n\n")
        f.write(md_body)

    print(f"\nREADME.md written to: {out_path}")
    print(f"  ({out_path.stat().st_size:,} bytes)")
    print(f"\nNext steps:")
    print(f"  1. Edit the README.md to fill in [More Information Needed] sections")
    print(f"  2. Copy a LICENSE file to the dataset root: {out_path.parent}/LICENSE")
    print(f"  3. Copy create_dataset.py to the dataset root: {out_path.parent}/create_dataset.py")
    print(f"  4. Run smoke_test.py to verify load_dataset() works")


if __name__ == "__main__":
    main()

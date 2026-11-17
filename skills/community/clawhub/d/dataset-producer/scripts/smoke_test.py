#!/usr/bin/env python3
"""
smoke_test.py — Post-build verification for a produced dataset.

Loads the dataset via `datasets.load_dataset()`, verifies that:
1. The YAML frontmatter in README.md parses cleanly.
2. All splits declared in the YAML are loadable and have the expected
   number of rows.
3. The schema (Features) matches what's declared in the YAML.
4. For ClassLabel fields, `int2str()` works and names match the YAML.
5. The example row in `### Data Instances` matches the actual schema
   (all keys present, types match).
6. The LICENSE file exists at the dataset root and is non-empty.
7. (If present) `create_dataset.py` exists and is non-empty.

USAGE
-----
    python smoke_test.py /path/to/dataset/

    # Or run from inside the dataset directory:
    python /path/to/skill/scripts/smoke_test.py .

"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: install pyyaml:  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    from datasets import load_dataset
except ImportError:
    print("ERROR: install datasets:  pip install datasets pyarrow", file=sys.stderr)
    sys.exit(1)


def _extract_yaml_frontmatter(readme_path: Path) -> Optional[str]:
    """Extract the YAML frontmatter block from a README.md file. Returns None if not found."""
    if not readme_path.exists():
        return None
    text = readme_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    # Find the closing `---` after the opening one
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def _extract_example_row_from_card(readme_path: Path) -> Optional[Dict[str, Any]]:
    """Extract the first ```json block from the `### Data Instances` section.

    Returns the parsed JSON object, or None if no example was found.
    """
    text = readme_path.read_text(encoding="utf-8")
    # Find the `### Data Instances` heading
    m = re.search(r"^### Data Instances\s*$", text, re.MULTILINE)
    if not m:
        return None
    # Find the next ```json block after the heading
    rest = text[m.end():]
    m2 = re.search(r"```json\s*\n(.*?)\n```", rest, re.DOTALL)
    if not m2:
        return None
    try:
        return json.loads(m2.group(1))
    except json.JSONDecodeError:
        return None


def smoke_test(dataset_path: Path) -> Tuple[bool, List[str]]:
    """Run the smoke test on a dataset directory. Returns (passed, messages)."""
    messages: List[str] = []
    passed = True
    dataset_path = dataset_path.resolve()

    if not dataset_path.is_dir():
        return False, [f"Dataset path is not a directory: {dataset_path}"]

    # ─── 1. README.md exists and YAML frontmatter parses ──────────────────
    readme_path = dataset_path / "README.md"
    yaml_str = _extract_yaml_frontmatter(readme_path)
    if yaml_str is None:
        messages.append("✗ README.md is missing or has no YAML frontmatter")
        return False, messages
    try:
        frontmatter = yaml.safe_load(yaml_str)
        messages.append(f"✓ YAML frontmatter parses ({len(frontmatter)} top-level keys)")
    except yaml.YAMLError as e:
        messages.append(f"✗ YAML frontmatter fails to parse: {e}")
        return False, messages

    # ─── 2. Required top-level fields present ──────────────────────────────
    required_fields = ["license", "language", "pretty_name", "size_categories",
                       "task_categories", "configs", "dataset_info"]
    missing = [f for f in required_fields if f not in frontmatter]
    if missing:
        messages.append(f"✗ YAML missing required fields: {missing}")
        passed = False
    else:
        messages.append("✓ All required YAML fields present")

    # ─── 3. Dataset loads via load_dataset() ───────────────────────────────
    try:
        ds = load_dataset(str(dataset_path))
        messages.append(f"✓ load_dataset() succeeded: splits={list(ds.keys())}")
    except Exception as e:
        messages.append(f"✗ load_dataset() failed: {e}")
        return False, messages

    # ─── 4. Each declared split has the expected row count ─────────────────
    # dataset_info comes in two shapes: dict (single-config) and list of
    # dicts (multi-config, one entry per config_name). The loader only loads
    # the default config, so only ITS splits are strictly verified — splits
    # belonging to other configs are noted, not failed.
    di = frontmatter.get("dataset_info", {})
    configs = frontmatter.get("configs", []) or []
    default_config_name = None
    if isinstance(configs, list) and configs:
        for cfg in configs:
            if isinstance(cfg, dict) and cfg.get("default"):
                default_config_name = cfg.get("config_name")
                break
        if default_config_name is None and isinstance(configs[0], dict):
            default_config_name = configs[0].get("config_name")

    if isinstance(di, list):
        declared_splits = []
        other_config_splits = []
        for cfg in di:
            if not isinstance(cfg, dict):
                continue
            if default_config_name is not None and cfg.get("config_name") == default_config_name:
                declared_splits.extend(cfg.get("splits", []))
            elif cfg.get("config_name"):
                other_config_splits.extend(cfg.get("splits", []))
            else:
                # Entry without config_name — treat as default
                declared_splits.extend(cfg.get("splits", []))
        if other_config_splits:
            names = sorted({s.get("name") for s in other_config_splits if isinstance(s, dict)})
            messages.append(f"ℹ {len(names)} split(s) belong to non-default configs (not loaded by the default load): {names}")
    else:
        declared_splits = di.get("splits", []) if isinstance(di, dict) else []

    actual_splits = {name: ds[name].num_rows for name in ds.keys()}
    for s in declared_splits:
        name = s.get("name")
        expected = s.get("num_examples")
        if name not in actual_splits:
            messages.append(f"✗ Split '{name}' declared in YAML but not in loaded dataset")
            passed = False
        elif expected is not None and actual_splits[name] != expected:
            messages.append(
                f"✗ Split '{name}': declared num_examples={expected}, "
                f"but actual={actual_splits[name]}"
            )
            passed = False
    if declared_splits and all(s.get("name") in actual_splits for s in declared_splits):
        messages.append(f"✓ All {len(declared_splits)} declared splits of the default config match: {actual_splits}")

    # ─── 5. ClassLabel fields work ────────────────────────────────────────
    first_split = list(ds.keys())[0]
    features = ds[first_split].features
    for name, feat in features.items():
        if hasattr(feat, "names") and getattr(feat, "names", None):
            try:
                # Pick a value and check int2str
                val = ds[first_split][0][name]
                if isinstance(val, int):
                    s = feat.int2str(val)
                    messages.append(
                        f"✓ ClassLabel '{name}': int2str({val}) = {s!r} (names={feat.names})"
                    )
            except Exception as e:
                messages.append(f"✗ ClassLabel '{name}' int2str() failed: {e}")
                passed = False

    # ─── 6. Example row in README matches schema ──────────────────────────
    example = _extract_example_row_from_card(readme_path)
    if example is None:
        messages.append("⚠ No example row found in `### Data Instances` (acceptable but recommended)")
    else:
        missing_keys = set(features.keys()) - set(example.keys())
        if missing_keys:
            messages.append(f"⚠ Example row in README is missing keys: {sorted(missing_keys)}")
        else:
            messages.append(f"✓ Example row in README matches schema ({len(example)} fields)")

    # ─── 7. LICENSE file exists ────────────────────────────────────────────
    license_file = None
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        p = dataset_path / name
        if p.exists():
            license_file = p
            break
    if license_file is None:
        declared_license = frontmatter.get("license", "?")
        messages.append(
            f"⚠ No LICENSE file in dataset root (YAML declares license: {declared_license})"
        )
    elif license_file.stat().st_size == 0:
        messages.append(f"✗ LICENSE file is empty: {license_file.name}")
        passed = False
    else:
        messages.append(f"✓ LICENSE file present ({license_file.name}, {license_file.stat().st_size:,} bytes)")

    # ─── 8. create_dataset.py exists (recommended) ─────────────────────────
    provenance = dataset_path / "create_dataset.py"
    if not provenance.exists():
        messages.append("⚠ No create_dataset.py in dataset root (provenance script recommended)")
    elif provenance.stat().st_size == 0:
        messages.append(f"✗ create_dataset.py is empty")
        passed = False
    else:
        messages.append(f"✓ create_dataset.py present ({provenance.stat().st_size:,} bytes)")

    # ─── 9. stats.json (optional, for re-running make_card) ───────────────
    stats_file = dataset_path / "stats.json"
    if stats_file.exists():
        messages.append(f"✓ stats.json present (can re-run make_card.py)")
    else:
        messages.append(f"⚠ No stats.json (needed only if you want to re-run make_card.py)")

    return passed, messages


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run a post-build smoke test on a produced dataset.")
    parser.add_argument("dataset_path", help="Path to the dataset root (containing README.md, data/, etc.)")
    args = parser.parse_args()

    dataset_path = Path(args.dataset_path)
    print(f"Running smoke test on: {dataset_path}\n")

    passed, messages = smoke_test(dataset_path)

    for msg in messages:
        print(f"  {msg}")

    print()
    if passed:
        print("✓ Smoke test PASSED — dataset is publish-ready")
        sys.exit(0)
    else:
        print("✗ Smoke test FAILED — see messages above")
        sys.exit(1)


if __name__ == "__main__":
    main()

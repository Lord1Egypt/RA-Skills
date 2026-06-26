#!/usr/bin/env python3
"""
normalize_terms.py
==================

This script normalises recognised characters from ancient manuscripts by
mapping them to standardised forms using a lookup table defined in a YAML
file. It produces a JSON file containing the original character, its list
of normalised variants, its type and notes, along with the original
confidence score.

Usage::

    python normalize_terms.py --input path/to/recognized_chars.json --workspace path/to/workspace

The script expects the alias mapping at
`assets/data/historical_aliases.yaml` relative to this script's directory.
The output is written to the `term_normalisation/` folder inside the
specified workspace.
"""

import argparse
import json
from pathlib import Path
import sys


def load_aliases(path):
    """Load alias rules from a YAML file. Returns a dict of mappings."""
    try:
        import yaml
    except ImportError:
        print("PyYAML is required to run this script. Please install pyyaml.", file=sys.stderr)
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def normalize_terms(recognized, aliases):
    """
    Given a list of recognized characters and an alias mapping, produce
    normalised term objects.
    """
    results = []
    for item in recognized:
        text = item.get('text')
        conf = item.get('confidence')
        rule = aliases.get(text, {})
        normalized_list = rule.get('aliases', [text])
        entry_type = rule.get('type', 'unknown')
        note = rule.get('note', '')
        results.append({
            'original': text,
            'normalized': normalized_list,
            'type': entry_type,
            'note': note,
            'confidence': conf
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Normalise recognised characters using alias rules.")
    parser.add_argument('--input', required=True, help='Path to recognized_chars.json file')
    parser.add_argument('--workspace', required=True, help='Path to the workspace directory')
    args = parser.parse_args()

    input_path = Path(args.input)
    workspace = Path(args.workspace)
    output_dir = workspace / 'term_normalisation'
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load input
    data = json.loads(input_path.read_text(encoding='utf-8'))
    recognized = data.get('recognized_chars')
    if recognized is None:
        print("Input JSON must contain a 'recognized_chars' key.", file=sys.stderr)
        sys.exit(1)

    # Load aliases
    script_dir = Path(__file__).parent
    alias_file = script_dir.parent / 'assets' / 'data' / 'historical_aliases.yaml'
    aliases = load_aliases(alias_file)

    normalized = normalize_terms(recognized, aliases)

    # Write output
    out_json = {'normalized_terms': normalized}
    out_path = output_dir / 'normalized_terms.json'
    out_path.write_text(json.dumps(out_json, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Normalised {len(normalized)} term(s) to {out_path}")


if __name__ == '__main__':
    main()
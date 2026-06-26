import argparse
import json
from typing import List, Dict


def generate_table(channels: List[Dict[str, str]]) -> str:
    """
    Generate a markdown channel plan table from a list of channel definitions.

    Each channel dict may contain:
      - name
      - role
      - format
      - message
      - cta
      - canonical
    Missing fields will be rendered as empty cells.
    """
    headers = [
        "Channel",
        "Role / Objective",
        "Format / Asset Type",
        "Primary Message / Angle",
        "Primary CTA",
        "Canonical Target",
    ]
    lines = []
    # Header
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")

    for ch in channels:
        row = [
            ch.get("name", ""),
            ch.get("role", ""),
            ch.get("format", ""),
            ch.get("message", ""),
            ch.get("cta", ""),
            ch.get("canonical", ""),
        ]
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a markdown channel plan table for geo-content-publisher.\n\n"
            "Input JSON format example:\n"
            '[{"name": "Website LP", "role": "GEO anchor", '
            '"format": "Landing page", "message": "Core value prop", '
            '"cta": "Start trial", "canonical": "/product"}]'
        )
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to JSON file containing a list of channel definitions.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional path to write the markdown table to. Prints to stdout if omitted.",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of channel objects.")

    table_md = generate_table(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(table_md)
    else:
        print(table_md)


if __name__ == "__main__":
    main()


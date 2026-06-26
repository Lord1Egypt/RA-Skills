import argparse
from pathlib import Path
import re
import sys


def count_words(file_path):
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    return len([word for word in re.split(r"\s+", text.strip()) if word])


def build_parser():
    parser = argparse.ArgumentParser(description="Verify whether a summary matches a target compression ratio.")
    parser.add_argument("original_file", help="Path to the original source text")
    parser.add_argument("summary_file", help="Path to the generated summary file")
    parser.add_argument("--target-ratio", type=float, default=0.20, help="Expected summary ratio")
    parser.add_argument("--tolerance", type=float, default=0.02, help="Accepted ratio tolerance")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        original_words = count_words(args.original_file)
        summary_words = count_words(args.summary_file)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)

    if original_words == 0:
        print("Error: Original file is empty.")
        sys.exit(1)

    ratio = summary_words / original_words
    lower_bound = args.target_ratio - args.tolerance
    upper_bound = args.target_ratio + args.tolerance

    print(f"Original word count: {original_words}")
    print(f"Summary word count:  {summary_words}")
    print(f"Actual Ratio:        {ratio:.4f} ({ratio * 100:.2f}%)")
    print(
        "Target Ratio:        "
        f"{args.target_ratio:.2f} +- {args.tolerance:.2f} "
        f"({lower_bound * 100:.0f}% to {upper_bound * 100:.0f}%)"
    )

    if lower_bound <= ratio <= upper_bound:
        print("\nSUCCESS: Summary ratio is within the acceptable range.")
        sys.exit(0)

    print("\nFAILURE: Summary ratio is outside the acceptable range.")
    sys.exit(1)


if __name__ == "__main__":
    main()
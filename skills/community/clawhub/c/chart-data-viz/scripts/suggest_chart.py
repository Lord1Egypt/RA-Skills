#!/usr/bin/env python3
import argparse

def parse_csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Suggest best chart type")
    parser.add_argument("--labels", required=True, help="Comma-separated labels")
    parser.add_argument("--values", required=True, help="Comma-separated values")
    parser.add_argument("--x_numeric", action="store_true", help="Treat x-axis as numeric or ordered")
    args = parser.parse_args()

    labels = parse_csv(args.labels)
    values = parse_csv(args.values)

    if len(labels) != len(values):
        raise SystemExit("labels and values length mismatch")

    suggestion = "bar"
    reason = "Best for comparing categories clearly."

    if args.x_numeric:
        suggestion = "line"
        reason = "Best for trends or ordered progression."
    elif len(labels) <= 5:
        suggestion = "bar"
        reason = "Best for quick category comparison."
    elif len(labels) > 8:
        suggestion = "line"
        reason = "Many points usually read better as a trend line."

    print(f"Suggested chart: {suggestion}")
    print(f"Reason: {reason}")

if __name__ == "__main__":
    main()

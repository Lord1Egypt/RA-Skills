#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_charts, save_charts, OUTPUT_DIR

VALID_TYPES = ["bar", "line", "pie", "scatter"]

def parse_csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]

def parse_float_csv(value):
    return [float(v.strip()) for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Generate a chart")
    parser.add_argument("--type", choices=VALID_TYPES, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--x_values", help="For scatter only")
    args = parser.parse_args()

    labels = parse_csv(args.labels)
    values = parse_float_csv(args.values)

    if args.type != "scatter" and len(labels) != len(values):
        raise SystemExit("labels and values length mismatch")

    chart_id = f"CHT-{str(uuid.uuid4())[:4].upper()}"
    filename = f"{chart_id}.png"
    output_path = os.path.join(OUTPUT_DIR, filename)

    plt.figure(figsize=(8, 5))

    if args.type == "bar":
        plt.bar(labels, values)
        plt.ylabel("Value")

    elif args.type == "line":
        plt.plot(labels, values, marker="o")
        plt.ylabel("Value")

    elif args.type == "pie":
        plt.pie(values, labels=labels, autopct="%1.1f%%")

    elif args.type == "scatter":
        if not args.x_values:
            raise SystemExit("--x_values is required for scatter")
        x_values = parse_float_csv(args.x_values)
        if len(x_values) != len(values):
            raise SystemExit("x_values and values length mismatch")
        plt.scatter(x_values, values)
        plt.xlabel("X")
        plt.ylabel("Y")

    plt.title(args.title)
    if args.type != "pie":
        plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    data = load_charts()
    data["charts"][chart_id] = {
        "id": chart_id,
        "title": args.title,
        "type": args.type,
        "labels": labels,
        "values": values,
        "output_path": output_path,
        "created_at": datetime.now().isoformat()
    }
    save_charts(data)

    print(f"✓ Chart created: {chart_id}")
    print(f"  Title: {args.title}")
    print(f"  Type: {args.type}")
    print(f"  Output: {output_path}")

if __name__ == "__main__":
    main()

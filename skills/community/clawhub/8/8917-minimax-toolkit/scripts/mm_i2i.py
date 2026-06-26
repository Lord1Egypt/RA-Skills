#!/usr/bin/env python3
import sys
import argparse
from minimax_client import MinimaxClient
from executor_common import execute_i2i


def main():
    parser = argparse.ArgumentParser(description="Generate image from reference image (I2I) using MiniMax")
    parser.add_argument("prompt", help="Text prompt describing the desired output style")
    parser.add_argument("--ref", required=True, help="Path to reference image")
    parser.add_argument("--model", default="image-01", choices=["image-01", "image-01-live"], help="Model name")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    client = MinimaxClient()
    result = execute_i2i(client, args.prompt, args.model, args.project, args.output_dir, args.estimate, {
        "ref": args.ref,
        "ratio": args.ratio,
    })
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("filepath"):
        print(f"MEDIA:{result['filepath']}")


if __name__ == "__main__":
    main()

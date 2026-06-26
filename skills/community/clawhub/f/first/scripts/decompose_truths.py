#!/usr/bin/env python3
import argparse
import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.reasoning import infer_truths, infer_components, infer_constraints

def main():
    parser = argparse.ArgumentParser(description="Decompose a problem into truths, components, and constraints")
    parser.add_argument("--text", required=True, help="Problem text")
    args = parser.parse_args()

    result = {
        "truths": infer_truths(args.text),
        "components": infer_components(args.text),
        "constraints": infer_constraints(args.text)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

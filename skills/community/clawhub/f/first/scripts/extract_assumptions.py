#!/usr/bin/env python3
import argparse
import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.reasoning import infer_assumptions

def main():
    parser = argparse.ArgumentParser(description="Extract assumptions from a problem statement")
    parser.add_argument("--text", required=True, help="Problem text")
    args = parser.parse_args()
    print(json.dumps({"assumptions": infer_assumptions(args.text)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.reasoning import infer_goal, infer_rebuilt_solution, infer_next_actions

def main():
    parser = argparse.ArgumentParser(description="Rebuild a solution from first principles")
    parser.add_argument("--text", required=True, help="Problem text")
    args = parser.parse_args()

    result = {
        "goal": infer_goal(args.text),
        "rebuilt_solution": infer_rebuilt_solution(args.text),
        "next_actions": infer_next_actions(args.text)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

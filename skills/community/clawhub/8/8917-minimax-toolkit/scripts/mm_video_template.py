#!/usr/bin/env python3
import sys
import argparse
from minimax_client import MinimaxClient
from executor_common import execute_video_template


def main():
    parser = argparse.ArgumentParser(description="Generate video using MiniMax Video Agent templates")
    parser.add_argument("template", help="Template name")
    parser.add_argument("--media", help="Path to input image file")
    parser.add_argument("--text", help="Text input for templates that need text")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    client = MinimaxClient()
    result = execute_video_template(client, args.template, None, args.project, args.output_dir, args.estimate, {
        "template": args.template,
        "media": args.media,
        "text": args.text,
    })
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("task_id"):
        print(f"Task created! ID: {result['task_id']}")
        if result.get("suggested_path"):
            print(f"Suggested output: {result['suggested_path']}")


if __name__ == "__main__":
    main()

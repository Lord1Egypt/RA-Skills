#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from typing import Dict, List


def main() -> None:
    try:
        args = parse_cli_args(sys.argv[1:])
        artifact_path = args.get("--artifact", "output/aicade-galaxy-skill.json")
        artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))

        tools = artifact.get("tools")
        if not isinstance(tools, list):
            raise RuntimeError("Invalid artifact format.")

        summary = {
            "baseUrl": artifact.get("baseUrl"),
            "toolCount": artifact.get("toolCount"),
            "tools": [
                {
                    "name": tool.get("name"),
                    "title": tool.get("metadata", {}).get("title", ""),
                    "method": tool.get("metadata", {}).get("method", ""),
                    "path": tool.get("metadata", {}).get("path", ""),
                    "required": tool.get("inputSchema", {}).get("required", []),
                    "responseFields": tool.get("metadata", {}).get(
                        "responseFields", []
                    ),
                }
                for tool in tools
                if isinstance(tool, dict)
            ],
        }

        print(json.dumps(summary, ensure_ascii=False, indent=2))
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def parse_cli_args(argv: List[str]) -> Dict[str, str]:
    if len(argv) % 2 != 0:
        raise RuntimeError("Usage: python3 scripts/list_tools.py --artifact <path>")

    result: Dict[str, str] = {}
    for index in range(0, len(argv), 2):
        key = argv[index]
        value = argv[index + 1]
        if not key.startswith("--"):
            raise RuntimeError(
                "Usage: python3 scripts/list_tools.py --artifact <path>"
            )
        result[key] = value
    return result


if __name__ == "__main__":
    main()

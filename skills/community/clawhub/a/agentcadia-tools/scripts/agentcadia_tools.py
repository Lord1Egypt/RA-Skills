#!/usr/bin/env python3
import pathlib
import runpy
import sys


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"upload", "download"}:
        print(
            "Usage: python3 scripts/agentcadia_tools.py <upload|download> [args...]",
            file=sys.stderr,
        )
        sys.exit(2)

    command = sys.argv[1]
    script_dir = pathlib.Path(__file__).resolve().parent
    target = script_dir / ("upload_agentcadia.py" if command == "upload" else "download_agentcadia.py")
    sys.argv = [str(target), *sys.argv[2:]]
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()

import argparse
import json

from guardlib import path_findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--allowed-root", action="append", dest="allowed_roots")
    args = parser.parse_args()
    print(json.dumps(path_findings(args.command, args.cwd, args.allowed_roots or []), indent=2))


if __name__ == "__main__":
    main()

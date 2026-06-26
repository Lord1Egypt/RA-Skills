import argparse
import json

from guardlib import rollback_hints


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    args = parser.parse_args()
    print(json.dumps({"rollback": rollback_hints(args.command)}, indent=2))


if __name__ == "__main__":
    main()

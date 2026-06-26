import argparse
import json

from guardlib import find_secret_findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    args = parser.parse_args()
    print(json.dumps(find_secret_findings(args.command), indent=2))


if __name__ == "__main__":
    main()

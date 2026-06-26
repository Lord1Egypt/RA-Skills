import argparse
import json

from guardlib import classify_command


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    args = parser.parse_args()
    print(json.dumps(classify_command(args.command), indent=2))


if __name__ == "__main__":
    main()

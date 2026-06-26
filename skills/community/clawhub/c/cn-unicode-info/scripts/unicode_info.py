#!/usr/bin/env python3

import argparse, json, sys, unicodedata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    result = []
    for ch in args.text:
        result.append({
            "char": ch,
            "codepoint": hex(ord(ch)),
            "name": unicodedata.name(ch, "UNKNOWN"),
            "category": unicodedata.category(ch),
        })
    print(json.dumps({"chars": result, "length": len(result)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

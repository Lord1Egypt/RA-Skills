#!/usr/bin/env python3

import argparse, json, sys

def detect_bom(data):
    if data.startswith(b"\xef\xbb\xbf"): return "UTF-8-BOM"
    if data.startswith(b"\xff\xfe"): return "UTF-16-LE"
    if data.startswith(b"\xfe\xff"): return "UTF-16-BE"
    return None

def detect_encoding(filepath):
    with open(filepath, "rb") as f:
        data = f.read(10000)
    
    bom = detect_bom(data)
    if bom:
        return bom
    
    # Try UTF-8
    try:
        data.decode("utf-8")
        return "UTF-8"
    except:
        pass
    
    # Try GBK
    try:
        data.decode("gbk")
        return "GBK"
    except:
        pass
    
    return "UNKNOWN"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    enc = detect_encoding(args.file)
    with open(args.file, "rb") as f:
        size = len(f.read())
    print(json.dumps({"file": args.file, "encoding": enc, "size_bytes": size}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

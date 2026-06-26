#!/usr/bin/env python3

import argparse, json, sys

def diff_json(j1, j2, path=""):
    diffs = []
    if type(j1) != type(j2):
        return [f"{path}: type changed {type(j1).__name__} -> {type(j2).__name__}"]
    if isinstance(j1, dict):
        for k in set(list(j1.keys()) + list(j2.keys())):
            p = f"{path}.{k}" if path else k
            if k not in j1:
                diffs.append(f"{p}: + added")
            elif k not in j2:
                diffs.append(f"{p}: - removed")
            else:
                diffs.extend(diff_json(j1[k], j2[k], p))
    elif isinstance(j1, list):
        if j1 != j2:
            diffs.append(f"{path}: list differs (len {len(j1)} vs {len(j2)})")
    else:
        if j1 != j2:
            diffs.append(f"{path}: {j1} -> {j2}")
    return diffs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file1", required=True)
    parser.add_argument("--file2", required=True)
    args = parser.parse_args()
    with open(args.file1) as f1, open(args.file2) as f2:
        d1, d2 = json.load(f1), json.load(f2)
    diffs = diff_json(d1, d2)
    print(json.dumps({"differences": diffs, "count": len(diffs)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

"""Deduplicate event records while preserving first-seen order."""
import json, sys


def dedupe(events):
    out = []
    for e in events:
        if e not in out:  # O(n^2)
            out.append(e)
    return out


def load(path):
    with open(path) as f:
        return [json.loads(line) for line in f]


if __name__ == "__main__":
    evs = load(sys.argv[1])
    res = dedupe(evs)
    print(len(res))

#!/usr/bin/env python3
"""Compare a plaintext tree against the manifest's checksums map.

verify_tree.py MANIFEST.json ROOT

Two moments to run it: on the staging tree just before `envrelay encrypt`
(does the manifest describe what is actually on disk?) and on the decrypt
output just after a restore (did everything land intact?). The archive
itself needs neither — the age MAC already proves every byte — which is why
this check lives out here, on plaintext, with no passphrase involved.

Output is one JSON object: `matched`, `mismatched`, `missing`, and
`unclaimed_files` (regular files under ROOT that no checksum covers —
`manifest.json` itself and `ledger.json` excepted). The exit code is about
whether the comparison ran, not what it found; read the JSON.
"""

import argparse
import hashlib
import json
import os
import sys

CHUNK = 1024 * 1024
UNCLAIMED_SAMPLE = 20
EXPECTED_UNCLAIMED = {"manifest.json", "ledger.json"}


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", help="manifest.json with a checksums map")
    parser.add_argument("root", help="tree to verify (staging dir or decrypt output)")
    args = parser.parse_args()

    try:
        with open(args.manifest, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError) as error:
        print(f"verify_tree: cannot read manifest {args.manifest}: {error}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.root):
        print(f"verify_tree: {args.root} is not a directory", file=sys.stderr)
        sys.exit(1)

    checksums = manifest.get("checksums") or {}
    result = {"checked": len(checksums), "matched": 0, "mismatched": [], "missing": []}
    if not checksums:
        result["note"] = "the manifest has no checksums map; nothing to verify"

    # The manifest crossed a machine boundary: a checksums key is untrusted
    # input, and hashing wherever it points would turn this script into a
    # file-existence and content-confirmation oracle over the whole machine.
    # Refuse anything that is not a plain relative path resolving inside ROOT.
    root_real = os.path.realpath(args.root)
    for rel in sorted(checksums):
        if os.path.isabs(rel) or ".." in rel.split("/"):
            result["mismatched"].append({"path": rel, "reason": "path escapes the root; refused"})
            continue
        path = os.path.join(args.root, rel)
        if os.path.islink(path):
            result["mismatched"].append({"path": rel, "reason": "is a symlink; refused to follow"})
            continue
        real = os.path.realpath(path)
        if real != root_real and not real.startswith(root_real + os.sep):
            result["mismatched"].append(
                {"path": rel, "reason": "resolves outside the root; refused"}
            )
            continue
        try:
            actual = sha256_of(path)
        except FileNotFoundError:
            result["missing"].append(rel)
            continue
        except OSError as error:
            result["mismatched"].append({"path": rel, "reason": error.strerror or str(error)})
            continue
        if actual == checksums[rel]:
            result["matched"] += 1
        else:
            result["mismatched"].append({"path": rel, "reason": "checksum differs"})

    unclaimed = []
    root = os.path.abspath(args.root)
    for dirpath, _dirnames, filenames in os.walk(root, followlinks=False):
        for name in filenames:
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                continue
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if rel not in checksums and rel not in EXPECTED_UNCLAIMED:
                unclaimed.append(rel)
    unclaimed.sort()
    result["unclaimed_files"] = {
        "count": len(unclaimed),
        "sample": unclaimed[:UNCLAIMED_SAMPLE],
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()

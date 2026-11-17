#!/usr/bin/env bash
# Generates a small synthetic tree used by the DirStat_Skill demo.
# The generated files are gitignored; only this script and the produced
# examples/demo-audit bundle are committed.
#
# The tree is deliberately shaped to surface the two "redundancy" advices:
#   - a duplicated large asset (same name+size in two directories)
#   - an incomplete download (.part) that dominates its directory
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

rm -rf sample-data
mkdir -p sample-data/models sample-data/backup/models sample-data/downloads

head -c 100000 /dev/urandom > sample-data/models/model.gguf
head -c 100000 /dev/urandom > sample-data/backup/models/model.gguf
head -c 900000 /dev/urandom > sample-data/downloads/pack.bin.part

echo "sample-data created under $(pwd)/sample-data"

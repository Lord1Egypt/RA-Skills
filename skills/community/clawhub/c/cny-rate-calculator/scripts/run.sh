#!/bin/bash
cd "$(dirname "$0")/.."
python3 scripts/cny_rate.py "$@"

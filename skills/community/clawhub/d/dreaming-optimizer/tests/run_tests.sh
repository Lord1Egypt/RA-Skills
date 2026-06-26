#!/usr/bin/env bash
# run_tests.sh — run the dreaming-optimizer test suite
set -euo pipefail
cd "$(dirname "$0")/.."
pytest tests/ -v --tb=short

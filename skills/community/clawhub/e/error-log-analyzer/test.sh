#!/bin/bash
# Quick test runner for Error Log Analyzer

cd "$(dirname "$0")"

case "$1" in
  "benchmark"|"b")
    ./venv/bin/python run_tests.py benchmark
    ;;
  "test"|"t")
    ./venv/bin/python run_tests.py test
    ;;
  "all"|"a")
    ./venv/bin/python run_tests.py all
    ;;
  "feedback"|"f")
    ./venv/bin/python run_tests.py feedback
    ;;
  *)
    echo "Usage: $0 {benchmark|test|all|feedback}"
    echo "  benchmark (b) - Run accuracy benchmark"
    echo "  test (t)      - Run unit tests"
    echo "  all (a)       - Run all tests"
    echo "  feedback (f)  - Show feedback stats"
    exit 1
    ;;
esac

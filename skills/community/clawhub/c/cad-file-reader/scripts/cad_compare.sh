#!/usr/bin/env bash
# P5 图纸对比候选入口。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_compare "$@"

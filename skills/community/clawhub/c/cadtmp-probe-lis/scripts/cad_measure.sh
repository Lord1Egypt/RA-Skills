#!/usr/bin/env bash
# 测量候选层：把 cad_scan / descriptive / mep / steel / municipal JSON 转成可追溯的长度、面积、体积候选。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_measure "$@"

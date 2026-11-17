#!/usr/bin/env bash
# 装饰识图中间数据：需要 cad_scan --detail-json 的输出。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_descriptive_geometry "$@"

#!/usr/bin/env bash
# 钢结构识图中间数据：需要 cad_scan --with-geom --with-geom-layer 的输出。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_steel_geometry "$@"

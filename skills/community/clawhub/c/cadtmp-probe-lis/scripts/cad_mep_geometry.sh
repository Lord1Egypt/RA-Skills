#!/usr/bin/env bash
# 安装专业识图中间数据：需要 cad_scan --with-geom --with-geom-layer 的输出。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_mep_geometry "$@"

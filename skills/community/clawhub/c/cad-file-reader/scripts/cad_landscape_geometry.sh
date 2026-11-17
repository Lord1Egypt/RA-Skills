#!/usr/bin/env bash
# 园林/景观识图中间数据：需要 cad_scan --with-geom --with-geom-layer 的输出（有图层原图效果最佳）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_landscape_geometry "$@"

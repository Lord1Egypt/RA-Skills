#!/usr/bin/env bash
# 设计院图例校准：扫出新设计院图中未匹配的块名并建议 plant_block_aliases。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_landscape_calibrate "$@"

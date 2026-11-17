#!/usr/bin/env bash
# 全量读取：实体树统计 / SVG 渲染 / 转 DXF 回退。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" read_cad "$@"

#!/usr/bin/env bash
# 按目录批量扫图，输出识图台账（Excel + 自检汇总.md）。
# 用法: scripts/cad_batch.sh 输入文件或目录 --out 输出目录 [--glob '*.dwg;*.dxf'] [--resume] ...
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_batch "$@"

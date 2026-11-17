#!/usr/bin/env bash
# 本机真实 DWG 回归：需要 --manifest <本地真图清单>（脱敏，含 id/name/path/expect）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" run_real_dwg_regression "$@"

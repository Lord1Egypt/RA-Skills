#!/usr/bin/env bash
# 矢量 PDF 原生文字坐标提取（供 PDF 识图分流复核）。
# 跨平台：统一交给 run_cad.py 分发，由其自举解释器并在 Windows/Linux 上
# 用 platform_paths 找到 pdf-inspector venv（Windows 是 Scripts/python.exe）。
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_pdf_vec "$@"

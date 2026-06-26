#!/usr/bin/env bash
# 合并桌面上的多个 PDF 为一个文件（PPT skill 配套：生成多份 PDF 后合并）
# Usage:
#   bash merge_pdf_on_desktop.sh [输出文件名.pdf] [PDF1.pdf PDF2.pdf ...]
#   bash merge_pdf_on_desktop.sh merged.pdf           # 合并 Desktop 下所有 PDF（按修改时间排序）
#   bash merge_pdf_on_desktop.sh merged.pdf a.pdf b.pdf  # 只合并指定文件（顺序即合并顺序）
# 输出默认在 ~/Desktop/

set -e
DESKTOP="${DESKTOP:-$HOME/Desktop}"
OUTPUT_NAME="${1:-merged_$(date +%Y%m%d_%H%M).pdf}"
shift || true

# 收集要合并的 PDF 列表
PDFS=()
if [ $# -eq 0 ]; then
  # 无额外参数：合并桌面所有 PDF（按文件名排序）
  while IFS= read -r f; do PDFS+=("$f"); done < <(find "$DESKTOP" -maxdepth 1 -name "*.pdf" -type f 2>/dev/null | sort)
else
  # 有参数：按参数顺序合并（可带路径或仅文件名，在 Desktop 下找）
  PDFS=()
  for f in "$@"; do
    if [ -f "$f" ]; then
      PDFS+=("$f")
    elif [ -f "$DESKTOP/$f" ]; then
      PDFS+=("$DESKTOP/$f")
    else
      echo "WARNING: not found: $f"
    fi
  done
fi

if [ ${#PDFS[@]} -eq 0 ]; then
  echo "No PDF files to merge on Desktop."
  exit 1
fi

if [ ${#PDFS[@]} -eq 1 ]; then
  echo "Only one PDF, copying to $OUTPUT_NAME"
  cp "${PDFS[0]}" "$DESKTOP/$OUTPUT_NAME"
  echo "Done: $DESKTOP/$OUTPUT_NAME"
  exit 0
fi

OUTPUT_PATH="$DESKTOP/$OUTPUT_NAME"
echo "Merging ${#PDFS[@]} PDFs -> $OUTPUT_PATH"

# 优先用 qpdf（brew install qpdf）
if command -v qpdf >/dev/null 2>&1; then
  qpdf --empty --pages "${PDFS[@]}" -- "$OUTPUT_PATH"
  echo "Done (qpdf): $OUTPUT_PATH"
  exit 0
fi

# 其次用 gs
if command -v gs >/dev/null 2>&1; then
  gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="$OUTPUT_PATH" "${PDFS[@]}"
  echo "Done (gs): $OUTPUT_PATH"
  exit 0
fi

# 再用 Python pypdf（pip install pypdf）
if python3 -c "import pypdf" 2>/dev/null; then
  python3 - "$OUTPUT_PATH" "${PDFS[@]}" << 'PY'
import sys
from pypdf import PdfMerger
out = sys.argv[1]
paths = sys.argv[2:]
m = PdfMerger()
for p in paths:
    m.append(p)
m.write(out)
m.close()
print("Done (pypdf):", out)
PY
  exit 0
fi

# 最后尝试 pdfunite（poppler）
if command -v pdfunite >/dev/null 2>&1; then
  pdfunite "${PDFS[@]}" "$OUTPUT_PATH"
  echo "Done (pdfunite): $OUTPUT_PATH"
  exit 0
fi

echo "No PDF merger found. Install one of: qpdf (brew install qpdf), gs (brew install gs), or pip install pypdf"
exit 1

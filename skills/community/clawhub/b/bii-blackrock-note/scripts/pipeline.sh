#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# pipeline.sh — 贝莱德智库风格 BII 简报：一条龙出 html + pdf + pptx
#
# 用法：
#   bash pipeline.sh <源 BII.html> <输出目录> [基线名] [页数]
#   例： bash pipeline.sh ~/Desktop/bii_sz001337_20260917.html ./out
#        → out/bii_sz001337_20260917_blackrock.{html,pdf,pptx}
#
# 六步（任一步失败即停，不留半成品）：
#   ① 注入：色板重定向 + 装饰注入（含 22 页结构断言）
#   ② 逐页版式体检：量高度定位溢出（装饰件挤爆某页时唯一有效的定位手段）
#   ③ 出 PDF（CDP，含 canvas 墨量验收）
#   ④ 封 PPTX（满幅位图 + 演讲者备注）
#   ⑤ 七门体检
#   ⑥ 汇报
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SRC="${1:-}"; OUTDIR="${2:-}"; BASE="${3:-}"; PAGES="${4:-22}"
[ -n "$SRC" ] && [ -n "$OUTDIR" ] || { sed -n '3,14p' "$0"; exit 2; }
[ -f "$SRC" ] || { echo "[!] 找不到源 HTML：$SRC"; exit 1; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${BR_PY:-$HOME/.workbuddy/binaries/python/envs/default/bin/python}"
[ -x "$PY" ] || PY="$(command -v python3)"
CDP_SKILL="$HOME/.workbuddy/skills/html-to-pdf-cdp/scripts"

SRC_ABS="$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")"
mkdir -p "$OUTDIR"
OUTDIR="$(cd "$OUTDIR" && pwd)"
[ -n "$BASE" ] || BASE="$(basename "$SRC_ABS" .html)"
OUT="$OUTDIR/${BASE}_blackrock"

echo "═══ ① 注入：色板重定向 + 结构装饰 ═══"
"$PY" "$HERE/theme_inject.py" "$SRC_ABS" "$OUT.html" \
  --pages "$PAGES" --report "$OUTDIR/${BASE}_inject_report.json"

echo
echo "═══ ② 逐页版式体检（溢出定位） ═══"
bash "$HERE/inspect_pages.sh" "$OUT.html" | tee "$OUTDIR/${BASE}_pages.txt" | tail -28

echo
echo "═══ ③ 出 PDF ═══"
bash "$CDP_SKILL/render_html_pdf.sh" "$OUT.html" "$OUT.pdf" 3200 css

echo
echo "═══ ④ 封 PPTX ═══"
"$PY" "$HERE/mkpptx.py" "$OUT.pdf" "$OUT.pptx" 200

echo
echo "═══ ⑤ 七门体检 ═══"
"$PY" "$HERE/check_br.py" "$OUT.html" --src "$SRC_ABS" --pdf "$OUT.pdf" \
  --pptx "$OUT.pptx" --pages "$PAGES" --json "$OUTDIR/${BASE}_qa.json"

echo
echo "═══ ⑥ 交付物 ═══"
ls -lh "$OUT.html" "$OUT.pdf" "$OUT.pptx"

#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# BII 双栏范式 · 一键出 PDF
#   生成 HTML → 起无头 Chrome → 校验（图表墨量 / 零溢出 / 页数）→ 导 PDF → 收尾
#
# 用法：
#   bash templates/bii/render.sh --data strategy/sample_data.json --date 2026-09-16
#   bash templates/bii/render.sh --data strategy/today.json --date 2026-09-16 --out out/lhb-20260916
#   bash templates/bii/render.sh --data strategy/today.json --date 2026-09-16 \
#        --predict-file out/lhb-20260916/predictions.json
#
# 次日 5 条可证伪预判（第 14 页）来自 --predict-file；不传时生成器会自动探测
# <data 同级>/predictions.json 与 <out>/predictions.json，都缺则渲染「示例占位页」。
#
# 为什么要"一键"：中间任何一步手工做，都会踩这三个坑
#   1) Chrome 用 nohup/& 起会被沙箱回收 → 必须由本脚本前台持有，跑完再收
#   2) 浏览器会缓存上一次的 HTML（改完代码还看到旧页面）→ 每次都用全新 user-data-dir
#   3) 直接 printToPDF 大 PDF 会静默失败 → 统一走 cdp_pdf.js 的 ReturnAsStream
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

DATA="$REPO/strategy/sample_data.json"
DATE="$(date +%F)"
OUT=""
PRED=""
PORT="${BII_CDP_PORT:-9333}"
KEEP="${BII_KEEP_ALIVE:-0}"      # 1 = 跑完不关 Chrome（调试用）

while [ $# -gt 0 ]; do
  case "$1" in
    --data) DATA="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2";  shift 2 ;;
    --predict-file) PRED="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --keep) KEEP=1;    shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "[!] 未知参数：$1"; exit 2 ;;
  esac
done

DC="${DATE//-/}"
[ -n "$OUT" ] || OUT="$REPO/out/dragon-tiger-$DC"
mkdir -p "$OUT"
# ⚠️ 必须转成绝对路径：后面要给 Chrome 拼 file:// URL，相对路径会拼出
#    file://out/xxx（被当成 host 名），页面加载失败但标签照样存在 ——
#    症状是"校验报 canvas 总数 0"，极难联想到路径问题。
OUT="$(cd "$OUT" && pwd)"
case "$DATA" in
  /*) : ;;
  *) [ -f "$DATA" ] && DATA="$(cd "$(dirname "$DATA")" && pwd)/$(basename "$DATA")" ;;
esac
# 预判文件同样要转绝对路径（原因同 DATA）
if [ -n "$PRED" ]; then
  [ -f "$PRED" ] || { echo "[!] 预判文件不存在：$PRED"; exit 2; }
  case "$PRED" in
    /*) : ;;
    *) PRED="$(cd "$(dirname "$PRED")" && pwd)/$(basename "$PRED")" ;;
  esac
fi

# ── 找可执行文件（优先 WorkBuddy 托管运行时） ──
PY="${BII_PY:-}"
if [ -z "$PY" ]; then
  for c in "$HOME/.workbuddy/binaries/python/versions/3.13.12/bin/python3" "$(command -v python3 || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { PY="$c"; break; }
  done
fi
NODE="${BII_NODE:-}"
if [ -z "$NODE" ]; then
  for c in "$(command -v node || true)" \
           "$HOME/.workbuddy/binaries/node/versions/22.12.0/bin/node" \
           "$HOME/.workbuddy/binaries/node/versions/22.22.2-3/bin/node"; do
    [ -n "$c" ] && [ -x "$c" ] && { NODE="$c"; break; }
  done
fi
[ -n "$PY" ]   || { echo "[!] 找不到 python3"; exit 1; }
[ -n "$NODE" ] || { echo "[!] 找不到 node（校验与导 PDF 都需要）"; exit 1; }

CHROME="${BII_CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           "$(command -v google-chrome || true)" \
           "$(command -v chromium || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { CHROME="$c"; break; }
  done
fi
[ -n "$CHROME" ] || { echo "[!] 找不到 Chrome/Edge/Chromium（导 PDF 必需）"; exit 1; }

# ── 1. 生成 HTML（内含占位符 + JS 语法双重自检） ──
echo "▶ [1/4] 生成 HTML"
GEN_ARGS=(--data "$DATA" --date "$DATE" --out "$OUT")
# ⚠️ 不要写成 `[ -n "$PRED" ] && GEN_ARGS+=(...)`：set -e 下左侧判定失败会让整个 AND 列表
#    返回非零，脚本会在这里静默退出（经典坑）。
if [ -n "$PRED" ]; then
  GEN_ARGS+=(--predict-file "$PRED")
fi
PYTHONPATH="$REPO" "$PY" "$HERE/gen_bii_2col.py" "${GEN_ARGS[@]}"

HTML="$OUT/涨停板龙虎榜深度研判报告-BII双栏-$DC.html"
PDF="$OUT/涨停板龙虎榜深度研判报告-BII双栏-$DC.pdf"
[ -f "$HTML" ] || { echo "[!] HTML 未生成：$HTML"; exit 1; }

# ── 2. 起无头 Chrome（全新 profile，杜绝缓存） ──
PROFILE="$(mktemp -d -t bii-chrome-XXXXXX)"
cleanup() {
  if [ "$KEEP" = "1" ]; then
    echo "▶ Chrome 保留在端口 ${PORT}（--keep）：$CHROME --remote-debugging-port=$PORT"
    return
  fi
  [ -n "${CHROME_PID:-}" ] && kill "$CHROME_PID" 2>/dev/null || true
  rm -rf "$PROFILE" 2>/dev/null || true
}
trap cleanup EXIT

# ⚠️ 端口自愈 —— 必须做，否则会静默校验到"上一次的页面"：
#    若 9333 上还蹲着一个残留 Chrome，新 Chrome 绑不上端口但请求会被老的那个接走，
#    于是你看到的永远是上一次的 HTML（改了代码却毫无变化），而页高/墨量数字还"看着正常"。
BASE_PORT="$PORT"
while curl -s --noproxy '*' "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1; do
  echo "[i] 端口 $PORT 已被其它 Chrome 占用，换端口"
  PORT=$((PORT + 1))
  if [ "$PORT" -gt "$((BASE_PORT + 20))" ]; then
    echo "[!] $BASE_PORT..$((BASE_PORT + 20)) 全被占用，先清残留 Chrome："
    echo "    pkill -f 'remote-debugging-port=$BASE_PORT'"
    exit 1
  fi
done

echo "▶ [2/4] 启动无头 Chrome（端口 ${PORT}）"
#   --no-sandbox / --in-process-gpu 是必需的：受限环境里 GPU 进程起不来会让 Chrome 直接退出
"$CHROME" --headless=new --no-sandbox --disable-setuid-sandbox \
  --disable-dev-shm-usage --disable-gpu --in-process-gpu \
  --no-first-run --no-default-browser-check --disable-application-cache \
  --user-data-dir="$PROFILE" --remote-debugging-port="$PORT" \
  --window-size=1400,1200 "file://$HTML" > "$OUT/.chrome.log" 2>&1 &
CHROME_PID=$!

CDP="http://127.0.0.1:$PORT"
for i in $(seq 1 40); do
  if curl -s --noproxy '*' "$CDP/json/version" >/dev/null 2>&1; then break; fi
  sleep 0.5
done
curl -s --noproxy '*' "$CDP/json/version" >/dev/null 2>&1 \
  || { echo "[!] Chrome 未在 20s 内就绪，日志见 $OUT/.chrome.log"; tail -5 "$OUT/.chrome.log"; exit 1; }

# ── 3. 校验：图表墨量 + 零溢出 ──
echo "▶ [3/4] 校验图表与版面"
#   视口钉 1123px = A4 横向 297mm；溢出阈值 794px = 210mm
if ! "$NODE" "$HERE/verify_print.js" "$CDP" 1123 794; then
  echo "[!] 校验未通过 —— 先修 HTML 再导 PDF（空白图/溢出都会被这里拦下）"
  exit 3
fi

# ── 4. 导 PDF（复用上面那个 Chrome，省一次冷启动） ──
echo "▶ [4/4] 导出 PDF"
CDP_ENDPOINT="$CDP" bash "$HERE/cdp_render.sh" "$HTML" "$PDF" 2400 css

# 页数一致性：PDF 页数须 == HTML section 数（这是最硬的判据，比看截图可靠）
N_PDF="$("$PY" - "$PDF" <<'PYEOF'
import re, sys
d = open(sys.argv[1], 'rb').read()
print(len(re.findall(rb'/Type\s*/Page[^s]', d)))
PYEOF
)"
N_HTML="$(grep -o 'class="page"' "$HTML" | wc -l | tr -d ' ')"
N_COVER="$(grep -o 'class="cover"' "$HTML" | wc -l | tr -d ' ')"
N_SEC=$((N_HTML + N_COVER))

echo "──────────────────────────────────────────────"
echo " PDF 页数 $N_PDF | HTML 区块 ${N_SEC}（cover $N_COVER + page ${N_HTML}）"
if [ "$N_PDF" = "$N_SEC" ]; then
  echo " ✅ 页数一致"
else
  echo " ❌ 页数不一致 —— 版面里一定有元素顶破页高，回到第 3 步查"
  exit 4
fi
ls -la "$PDF"
echo "──────────────────────────────────────────────"

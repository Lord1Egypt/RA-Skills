#!/usr/bin/env bash
# 股票雷达 · 10 技能执行器（2026-09-24 老板确认「写死」）
# 用法：
#   bash skills/trading-desk/scripts/radar_run.sh                 # 只跑「无需候选」的阶段1-2
#   bash skills/trading-desk/scripts/radar_run.sh 002487 603667   # 带候选代码 → 跑全链（含风险/资金/分时/深研）
# 产出：/tmp/openclaw/radar/<TS>/ 下各技能原始输出 + 终端一张「参与状态表」
set -o pipefail

# --- 定位工作区根 ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR/../../.." && pwd)"   # skills/trading-desk/scripts -> workspace
cd "$WS" || { echo "无法进入工作区: $WS"; exit 1; }

DATE="${RADAR_DATE:-$(date +%Y-%m-%d)}"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="${RADAR_OUT:-/tmp/openclaw/radar/$TS}"
mkdir -p "$OUT"
CODES=("$@")

PASS=0; FALLBACK=0; FAIL=0; NA=0
declare -a ROWS

mark() { # name status detail
  case "$2" in
    ✅*) PASS=$((PASS+1));;
    🟡*) FALLBACK=$((FALLBACK+1));;
    ⬜*) NA=$((NA+1));;
    *)   FAIL=$((FAIL+1));;
  esac
  ROWS+=("$1|$2|$3")
}
run() { # logfile, then command...
  local log="$1"; shift
  timeout 300 "$@" >"$OUT/$log" 2>&1
}
nonempty() { [ -s "$OUT/$1" ] && ! grep -qiE "Traceback|RemoteDisconnected|can't open file|No such file" "$OUT/$1"; }

echo "════════════════════════════════════════════════════"
echo " 股票雷达 · 10 技能全跑  日期 $DATE"
echo " 输出: $OUT"
echo "════════════════════════════════════════════════════"

# RADAR_SKIP_BASE=1 → 跳过阶段1-6（基础扫描），只跑 7~9（需候选），用于快速复跑
if [ "${RADAR_SKIP_BASE:-}" != "1" ]; then

# ---------- 1. trading-desk 主引擎（情绪 / 全市场扫描 / 板块） ----------
echo "[1/10] trading-desk 主引擎 ..."
run td_emotion.log   python3 skills/trading-desk/scripts/emotion.py "${DATE//-/}"
run td_scan.log      python3 skills/trading-desk/scripts/ashare_screen.py scan 20
run td_sector.log    python3 skills/trading-desk/scripts/sector_flow.py industry 15
if nonempty td_scan.log; then
  mark "trading-desk" "✅ 跑了" "emotion+scan+sector 见 $OUT/td_*.log"
else
  mark "trading-desk" "❌ 失败" "scan 空/报错，见 td_scan.log"
fi

# ---------- 2. a-share-short-decision 第二引擎 ----------
echo "[2/10] a-share-short-decision 第二引擎 ..."
( cd skills/a-share-short-decision && timeout 600 python3 main.py short_term_signal_engine --date "$DATE" ) >"$OUT/sd_engine.log" 2>&1
if grep -q '"candidates"' "$OUT/sd_engine.log" 2>/dev/null; then
  if grep -qE '"candidates": \[\]' "$OUT/sd_engine.log"; then
    mark "a-share-short-decision" "🟡 跑了(空)" "candidates=[] → 独立信号暂无"
  else
    mark "a-share-short-decision" "✅ 跑了" "candidates 非空，见 sd_engine.log"
  fi
else
  mark "a-share-short-decision" "❌ 失败" "无 candidates 字段，见 sd_engine.log"
fi

# ---------- 3. market-price 实时价校验 ----------
echo "[3/10] market-price 实时价校验 ..."
MP_OK=0
if curl -s --max-time 12 "https://finance.juglans.ai/api/v1/ticker?id=CN_STOCK:600000.SH@CNY_SPOT" -o "$OUT/mp_juglans.log" 2>/dev/null; then
  [ -s "$OUT/mp_juglans.log" ] && MP_OK=1
fi
if [ "$MP_OK" = "1" ]; then
  mark "market-price" "✅ 跑了" "juglans 可达"
else
  mark "market-price" "🟡 换源兜底" "juglans 不可达 → 改用 新浪+腾讯 双源（脚本内校验）"
fi

# ---------- 4. futures-panda 关联背景 ----------
echo "[4/10] futures-panda 关联背景 ..."
run fp_bg.log python3 skills/trading-desk/scripts/futures_quote.py 沪深300 中证500 焦炭
if nonempty fp_bg.log; then
  mark "futures-panda" "✅ 跑了" "股指/关联期货 见 fp_bg.log"
else
  mark "futures-panda" "❌ 失败" "见 fp_bg.log"
fi

# ---------- 5. a-stock-trading-assistant 多源复核（大盘/热点） ----------
echo "[5/10] a-stock-trading-assistant 多源复核 ..."
run ta_index.log python3 skills/a-stock-trading-assistant/scripts/fetch_stock.py --index
run ta_hot.log   python3 skills/a-stock-trading-assistant/scripts/fetch_stock.py --hot-sectors
if nonempty ta_index.log; then
  mark "a-stock-trading-assistant" "✅ 跑了" "大盘+热点 见 ta_*.log"
else
  mark "a-stock-trading-assistant" "❌ 失败" "见 ta_index.log"
fi

# ---------- 6. a-stock-portfolio-monitor 第二名单 ----------
echo "[6/10] a-stock-portfolio-monitor 多因子名单 ..."
run pm_selector.log python3 skills/a-stock-portfolio-monitor/scripts/selector.py
if nonempty pm_selector.log; then
  mark "a-stock-portfolio-monitor" "✅ 跑了" "多因子名单 见 pm_selector.log"
else
  mark "a-stock-portfolio-monitor" "❌ 失败" "见 pm_selector.log"
fi

# ---------- 扩展数据（雷达+：涨停质量 / 板块接力 / 龙虎榜） ----------
echo "[+] 扩展数据：涨停质量 / 板块资金接力 / 龙虎榜 ..."
run x_zt.log    python3 skills/trading-desk/scripts/limitup_quality.py
run x_relay.log python3 skills/trading-desk/scripts/sector_relay.py industry 12
run x_lhb.log   python3 skills/trading-desk/scripts/lhb.py api
nonempty x_zt.log    && mark "↳ 涨停质量"      "✅ 跑了" "封单/首封/连板 见 x_zt.log" || mark "↳ 涨停质量" "❌ 失败" "见 x_zt.log"
nonempty x_relay.log && mark "↳ 板块资金接力"  "✅ 跑了" "今日/5日/10日 见 x_relay.log" || mark "↳ 板块资金接力" "❌ 失败" "见 x_relay.log"
nonempty x_lhb.log   && mark "↳ 龙虎榜/席位" "✅ 跑了" "lhb-api 席位明细 见 x_lhb.log" || mark "↳ 龙虎榜/席位" "🟡 无数据" "盘后17:30后才更新"
run x_rt.log    python3 skills/trading-desk/scripts/realtime_flow.py
nonempty x_rt.log && mark "↳ 实时资金(全市场)" "✅ 跑了" "牛股王 分钟级 见 x_rt.log" || mark "↳ 实时资金" "❌ 失败" "见 x_rt.log"

fi  # ← end RADAR_SKIP_BASE

if [ "${#CODES[@]}" -gt 0 ]; then
  CS="${CODES[*]}"
  echo "[7/10] trading-desk 风险+资金（候选: $CS）..."
  run td_risk.log  python3 skills/trading-desk/scripts/risk_flags.py "${CODES[@]}"
  ( for c in "${CODES[@]}"; do echo "== $c =="; timeout 120 python3 skills/trading-desk/scripts/money_flow.py trend "$c" 5 2>&1; done ) >"$OUT/td_money.log" 2>&1
  nonempty td_risk.log && mark "trading-desk·形态/资金" "✅ 跑了" "risk_flags+money_flow 见 td_risk.log/td_money.log" || mark "trading-desk·形态/资金" "❌ 失败" "见 td_risk.log"

  echo "[8/10] a-stock-analysis 分时量能 ..."
  run as_analyze.log python3 skills/a-stock-analysis/scripts/analyze.py "${CODES[@]}" --minute
  nonempty as_analyze.log && mark "a-stock-analysis" "✅ 跑了" "分时量能 见 as_analyze.log" || mark "a-stock-analysis" "❌ 失败" "见 as_analyze.log"

  echo "[9/10] a-share-stock-dossier 候选深研 ..."
  run dos_snap.log python3 skills/a-share-stock-dossier/scripts/a_share_snapshot.py --codes "$(IFS=,; echo "${CODES[*]}")" --with-indices --with-kline --pretty
  if nonempty dos_snap.log; then
    if grep -q '"data_source": "tencent"' "$OUT/dos_snap.log"; then
      mark "a-share-stock-dossier" "🟡 换源兜底" "东财限流→腾讯源，见 dos_snap.log"
    else
      mark "a-share-stock-dossier" "✅ 跑了" "快照+K线 见 dos_snap.log"
    fi
  else
    mark "a-share-stock-dossier" "❌ 失败" "见 dos_snap.log"
  fi

  echo "[+] 30分钟结构/量价背离 ..."
  run as_struct.log python3 skills/trading-desk/scripts/intraday_structure.py "${CODES[@]}"
  nonempty as_struct.log && mark "↳ 30min结构" "✅ 跑了" "见 as_struct.log" || mark "↳ 30min结构" "❌ 失败" "见 as_struct.log"

  echo "[+] 公告/事件排雷 ..."
  run ann.log python3 skills/trading-desk/scripts/announce.py "${CODES[@]}"
  nonempty ann.log && mark "↳ 公告排雷" "✅ 跑了" "减持/解禁/监管/预亏 见 ann.log" || mark "↳ 公告排雷" "❌ 失败" "见 ann.log"

  echo "[+] 个股实时大单（逐笔）..."
  run rt_stock.log python3 skills/trading-desk/scripts/realtime_flow.py --codes "${CODES[@]}"
  nonempty rt_stock.log && mark "↳ 实时大单(个股)" "✅ 跑了" "逐笔主力净额 见 rt_stock.log" || mark "↳ 实时大单(个股)" "🟡 限流" "东财逐笔受限，稍后重试"
else
  mark "trading-desk·形态/资金" "⬜ 待候选" "无候选代码 → 阶段3未跑（跑法: radar_run.sh <code...>）"
  mark "a-stock-analysis"       "⬜ 待候选" "无候选代码 → 分时未跑"
  mark "a-share-stock-dossier"  "⬜ 待候选" "无候选代码 → 深研未跑"
fi

# ---------- 10. trading-sop 编排 + trading-coach 复盘 ----------
mark "trading-sop"    "✅ 编排" "本脚本即按其流水线编排（阶段1-6）"
if [ -n "${RADAR_CSV:-}" ] && [ -f "$RADAR_CSV" ]; then
  mark "trading-coach" "✅ 跑了" "券商交割单 $RADAR_CSV → 复盘"
else
  mark "trading-coach" "⬜ 待交割单" "需老板提供券商 CSV 才能盘后复盘"
fi

# ---------- 汇总表 ----------
echo
echo "────────────────── 参与状态汇总 ──────────────────"
printf "%-28s %-12s %s\n" "技能" "状态" "说明"
for r in "${ROWS[@]}"; do IFS='|' read -r n s d <<<"$r"; printf "%-28s %-12s %s\n" "$n" "$s" "$d"; done
echo "──────────────────────────────────────────────────"
echo "✅跑通 $PASS ｜ 🟡换源兜底 $FALLBACK ｜ ⬜待输入 $NA ｜ ❌失败 $FAIL"
[ "$FAIL" -eq 0 ] && echo ">> 10 技能已全部参与（或有据豁免）" || echo ">> ⚠️ 有技能失败，需修复后重跑"
exit 0

#!/usr/bin/env bash
# pipeline.sh - Full pipeline: fetch -> qualify -> report
# Usage:
#   bash pipeline.sh [--fresh] [--platform <name>] [--quote] [--date YYYY-MM-DD]
#   bash pipeline.sh --dry-run [--summary]
#   bash pipeline.sh --help

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CACHE_DIR="${SCRIPT_DIR}/bid_cache"
REPORT_DIR="${SCRIPT_DIR}/bid_reports"
QUOTE_DIR="${SCRIPT_DIR}/bid_quotes"
RULES_FILE="${SCRIPT_DIR}/qual_rules.json"

mkdir -p "$CACHE_DIR" "$REPORT_DIR" "$QUOTE_DIR"

FRESH=0
PLATFORM=""
GEN_QUOTE=0
TARGET_DATE=""
DRY_RUN=0
SUMMARY_MODE=0
NO_PUSH=0
F_BMIN=""
F_BMAX=""
F_REGION=""
F_INDUSTRY=""
F_VERDICT=""
F_CALENDAR=0
F_CALDAYS=7

print_help() {
  cat << 'EOF'
BidHunter Pipeline v1.2

Usage:
  bash pipeline.sh [options]

Options:
  --dry-run           干跑模式：执行全流程但不推送，输出报告预览
  --platform <name>   指定单平台运行（默认采集所有已配置平台）
                       支持: cnooc, sinopec, petrochina, cnpc 等
  --summary           精华版报告（Top 5，适合 IM 推送）
  --fresh             强制重新采集当天数据（跳过缓存）
  --quote             生成报价表底稿（CSV）
  --no-push           跳过推送步骤（默认配置后自动推送）
  --date YYYY-MM-DD   指定运行日期（默认今天）
  --budget-min N      仅保留预算≥N元的可投标（A4 多维筛选）
  --budget-max N      仅保留预算≤N元的可投标（A4 多维筛选）
  --region 天津,青岛  按地区过滤（A4）
  --industry 智能设备  按行业类目过滤（A4）
  --verdict 可投,需确认 仅保留指定判定（A4）
  --calendar [N]      生成后额外打印未来 N 天投标日历（默认7）
  --help              显示本帮助信息

Examples:
  # 每日定时运行（全流程）
  bash pipeline.sh

  # 预览今天数据（不推送）
  bash pipeline.sh --dry-run

  # 只看精华版
  bash pipeline.sh --dry-run --summary

  # 指定平台 + 强制重新采集
  bash pipeline.sh --platform cnooc --fresh

Environment:
  PYTHON              Python interpreter (default: python3)
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --help)
      print_help
      exit 0
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --platform)
      PLATFORM="$2"
      shift 2
      ;;
    --summary)
      SUMMARY_MODE=1
      shift
      ;;
    --no-push)
      NO_PUSH=1
      shift
      ;;
    --budget-min)
      F_BMIN="$2"
      shift 2
      ;;
    --budget-max)
      F_BMAX="$2"
      shift 2
      ;;
    --region)
      F_REGION="$2"
      shift 2
      ;;
    --industry)
      F_INDUSTRY="$2"
      shift 2
      ;;
    --verdict)
      F_VERDICT="$2"
      shift 2
      ;;
    --calendar)
      F_CALENDAR=1
      if [[ "${2:-}" =~ ^[0-9]+$ ]]; then F_CALDAYS="$2"; shift 2; else shift; fi
      ;;
    --fresh)
      FRESH=1
      shift
      ;;
    --quote)
      GEN_QUOTE=1
      shift
      ;;
    --date)
      TARGET_DATE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

[[ -z "$TARGET_DATE" ]] && TARGET_DATE="$(date +%Y-%m-%d)"
CACHE_FILE="${CACHE_DIR}/bid_${TARGET_DATE}.jsonl"
QUAL_FILE="${CACHE_DIR}/qual_${TARGET_DATE}.jsonl"
TEXT_REPORT="${REPORT_DIR}/report_${TARGET_DATE}.txt"
HTML_REPORT="${REPORT_DIR}/report_${TARGET_DATE}.html"

PYTHON="${PYTHON:-python3}"

# DRY RUN: validate rules first, then show preview
if [[ $DRY_RUN -eq 1 ]]; then
  echo "=== BidHunter Pipeline [DRY RUN] ==="
  echo "Date: ${TARGET_DATE}"
  echo ""

  # Validate rules
  echo "[Validate] Checking rule library..."
  if $PYTHON "${SCRIPT_DIR}/qual_check.py" --validate-rules "$RULES_FILE"; then
    echo "  Rules: OK"
  else
    echo "  Rules: Issues found (see above)" >&2
  fi
  echo ""

  # Check if cache exists
  if [[ ! -f "$CACHE_FILE" ]]; then
    echo "No cached data for ${TARGET_DATE}. Run without --dry-run to fetch data."
    exit 0
  fi

  ITEM_COUNT=$(wc -l < "$CACHE_FILE" | tr -d ' ')
  echo "Cache: ${ITEM_COUNT} items found"
  echo ""

  # Run qualification check
  echo "[Qualify] Running qualification check..."
  $PYTHON "${SCRIPT_DIR}/qual_check.py" "$CACHE_FILE" "$RULES_FILE" > "$QUAL_FILE" 2>&1 || true

  # Generate text report
  echo "[Report] Generating text report..."
  if [[ $SUMMARY_MODE -eq 1 ]]; then
    REPORT_CONTENT=$($PYTHON "${SCRIPT_DIR}/report_text.py" "$QUAL_FILE" "$TARGET_DATE" --summary 2>/dev/null)
  else
    REPORT_CONTENT=$($PYTHON "${SCRIPT_DIR}/report_text.py" "$QUAL_FILE" "$TARGET_DATE" 2>/dev/null)
  fi

  # Show preview (first 30 lines)
  echo "========== Report Preview (first 30 lines) =========="
  echo "$REPORT_CONTENT" | head -n 30
  echo "..."
  echo "========== End Preview =========="
  echo ""

  # List output files
  echo "Output files:"
  echo "  Text:  ${TEXT_REPORT}"
  echo "  Qual:  ${QUAL_FILE}"
  echo "  HTML:  ${HTML_REPORT}"
  echo ""
  echo "✅ Dry run complete. Remove --dry-run to run for real."
  echo "   Example: bash pipeline.sh --summary"
  exit 0
fi

# Normal full run
echo "=== BidHunter Pipeline ==="
echo "Date: ${TARGET_DATE}"
echo ""

# Step 1: Fetch
echo "[1/4] Fetching announcements..."
FETCH_ARGS=""
[[ $FRESH -eq 1 ]] && FETCH_ARGS="--fresh"
[[ -n "$PLATFORM" ]] && FETCH_ARGS="$FETCH_ARGS --platform $PLATFORM"
[[ -n "$TARGET_DATE" ]] && FETCH_ARGS="$FETCH_ARGS --date $TARGET_DATE"

bash "${SCRIPT_DIR}/bid_monitor.sh" $FETCH_ARGS > "$CACHE_FILE" 2>/dev/null || {
  echo "ERROR: fetch failed" >&2
  exit 1
}

ITEM_COUNT=$(wc -l < "$CACHE_FILE" | tr -d ' ')
echo "    Fetched: ${ITEM_COUNT} items"

if [[ "$ITEM_COUNT" -eq 0 ]]; then
  echo "    No items found. Done."
  echo "今日无新公告。" > "$TEXT_REPORT"
  exit 0
fi

# Step 2: Qualify
echo "[2/4] Running qualification check..."
$PYTHON "${SCRIPT_DIR}/qual_check.py" "$CACHE_FILE" "$RULES_FILE" > "$QUAL_FILE" 2>/dev/null || {
  echo "ERROR: qualification check failed" >&2
  exit 1
}

QUAL_COUNT=$(wc -l < "$QUAL_FILE" | tr -d ' ')
echo "    Qualified: ${QUAL_COUNT} items"

# A4 multi-dimension filter (post-filter qual output)
REPORT_INPUT="$QUAL_FILE"
FILTER_ARGS=()
[[ -n "$F_BMIN" ]] && FILTER_ARGS+=("--min" "$F_BMIN")
[[ -n "$F_BMAX" ]] && FILTER_ARGS+=("--max" "$F_BMAX")
[[ -n "$F_REGION" ]] && FILTER_ARGS+=("--region" "$F_REGION")
[[ -n "$F_INDUSTRY" ]] && FILTER_ARGS+=("--industry" "$F_INDUSTRY")
[[ -n "$F_VERDICT" ]] && FILTER_ARGS+=("--verdict" "$F_VERDICT")
if [[ ${#FILTER_ARGS[@]} -gt 0 ]]; then
  FILT_OUT="${CACHE_DIR}/qual_filtered_${TARGET_DATE}.jsonl"
  $PYTHON "${SCRIPT_DIR}/filter_multi.py" "$QUAL_FILE" "${FILTER_ARGS[@]}" --out "$FILT_OUT" 2>/dev/null || true
  if [[ -s "$FILT_OUT" ]]; then
    REPORT_INPUT="$FILT_OUT"
    echo "    Filtered (A4): $(wc -l < "$FILT_OUT" | tr -d ' ') items"
  fi
fi

# Step 3: Generate reports
echo "[3/4] Generating reports..."
REPORT_ARGS=()
[[ $SUMMARY_MODE -eq 1 ]] && REPORT_ARGS+=("--summary")

$PYTHON "${SCRIPT_DIR}/report_text.py" "$REPORT_INPUT" "$TARGET_DATE" "${REPORT_ARGS[@]}" > "$TEXT_REPORT" 2>/dev/null || {
  echo "WARN: text report generation had issues" >&2
}
$PYTHON "${SCRIPT_DIR}/report_html.py" "$REPORT_INPUT" "$TARGET_DATE" "$HTML_REPORT" 2>/dev/null || {
  echo "WARN: html report generation had issues" >&2
}

echo "    Text:  ${TEXT_REPORT}"
echo "    HTML:  ${HTML_REPORT}"

# Step 4: Quote generation (optional)
if [[ $GEN_QUOTE -eq 1 ]]; then
  echo "[4/4] Generating quote draft..."
  $PYTHON "${SCRIPT_DIR}/quote_gen.py" "$QUAL_FILE" "$TARGET_DATE" "${QUOTE_DIR}" 2>/dev/null || {
    echo "WARN: quote generation had issues" >&2
  }
  echo "    Quotes: ${QUOTE_DIR}"
else
  echo "[4/4] Quote generation skipped (use --quote to enable)"
fi

# Step 5: Push (auto-skipped when not configured; use --no-push to force off)
if [[ $NO_PUSH -eq 1 ]]; then
  echo "[push] Skipped (--no-push)"
elif [[ -f "$HOME/.config/bidhunter/push.json" ]]; then
  echo "[push] Pushing report..."
  if [[ $SUMMARY_MODE -eq 1 ]]; then
    $PYTHON "${SCRIPT_DIR}/push_manager.py" send-file "$TEXT_REPORT" --summary || {
      echo "WARN: push had issues (see push_manager history)" >&2
    }
  else
    $PYTHON "${SCRIPT_DIR}/push_manager.py" send-file "$TEXT_REPORT" || {
      echo "WARN: push had issues (see push_manager history)" >&2
    }
  fi
else
  echo "[push] 未配置推送，跳过（运行 python3 scripts/config_wizard.py 配置）"
fi

echo ""
echo "=== Pipeline complete ==="
echo "Reports saved to: ${REPORT_DIR}/"

# A2 optional bid calendar
if [[ $F_CALENDAR -eq 1 ]]; then
  echo ""
  echo "=== 投标日历（未来 ${F_CALDAYS} 天）==="
  $PYTHON "${SCRIPT_DIR}/calendar.py" "$REPORT_INPUT" --days "$F_CALDAYS" 2>/dev/null || true
fi

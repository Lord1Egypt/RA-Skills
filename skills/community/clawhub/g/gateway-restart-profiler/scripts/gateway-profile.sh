#!/bin/bash
#
# OpenClaw Gateway Restart Profiler - Linux Bash 版本 (可视化图表版)
# 用法: bash gateway-profile.sh
#

set -e

# 配置
LOG_DIR="${HOME}/.openclaw/logs"
TMP_LOG_DIR="/tmp/openclaw"
TIMESTAMP=$(date '+%Y-%m-%d-%H%M%S')
REPORT_FILE="${LOG_DIR}/gateway-profile-${TIMESTAMP}.txt"
HTML_REPORT_FILE="${LOG_DIR}/gateway-profile-${TIMESTAMP}.html"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 阶段映射
declare -A STAGES=(
    ["loading configuration"]="配置加载"
    ["resolving authentication"]="身份验证"
    ["starting..."]="启动中"
    ["starting HTTP server"]="HTTP服务"
    ["canvas"]="Canvas"
    ["MCP loopback server"]="MCP服务"
    ["heartbeat"]="心跳服务"
    ["health-monitor"]="健康监控"
    ["agent model"]="模型加载"
    ["ready"]="就绪"
    ["starting channels"]="频道启动"
    ["embedded acpx"]="ACPX插件"
    ["browser/server"]="浏览器控制"
    ["bonjour"]="Bonjour广播"
    ["hooks"]="Hooks"
    ["plugins"]="插件系统"
)

# 阶段耗时（毫秒）
declare -A PHASE_TIMES
PREV_TIME=""
PREV_STAGE=""

echo -e "${CYAN}==============================================${NC}"
echo -e "${CYAN}  OpenClaw Gateway Restart Profiler (Linux)${NC}"
echo -e "${CYAN}       === 可视化图表版 ===${NC}"
echo -e "${CYAN}==============================================${NC}"
echo ""

# 查找最新的日志文件
LOG_FILE=""
if [ -d "$LOG_DIR" ]; then
    LOG_FILE=$(ls -t ${LOG_DIR}/openclaw-*.log 2>/dev/null | head -1)
fi
if [ -z "$LOG_FILE" ] && [ -d "$TMP_LOG_DIR" ]; then
    LOG_FILE=$(ls -t ${TMP_LOG_DIR}/openclaw-*.log 2>/dev/null | head -1)
fi
if [ -z "$LOG_FILE" ]; then
    LOG_FILE="${TMP_LOG_DIR}/openclaw-$(date '+%Y-%m-%d').log"
fi
echo -e "  日志文件: ${CYAN}${LOG_FILE}${NC}"

if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}错误: 日志文件不存在: $LOG_FILE${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[$(date '+%H:%M:%S')] 停止现有 Gateway...${NC}"
openclaw gateway stop 2>/dev/null || true
sleep 3

echo -e "${YELLOW}[$(date '+%H:%M:%S')] 启动 Gateway 并分析日志...${NC}"
echo ""
echo -e "${CYAN}----------------------------------------------${NC}"
echo -e "${CYAN}  实时日志监控 (约3分钟后自动结束)${NC}"
echo -e "${CYAN}----------------------------------------------${NC}"
echo ""

LAST_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE" 2>/dev/null)
START_TIME=$(date +%s)
TIMEOUT=180

# 后台启动 Gateway
openclaw gateway start > /dev/null 2>&1 &
GW_PID=$!

# 初始化日志解析
parse_log_line() {
    local line="$1"
    local stage_found=""

    for key in "${!STAGES[@]}"; do
        local key_lower=$(echo "$key" | tr '[:upper:]' '[:lower:]')
        local line_lower=$(echo "$line" | tr '[:upper:]' '[:lower:]')
        if [[ "$line_lower" == *"$key_lower"* ]]; then
            stage_found="${STAGES[$key]}"
            break
        fi
    done

    if [ -z "$stage_found" ]; then
        return 1
    fi

    # 提取时间戳
    local ts=""
    if [[ $line =~ time=\"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})\.([0-9]+)\" ]]; then
        ts="${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
    elif [[ $line =~ ^([0-9]{2}:[0-9]{2}:[0-9]{2}) ]]; then
        ts="$(date '+%Y-%m-%d') ${BASH_REMATCH[1]} 000"
    fi

    if [ -z "$ts" ]; then
        return 1
    fi

    # 计算上一个阶段的耗时
    if [ -n "$PREV_TIME" ] && [ -n "$PREV_STAGE" ]; then
        # 简单计算毫秒差
        local t1_sec=$(echo "$PREV_TIME" | awk '{print $2}' | cut -d: -f1-3)
        local t2_sec=$(echo "$ts" | awk '{print $2}' | cut -d: -f1-3)
        local t1_ms=$(echo "$PREV_TIME" | awk '{print $3}')
        local t2_ms=$(echo "$ts" | awk '{print $3}')

        local t1=$(date -d "$t1_sec" +%s%3N 2>/dev/null || date -j -f "%H:%M:%S" "$t1_sec" +%s%3N 2>/dev/null)
        local t2=$(date -d "$t2_sec" +%s%3N 2>/dev/null || date -j -f "%H:%M:%S" "$t2_sec" +%s%3N 2>/dev/null)

        if [ -n "$t1" ] && [ -n "$t2" ]; then
            local dur=$((t2 - t1 + t2_ms - t1_ms))
            if [ "$dur" -gt 0 ] && [ "$dur" -lt 300000 ]; then
                PHASE_TIMES["$PREV_STAGE"]=$dur
            fi
        fi
    fi

    PREV_TIME="$ts"
    PREV_STAGE="$stage_found"

    local time_str=$(echo "$ts" | awk '{print $2}')
    echo -e "${CYAN}[$time_str]${NC} $stage_found"
    return 0
}

# 主监控循环
while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))

    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo -e "${YELLOW}超时，停止监听${NC}"
        break
    fi

    if ! kill -0 $GW_PID 2>/dev/null; then
        break
    fi

    CURRENT_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE" 2>/dev/null)

    if [ "$CURRENT_SIZE" -gt "$LAST_SIZE" ]; then
        # 读取新增的内容
        dd if="$LOG_FILE" bs=1 skip=$LAST_SIZE count=$((CURRENT_SIZE - LAST_SIZE)) 2>/dev/null | while IFS= read -r line; do
            parse_log_line "$line" 2>/dev/null || true
        done
        LAST_SIZE=$CURRENT_SIZE
    fi

    sleep 0.5
done

sleep 5

echo ""
echo -e "${CYAN}==============================================${NC}"
echo -e "${CYAN}  Gateway 重启性能报告${NC}"
echo -e "${CYAN}==============================================${NC}"
echo ""
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "日志文件: $LOG_FILE"
echo ""

echo -e "${YELLOW}阶段耗时明细 (按耗时降序):${NC}"
echo ""

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

# 计算 TOTAL_MS 和 MAX_MS
TOTAL_MS=0
MAX_MS=1
if [ ${#PHASE_TIMES[@]} -gt 0 ]; then
    for ms in "${PHASE_TIMES[@]}"; do
        TOTAL_MS=$((TOTAL_MS + ms))
        if [ "$ms" -gt "$MAX_MS" ]; then
            MAX_MS=$ms
        fi
    done
fi

# 排序输出（用数组保存排序后的结果）
SORTED_FILE=$(mktemp)
if [ ${#PHASE_TIMES[@]} -gt 0 ]; then
    for stage in "${!PHASE_TIMES[@]}"; do
        echo "${PHASE_TIMES[$stage]} $stage"
    done | sort -rn > "$SORTED_FILE"

    while IFS= read -r line; do
        ms=$(echo "$line" | awk '{print $1}')
        name=$(echo "$line" | awk '{print $2}')
        if [ -z "$ms" ] || [ -z "$name" ]; then
            continue
        fi
        sec=$(echo "scale=2; $ms/1000" | bc)
        bar_len=$((ms / 1000))
        [ "$bar_len" -gt 50 ] && bar_len=50
        bar=$(printf '#%.0s' $(seq 1 $bar_len))

        if [ "$ms" -gt 30000 ]; then
            color=$RED
        elif [ "$ms" -gt 10000 ]; then
            color=$YELLOW
        else
            color=$GREEN
        fi

        printf "  %-20s %8sms (%6ss) ${color}%s${NC}\n" "$name" "$ms" "$sec" "$bar"
    done < "$SORTED_FILE"
else
    echo -e "  ${YELLOW}未能解析到阶段数据，请检查日志文件是否存在${NC}"
fi

rm -f "$SORTED_FILE"

echo ""
echo -e "${CYAN}----------------------------------------------${NC}"
echo -e "  总耗时: ${TOTAL_DURATION}秒 (约 $((TOTAL_DURATION / 60)) 分钟)"
echo -e "${CYAN}----------------------------------------------${NC}"
echo ""

# ==============================================
# 生成 HTML 可视化报告
# ==============================================

# 收集图表数据
CHART_LABELS=""
CHART_DATA=""
CHART_COLORS=""
TABLE_ROWS=""
SUGGESTIONS=""
PHASE_COUNT=0
AVG_MS=0
SLOW_COUNT=0

if [ ${#PHASE_TIMES[@]} -gt 0 ]; then
    # 计算 PHASE_COUNT 和 AVG_MS
    for v in "${PHASE_TIMES[@]}"; do
        PHASE_COUNT=$((PHASE_COUNT + 1))
    done
    if [ $PHASE_COUNT -gt 0 ]; then
        AVG_MS=$((TOTAL_MS / PHASE_COUNT))
    fi

    # 生成图表数据
    FIRST=1
    while IFS= read -r line; do
        ms=$(echo "$line" | awk '{print $1}')
        name=$(echo "$line" | awk '{print $2}')
        [ -z "$ms" ] || [ -z "$name" ] && continue

        # 颜色
        row_color="#22c55e"
        if [ "$ms" -gt 30000 ]; then
            row_color="#ef4444"
            SLOW_COUNT=$((SLOW_COUNT + 1))
        elif [ "$ms" -gt 10000 ]; then
            row_color="#f97316"
        fi

        # 图表分隔符
        if [ "$FIRST" -eq 1 ]; then
            FIRST=0
        else
            CHART_LABELS+=","
            CHART_DATA+=","
            CHART_COLORS+=","
        fi
        CHART_LABELS+="\"$name\""
        CHART_DATA+="$ms"
        CHART_COLORS+="\"$row_color\""

        # 百分比
        if [ "$TOTAL_MS" -gt 0 ]; then
            pct=$(echo "scale=1; ($ms/$TOTAL_MS)*100" | bc)
        else
            pct=0
        fi

        # 进度条
        bar_len=$((ms * 40 / MAX_MS))
        [ "$bar_len" -gt 40 ] && bar_len=40
        bar=$(printf '█%.0s' $(seq 1 $bar_len))

        TABLE_ROWS="${TABLE_ROWS}<tr><td style=\"text-align:left;padding:8px;border-bottom:1px solid #333;\">${name}</td><td style=\"text-align:right;padding:8px;border-bottom:1px solid #333;color:${row_color};font-weight:bold;\">${ms} ms</td><td style=\"text-align:right;padding:8px;border-bottom:1px solid #333;\">$(echo "scale=2; $ms/1000" | bc)s</td><td style=\"text-align:right;padding:8px;border-bottom:1px solid #333;\">${pct}%</td><td style=\"text-align:left;padding:8px;border-bottom:1px solid #333;color:${row_color};font-family:monospace;\">${bar}</td></tr>"

        # 建议
        case "$name" in
            "配置加载") [ "$ms" -gt 30000 ] && SUGGESTIONS="${SUGGESTIONS}<li><strong>[配置加载]</strong> 检查配置文件是否过大或损坏</li>" ;;
            "身份验证") [ "$ms" -gt 30000 ] && SUGGESTIONS="${SUGGESTIONS}<li><strong>[身份验证]</strong> 检查网络连接和认证服务</li>" ;;
            "模型加载") [ "$ms" -gt 30000 ] && SUGGESTIONS="${SUGGESTIONS}<li><strong>[模型加载]</strong> Ollama服务可能响应慢，考虑换用API模式</li>" ;;
            "频道启动") [ "$ms" -gt 30000 ] && SUGGESTIONS="${SUGGESTIONS}<li><strong>[频道启动]</strong> 检查QQ/Telegram等频道连接状态</li>" ;;
            "插件系统") [ "$ms" -gt 30000 ] && SUGGESTIONS="${SUGGESTIONS}<li><strong>[插件系统]</strong> npm依赖可能需要重新安装</li>" ;;
        esac
    done < "$SORTED_FILE"
fi

# 如果没有建议
if [ -z "$SUGGESTIONS" ]; then
    SUGGESTIONS="<li style=\"color:#22c55e\">✓ 各阶段耗时正常，无明显瓶颈</li>"
fi

# 生成 HTML 文件
cat > "$HTML_REPORT_FILE" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenClaw Gateway 重启性能报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',system-ui,sans-serif; background:#0f172a; color:#e2e8f0; min-height:100vh; padding:24px; }
.container { max-width:1100px; margin:0 auto; }
.header { text-align:center; margin-bottom:32px; padding:24px; background:linear-gradient(135deg,#1e293b,#334155); border-radius:16px; border:1px solid #334155; }
.header h1 { font-size:28px; color:#f8fafc; margin-bottom:8px; }
.header .meta { color:#94a3b8; font-size:14px; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }
.card { background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; }
.card h2 { font-size:16px; color:#94a3b8; margin-bottom:16px; text-transform:uppercase; letter-spacing:1px; border-bottom:1px solid #334155; padding-bottom:8px; }
.big-number { font-size:56px; font-weight:700; color:#f8fafc; text-align:center; line-height:1; }
.big-number span { font-size:20px; color:#94a3b8; font-weight:400; }
.unit-label { text-align:center; color:#64748b; margin-top:8px; font-size:14px; }
.chart-box { position:relative; height:300px; }
.stats-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:16px; }
.stat { background:#0f172a; border-radius:8px; padding:12px; text-align:center; }
.stat .val { font-size:22px; font-weight:600; color:#f8fafc; }
.stat .lbl { font-size:12px; color:#64748b; margin-top:4px; }
table { width:100%; border-collapse:collapse; margin-top:8px; }
th { text-align:left; padding:10px 8px; color:#64748b; font-size:12px; text-transform:uppercase; border-bottom:1px solid #334155; }
td { font-size:14px; }
.suggestions { list-style:none; padding:0; }
.suggestions li { padding:10px 14px; margin-bottom:8px; background:#0f172a; border-radius:8px; border-left:4px solid #f97316; color:#fb923c; font-size:14px; }
.suggestions li[style*="22c55e"] { border-left-color:#22c55e; color:#22c55e; }
.legend { display:flex; gap:16px; margin-top:12px; flex-wrap:wrap; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:12px; color:#94a3b8; }
.legend-dot { width:12px; height:12px; border-radius:3px; }
footer { text-align:center; color:#475569; font-size:12px; margin-top:24px; }
@media(max-width:768px) { .grid { grid-template-columns:1fr; } .stats-grid { grid-template-columns:1fr; } }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🚀 OpenClaw Gateway 重启性能报告</h1>
    <div class="meta">REPORT_META</div>
  </div>

  <div class="grid">
    <div class="card">
      <h2>⏱️ 总耗时</h2>
      <div class="big-number">TOTAL_DURATION<span>秒</span></div>
      <div class="unit-label">约 MINUTES 分钟</div>
      <div class="stats-grid">
        <div class="stat"><div class="val">PHASE_COUNT</div><div class="lbl">检测阶段数</div></div>
        <div class="stat"><div class="val">TOTAL_MS_S s</div><div class="lbl">阶段累计</div></div>
        <div class="stat"><div class="val">AVG_MS ms</div><div class="lbl">平均耗时</div></div>
      </div>
    </div>

    <div class="card">
      <h2>📊 耗时分布</h2>
      <div class="chart-box"><canvas id="pieChart"></canvas></div>
      <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>> 30s</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f97316"></div>10-30s</div>
        <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>< 10s</div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:20px;">
    <h2>📈 阶段耗时明细（柱状图）</h2>
    <div class="chart-box" style="height:350px;"><canvas id="barChart"></canvas></div>
  </div>

  <div class="card" style="margin-bottom:20px;">
    <h2>📋 详细数据表</h2>
    <table>
      <thead>
        <tr>
          <th>阶段</th>
          <th style="text-align:right;">毫秒</th>
          <th style="text-align:right;">秒</th>
          <th style="text-align:right;">占比</th>
          <th>耗时可视化</th>
        </tr>
      </thead>
      <tbody>
        TABLE_ROWS
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>💡 优化建议</h2>
    <ul class="suggestions">
      SUGGESTIONS
    </ul>
  </div>
</div>

<script>
const ctxPie = document.getElementById('pieChart').getContext('2d');
const ctxBar = document.getElementById('barChart').getContext('2d');

new Chart(ctxPie, {
    type: 'doughnut',
    data: { labels: CHART_LABELS, datasets: [{ data: CHART_DATA, backgroundColor: CHART_COLORS, borderColor: '#0f172a', borderWidth: 3, hoverOffset: 8 }] },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
            legend: { position:'bottom', labels:{ color:'#94a3b8', padding:16, font:{ size:12 } } },
            tooltip: { callbacks: { label: function(ctx) { const total = ctx.dataset.data.reduce((a,b)=>a+b,0); const pct = ((ctx.raw/total)*100).toFixed(1); return ctx.label + ': ' + ctx.raw + 'ms (' + pct + '%)'; } } }
        }
    }
});

new Chart(ctxBar, {
    type: 'bar',
    data: { labels: CHART_LABELS, datasets: [{ label: '耗时 (ms)', data: CHART_DATA, backgroundColor: CHART_COLORS, borderRadius: 6, borderSkipped: false }] },
    options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display:false }, tooltip: { callbacks: { label: function(ctx) { return ctx.raw + 'ms (' + (ctx.raw/1000).toFixed(2) + 's)'; } } } },
        scales: { x: { grid:{ color:'#334155' }, ticks:{ color:'#94a3b8' }, title:{ display:true, text:'毫秒 (ms)', color:'#64748b' } }, y: { grid:{ display:false }, ticks:{ color:'#e2e8f0', font:{ size:13 } } } }
    }
});
</script>
</body>
</html>
HTMLEOF

# 替换占位符
sed -i "s|REPORT_META|生成时间: $(date '+%Y-%m-%d %H:%M:%S') \&nbsp;\&nbsp; 日志: $LOG_FILE|g" "$HTML_REPORT_FILE"
sed -i "s|TOTAL_DURATION|${TOTAL_DURATION}|g" "$HTML_REPORT_FILE"
sed -i "s|MINUTES|$((TOTAL_DURATION / 60))|g" "$HTML_REPORT_FILE"
sed -i "s|PHASE_COUNT|${PHASE_COUNT}|g" "$HTML_REPORT_FILE"
sed -i "s|TOTAL_MS_S|$(echo "scale=1; $TOTAL_MS/1000" | bc)|g" "$HTML_REPORT_FILE"
sed -i "s|AVG_MS|${AVG_MS}|g" "$HTML_REPORT_FILE"
sed -i "s|CHART_LABELS|[${CHART_LABELS}]|g" "$HTML_REPORT_FILE"
sed -i "s|CHART_DATA|[${CHART_DATA}]|g" "$HTML_REPORT_FILE"
sed -i "s|CHART_COLORS|[${CHART_COLORS}]|g" "$HTML_REPORT_FILE"
sed -i "s|TABLE_ROWS|${TABLE_ROWS}|g" "$HTML_REPORT_FILE"
sed -i "s|SUGGESTIONS|${SUGGESTIONS}|g" "$HTML_REPORT_FILE"

# 文本报告保存
{
    echo "OpenClaw Gateway Restart Performance Report (Linux)"
    echo "=================================================="
    echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "日志文件: $LOG_FILE"
    echo ""
    echo "阶段耗时明细:"
    if [ ${#PHASE_TIMES[@]} -gt 0 ]; then
        for stage in "${!PHASE_TIMES[@]}"; do
            echo "  ${PHASE_TIMES[$stage]}ms - $stage"
        done | sort -rn
    fi
} > "$REPORT_FILE"

echo ""
echo -e "${GREEN}[文本报告已保存: $REPORT_FILE]${NC}"
echo -e "${GREEN}[HTML图表报告已保存: $HTML_REPORT_FILE]${NC}"
echo -e "${YELLOW}  → 用浏览器打开 HTML 文件查看可视化图表！${NC}"
echo ""

# 优化建议输出
echo -e "${CYAN}==============================================${NC}"
echo -e "${CYAN}  优化建议${NC}"
echo -e "${CYAN}==============================================${NC}"
echo ""

if [ "$SLOW_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}以下阶段耗时超过30秒，值得关注：${NC}"
    echo "$SUGGESTIONS" | sed 's/<li>/  • /g' | sed 's/<[^>]*>//g'
else
    echo -e "  ${GREEN}各阶段耗时正常，无明显瓶颈${NC}"
fi

echo ""

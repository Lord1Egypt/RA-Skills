#!/usr/bin/env bash
# fetch_xiaoqu.sh — 一键抓取贝壳小区完整数据
#
# 用法：
#   bash fetch_xiaoqu.sh <小区名> [城市前缀] [输出目录]
#
# 示例：
#   bash fetch_xiaoqu.sh "东方花园三期"
#   bash fetch_xiaoqu.sh "东方花园三期" sh /tmp/result/
#   bash fetch_xiaoqu.sh "好世鹿鸣苑" sh /tmp/result/
#
# 依赖：
#   - mcp-chrome 插件运行在 127.0.0.1:12306
#   - parse_beike.py 在同目录下
#   - python3, curl, jq（可选）

set -e

NAME="${1:?用法: $0 <小区名> [城市=sh] [输出目录=/tmp/beike]}"
CITY="${2:-sh}"
OUTDIR="${3:-/tmp/beike}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$OUTDIR"

# ── 1. 初始化 mcp-chrome session ──────────────────────────────────────────
echo "🔌 连接 mcp-chrome..."
INIT_RESP=$(curl -s -i -X POST "http://127.0.0.1:12306/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"beike-fetch","version":"1.0"}}}')

SESSION_ID=$(echo "$INIT_RESP" | grep -i "mcp-session-id:" | awk '{print $2}' | tr -d '\r\n ')
if [ -z "$SESSION_ID" ]; then
  echo "❌ 无法获取 SESSION_ID，请确认 mcp-chrome 插件已启动"
  exit 1
fi
echo "✅ SESSION_ID=$SESSION_ID"

# ── 工具函数 ──────────────────────────────────────────────────────────────
mcp_call() {
  local id=$1 tool=$2 args=$3
  curl -s -X POST "http://127.0.0.1:12306/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "mcp-session-id: $SESSION_ID" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":$id,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}"
}

get_text() {
  python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try: print(json.loads(item.get('text', '')).get('result', ''))
            except: pass
"
}

check_captcha() {
  grep -q "请在下图\|请按语序" "$1"
}

# P1-1: headless 检测
_is_headless() { [ "${BEIKE_HEADLESS:-0}" = "1" ]; }

navigate_and_read() {
  local url=$1 outfile=$2 tab=$3
  echo "  → 导航: $url"
  mcp_call $RANDOM "chrome_navigate" "{\"url\":\"$url\",\"tabId\":$tab}" > /dev/null
  sleep 7
  mcp_call $RANDOM "chrome_javascript" "{\"tabId\":$tab,\"code\":\"return document.body.innerText\"}" \
    | get_text > "$outfile"

  if check_captcha "$outfile"; then
    echo ""
    echo "⚠️  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  贝壳触发验证码！"
    echo "⚠️  请在 Chrome 中手动完成图片点选验证，完成后按 Enter 继续..."
    echo "⚠️  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    # P1-1: headless 模式不挂起，直接报错退出
    if _is_headless; then
      echo '{"status":"captcha_required","step":"navigate_and_read","url":"'"$url"'","message":"贝壳触发验证码，headless 模式无法处理"}' >&2
      exit 4
    fi
    # P0-3: 循环检测最多3次，防贝壳连续出题
    local max_attempts=3
    local attempt=0
    while [ $attempt -lt $max_attempts ]; do
      attempt=$((attempt + 1))
      read -r _
      # 不重新 navigate，直接重读
      mcp_call $RANDOM "chrome_javascript" "{\"tabId\":$tab,\"code\":\"return document.body.innerText\"}" \
        | get_text > "$outfile"
      if ! check_captcha "$outfile"; then
        echo "✅ 验证通过，继续"
        return 0
      fi
      if [ $attempt -lt $max_attempts ]; then
        echo "⚠️  仍有验证码 (${attempt}/${max_attempts})，请再次完成后按 Enter..."
      fi
    done
    echo "❌ 验证码 ${max_attempts} 次均未通过，请重试"
    exit 3
  fi
}

# ── 2. 找可用的贝壳 Tab ───────────────────────────────────────────────────
echo "🔍 查找贝壳 Tab..."
TAB=$(mcp_call 2 "get_windows_and_tabs" "{}" | python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try:
                d = json.loads(item.get('text', ''))
                for w in d.get('windows', []):
                    for t in w.get('tabs', []):
                        if 'ke.com' in t.get('url', ''):
                            print(t['tabId'])
                            raise SystemExit
            except SystemExit: raise
            except: pass
# 找不到贝壳 Tab，用第一个 Tab
for line in sys.stdin.read().split('\n'):
    pass  # already consumed
" 2>/dev/null)

if [ -z "$TAB" ]; then
  # 用 get_windows_and_tabs 的第一个 tab
  TAB=$(mcp_call 3 "get_windows_and_tabs" "{}" | python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try:
                d = json.loads(item.get('text', ''))
                t = d.get('windows', [{}])[0].get('tabs', [{}])[0]
                print(t.get('tabId', ''))
                raise SystemExit
            except SystemExit: raise
            except: pass
")
fi

echo "✅ 使用 Tab ID: $TAB"

# ── 3. Step 1：找小区 ID ──────────────────────────────────────────────────
echo ""
echo "📍 Step 1：查找小区 ID..."
SEARCH_URL="https://${CITY}.ke.com/ershoufang/rs${NAME}/"
mcp_call $RANDOM "chrome_navigate" "{\"url\":\"$SEARCH_URL\",\"tabId\":$TAB}" > /dev/null
sleep 6

XIAOQU_URL=$(mcp_call $RANDOM "chrome_javascript" \
  "{\"tabId\":$TAB,\"code\":\"return document.querySelector('a.agentCardResblockLink')?.href || ''\"}" \
  | get_text)

if [ -z "$XIAOQU_URL" ]; then
  echo "❌ 未找到小区链接，请检查小区名是否正确"
  exit 2
fi

XIAOQU_ID=$(echo "$XIAOQU_URL" | grep -oE '/[0-9]+/' | tr -d '/')
echo "✅ 小区 ID: $XIAOQU_ID"
echo "✅ 小区页: $XIAOQU_URL"

# ── 4. Step 2：小区详情页 ─────────────────────────────────────────────────
echo ""
echo "🏠 Step 2：读取小区详情..."
XIAOQU_FILE="$OUTDIR/${NAME}_xiaoqu.txt"
navigate_and_read "$XIAOQU_URL" "$XIAOQU_FILE" "$TAB"
python3 "$SCRIPT_DIR/parse_beike.py" xiaoqu < "$XIAOQU_FILE" > "$OUTDIR/${NAME}_xiaoqu.json"
echo "✅ 保存: $OUTDIR/${NAME}_xiaoqu.json"

# ── 5. Step 3：在售二手房 ─────────────────────────────────────────────────
echo ""
echo "🏷️  Step 3：读取在售二手房..."
ERSHOU_FILE="$OUTDIR/${NAME}_ershou.txt"
navigate_and_read "https://${CITY}.ke.com/ershoufang/rs${NAME}/" "$ERSHOU_FILE" "$TAB"
python3 "$SCRIPT_DIR/parse_beike.py" ershou < "$ERSHOU_FILE" > "$OUTDIR/${NAME}_ershou.json"
echo "✅ 保存: $OUTDIR/${NAME}_ershou.json"

sleep 10  # 缓冲，降低成交页触发验证码概率

# ── 6. Step 4：成交记录 ───────────────────────────────────────────────────
echo ""
echo "📊 Step 4：读取成交记录..."
CHENGJIAO_FILE="$OUTDIR/${NAME}_chengjiao.txt"
navigate_and_read "https://${CITY}.ke.com/chengjiao/rs${NAME}/" "$CHENGJIAO_FILE" "$TAB"
python3 "$SCRIPT_DIR/parse_beike.py" chengjiao < "$CHENGJIAO_FILE" > "$OUTDIR/${NAME}_chengjiao.json"
echo "✅ 保存: $OUTDIR/${NAME}_chengjiao.json"

# ── 7. 输出摘要 ───────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 ${NAME} 数据摘要"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 - << PYEOF
import json, sys

def load(path):
    try:
        with open(path) as f: return json.load(f)
    except: return {}

xq = load('$OUTDIR/${NAME}_xiaoqu.json')
er = load('$OUTDIR/${NAME}_ershou.json')
cj = load('$OUTDIR/${NAME}_chengjiao.json')

print(f"均价：{xq.get('avg_price','?')} 元/㎡")
print(f"建筑：{xq.get('building_type','?')}，{xq.get('built_year','?')}，容积率{xq.get('far','?')}，绿化率{xq.get('green_rate','?')}")
print(f"规模：{xq.get('total_units','?')}户 / {xq.get('total_buildings','?')}栋")
print(f"物业：{xq.get('mgmt_company','?')}，{xq.get('mgmt_fee','?')} 元/㎡/月")
print(f"关注：{xq.get('followers','?')}人 | 在售：{xq.get('on_sale','?')}套 | 近90天成交：{xq.get('sold_90d','?')}套 | 近30天带看：{xq.get('views_30d','?')}次")

metros = xq.get('metros', [])
if metros:
    m = metros[0]
    print(f"最近地铁：{m['distance_m']}米 {m['line']}")

print(f"\n在售：{er.get('total_listings_approx','?')}套，价格区间 {er.get('price_min','?')}-{er.get('price_max','?')} 万")
if er.get('parking_mention_count', 0) > 0:
    print(f"  产权车位：{er['parking_mention_count']} 套房源提及")

print(f"\n成交：近12月 {cj.get('recent_12m_count','?')} 套（月均 {cj.get('monthly_avg','?')} 套）")
print(f"  成交周期：平均 {cj.get('period_avg_days','?')} 天（快≤60天:{cj.get('fast_sales_count','?')}套 | 慢>180天:{cj.get('slow_sales_count','?')}套）")
if cj.get('has_parking_sales'):
    print(f"  车位成交：{cj.get('parking_sales_count','?')} 次 ✅")
else:
    print(f"  车位成交：未发现 ⚠️")
PYEOF

echo ""
echo "📁 输出文件目录：$OUTDIR/"
echo "✅ 完成！"

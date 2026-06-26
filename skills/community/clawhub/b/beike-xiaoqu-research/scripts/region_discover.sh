#!/usr/bin/env bash
# region_discover.sh — 按地区批量发现并筛选贝壳小区，可选接 consensus 评估
#
# 用法：
#   bash region_discover.sh <板块/区域列表> [城市] [输出目录] [--district <区>] [--no-detail] [--consensus]
#
# 参数说明：
#   板块列表  : 逗号分隔的贝壳 URL 板块路径关键词（如 qibao,gumei）
#               格式1 - 区内板块：qibao,gumei,jinhui  （将拼接 /xiaoqu/{district}/{board}/）
#               格式2 - 完整路径：直接传 "pudong/zhangjiang,pudong/jinqiao" 则不拼接区
#   --district : 指定区域路径段，默认 minhang（闵行）。其他示例：pudong, xuhui, changning
#
# 示例：
#   bash region_discover.sh "qibao,gumei,jinhui"                          # 闵行七宝/古美/金汇
#   bash region_discover.sh "qibao,gumei" sh /tmp/res/                    # 指定城市和输出目录
#   bash region_discover.sh "zhangjiang,jinqiao" sh /tmp/ --district pudong  # 浦东张江/金桥
#   bash region_discover.sh "qibao,gumei" sh /tmp/res/ --consensus        # 抓完做多模型评估
#   bash region_discover.sh "qibao" sh /tmp/ --no-detail                  # 仅发现，不抓详情
#
# 依赖：
#   - mcp-chrome 插件运行在 127.0.0.1:12306
#   - parse_beike.py 在同目录下
#   - mcporter（consensus模式需要）
#   - python3, curl

set -euo pipefail

BOARDS="${1:?用法: $0 <板块列表,逗号分隔> [城市=sh] [输出目录=/tmp/beike_discover] [--district minhang] [--no-detail] [--consensus]}"
CITY="${2:-sh}"
OUTDIR="${3:-/tmp/beike_discover}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DO_DETAIL=true
DO_CONSENSUS=false
DISTRICT="minhang"  # 默认闵行，可通过 --district 覆盖

# 解析可选标志（支持任意位置）
for i in "$@"; do
  case $i in
    --no-detail)      DO_DETAIL=false ;;
    --consensus)      DO_CONSENSUS=true ;;
    --district)       : ;;  # 下一个参数是值，由下面的 prev 机制处理
  esac
done
# 解析 --district <value>
PREV=""
for arg in "$@"; do
  if [ "$PREV" = "--district" ]; then
    DISTRICT="$arg"
  fi
  PREV="$arg"
done

echo "🗺  区域(district): $DISTRICT | 板块: $BOARDS | 城市: $CITY"

mkdir -p "$OUTDIR"

# ── 初始化 mcp-chrome session ─────────────────────────────────────────────
echo "🔌 连接 mcp-chrome..."
INIT_RESP=$(curl -s -i -X POST "http://127.0.0.1:12306/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"beike-discover","version":"2.0"}}}')

SESSION_ID=$(echo "$INIT_RESP" | grep -i "mcp-session-id:" | awk '{print $2}' | tr -d '\r\n ')
if [ -z "$SESSION_ID" ]; then
  echo "❌ 无法获取 SESSION_ID，请确认 mcp-chrome 插件已启动"
  exit 1
fi
echo "✅ SESSION_ID=$SESSION_ID"

# ── 工具函数 ──────────────────────────────────────────────────────────────
mcp_call() {
  curl -s -X POST "http://127.0.0.1:12306/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "mcp-session-id: $SESSION_ID" \
    -d "$1" | python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try: print(json.loads(item.get('text', '')).get('result', ''))
            except: pass
"
}

nav() {
  mcp_call "{\"jsonrpc\":\"2.0\",\"id\":$RANDOM,\"method\":\"tools/call\",\"params\":{\"name\":\"chrome_navigate\",\"arguments\":{\"url\":\"$1\",\"tabId\":$TAB}}}" > /dev/null
  sleep 7
}

read_text() {
  mcp_call "{\"jsonrpc\":\"2.0\",\"id\":$RANDOM,\"method\":\"tools/call\",\"params\":{\"name\":\"chrome_javascript\",\"arguments\":{\"tabId\":$TAB,\"code\":\"return document.body.innerText\"}}}"
}

# P1-2: CSS Selector 精准提取 — 优先用 selector，fallback 到 innerText
# 返回 JSON 字符串，parse_beike.py 的 css_json 模式解析
read_css_json() {
  mcp_call "{\"jsonrpc\":\"2.0\",\"id\":$RANDOM,\"method\":\"tools/call\",\"params\":{\"name\":\"chrome_javascript\",\"arguments\":{\"tabId\":$TAB,\"code\":\"(function(){ try { var sel=function(s,d){var e=(d||document).querySelector(s);return e?e.innerText.trim():''}; var selAll=function(s,d){return Array.from((d||document).querySelectorAll(s)).map(e=>e.innerText.trim())}; var r={_source:'css'}; r.avg_price=sel('.xiaoquUnitPrice .xiaoquUnitPriceNum')||sel('[class*=unitPrice]')||''; r.building_type=sel('[class*=xiaoquInfo] li:nth-child(1) span:last-child')||''; r.built_year=sel('[class*=xiaoquInfo] li:nth-child(2) span:last-child')||''; r.total_units=sel('[class*=xiaoquInfo] li:nth-child(4) span:last-child')||''; r.far=sel('[class*=xiaoquInfo] li:nth-child(5) span:last-child')||''; r.green_rate=sel('[class*=xiaoquInfo] li:nth-child(6) span:last-child')||''; r.mgmt_company=sel('[class*=xiaoquInfo] li:nth-child(7) span:last-child')||''; r.mgmt_fee=sel('[class*=xiaoquInfo] li:nth-child(8) span:last-child')||''; r.on_sale=sel('[class*=houseInfo] [class*=onsale]')||sel('[class*=xiaoquSellInfo] [class*=info]:nth-child(1) [class*=num]')||''; r.sold_90d=sel('[class*=xiaoquSellInfo] [class*=info]:nth-child(2) [class*=num]')||''; r.views_30d=sel('[class*=xiaoquSellInfo] [class*=info]:nth-child(3) [class*=num]')||''; r.captcha=!!(document.querySelector('[class*=geetest]')||document.querySelector('[id*=captcha]')); return JSON.stringify(r); } catch(e){return JSON.stringify({_source:'css_error',error:e.message})} })()\"}}}"|sed 's/\\\\n//g'
}

get_xiaoqu_link() {
  mcp_call "{\"jsonrpc\":\"2.0\",\"id\":$RANDOM,\"method\":\"tools/call\",\"params\":{\"name\":\"chrome_javascript\",\"arguments\":{\"tabId\":$TAB,\"code\":\"return Array.from(document.querySelectorAll('a')).find(a=>a.href.includes('/xiaoqu/') && /\\\\/\\\\d+\\\\//.test(a.href))?.href || ''\"}}}"
}

check_captcha() { grep -q "请在下图\|请按语序" "$1"; }

# P1-1: headless 检测 — BEIKE_HEADLESS=1 时不挂起，输出结构化错误后退出
_is_headless() { [ "${BEIKE_HEADLESS:-0}" = "1" ]; }

handle_captcha() {
  local outfile="$1"
  local context="${2:-unknown}"   # 传入当前步骤名，方便定位

  # Headless 模式：不能交互，直接输出 JSON 错误并退出
  if _is_headless; then
    echo '{"status":"captcha_required","step":"'"$context"'","message":"贝壳触发验证码，headless 模式无法处理，请在交互式环境中手动完成后重试"}' >&2
    exit 4  # exit 4 = captcha in headless
  fi

  local max_attempts=3
  local attempt=0
  while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    echo ""
    echo "⚠️  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  贝壳触发验证码！(第 ${attempt}/${max_attempts} 次尝试)"
    echo "⚠️  请在 Chrome 中手动完成图片点选验证，完成后按 Enter 继续..."
    echo "⚠️  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    read -r _
    read_text > "$outfile"
    if ! check_captcha "$outfile"; then
      echo "✅ 验证通过，继续"
      return 0
    fi
    echo "⚠️  页面仍有验证码，请再次完成..."
  done
  echo "❌ 验证码 ${max_attempts} 次均未通过，跳过此步骤"
  return 1
}

# ── 获取一个贝壳 Tab ──────────────────────────────────────────────────────
TAB=$(mcp_call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_windows_and_tabs","arguments":{}}}' | python3 -c "
import sys, json, re
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try:
                d = json.loads(item.get('text', ''))
                for w in d.get('windows', []):
                    for t in w.get('tabs', []):
                        if 'ke.com' in t.get('url', ''):
                            print(t['tabId']); raise SystemExit
            except SystemExit: raise
            except: pass
# 备用：第一个tab
" 2>/dev/null)

if [ -z "$TAB" ]; then
  TAB=$(mcp_call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_windows_and_tabs","arguments":{}}}' | python3 -c "
import sys, json
for line in sys.stdin.read().split('\n'):
    if line.startswith('data: '):
        j = json.loads(line[6:])
        for item in j.get('result', {}).get('content', []):
            try:
                d = json.loads(item.get('text', ''))
                t = d.get('windows', [{}])[0].get('tabs', [{}])[0]
                print(t.get('tabId', '')); raise SystemExit
            except SystemExit: raise
            except: pass
")
fi

echo "✅ 已找到现有 Tab: $TAB"

# ── P0-3: 创建专用隔离 Tab，避免干扰用户现有页面 ──────────────────────────
echo "🆕 创建专用隔离 Tab..."
NEW_TAB_RESP=$(mcp_call "{\"jsonrpc\":\"2.0\",\"id\":$RANDOM,\"method\":\"tools/call\",\"params\":{\"name\":\"create_tab\",\"arguments\":{\"url\":\"about:blank\"}}}" 2>/dev/null)
ISOLATED_TAB=$(echo "$NEW_TAB_RESP" | python3 -c "
import sys, re
text = sys.stdin.read()
m = re.search(r'tabId[\":\s]+(\d+)', text)
print(m.group(1) if m else '')
" 2>/dev/null)

if [ -n "$ISOLATED_TAB" ] && [ "$ISOLATED_TAB" != "0" ]; then
  TAB="$ISOLATED_TAB"
  echo "✅ 专用 Tab 已创建: $TAB（全程使用此 Tab，不影响你的其他页面）"
else
  echo "⚠️  无法创建新 Tab，继续使用现有 Tab: $TAB（请勿手动切换页面）"
fi

# ── Phase 1：抓取各板块列表，发现候选小区 ─────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Phase 1：发现候选小区"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ALL_CANDIDATES_JSON="$OUTDIR/all_candidates.json"
echo "[]" > "$ALL_CANDIDATES_JSON"

IFS=',' read -ra BOARD_LIST <<< "$BOARDS"
for board in "${BOARD_LIST[@]}"; do
  board=$(echo "$board" | tr -d ' ')
  echo ""
  echo "🗺  板块: $board"
  
  LIST_FILE="$OUTDIR/${board}_list.txt"
  # P0-1: 支持完整路径（含/）或简单板块名（自动拼接 district）
  if echo "$board" | grep -q '/'; then
    BOARD_URL="https://${CITY}.ke.com/xiaoqu/${board}/"
  else
    BOARD_URL="https://${CITY}.ke.com/xiaoqu/${DISTRICT}/${board}/"
  fi
  echo "   URL: $BOARD_URL"
  nav "$BOARD_URL"
  read_text > "$LIST_FILE"
  
  if check_captcha "$LIST_FILE"; then
    handle_captcha "$LIST_FILE" || continue
  fi
  
  SIZE=$(wc -c < "$LIST_FILE" | tr -d ' ')
  echo "   读取: ${SIZE} bytes"
  
  # 解析列表，添加板块信息
  RESULT=$(python3 -c "
import json, sys
sys.argv = ['parse_beike.py', 'region_list']
exec(open('$SCRIPT_DIR/parse_beike.py').read().replace('if __name__', 'if False'))
with open('$LIST_FILE') as f: text = f.read()
result = parse_region_list(text)
# 注入板块信息
for x in result['candidates']: x['board'] = '$board'
print(json.dumps(result, ensure_ascii=False))
" 2>/dev/null)
  
  COUNT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('filtered_count',0))" 2>/dev/null)
  TOTAL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_found',0))" 2>/dev/null)
  echo "   发现: ${TOTAL} 个小区，符合条件: ${COUNT} 个"
  
  # 打印候选
  echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('candidates', []):
    m = '🚇' + r['metro'] if r['metro'] else ''
    print(f\"   ✅ {r['name']} | {r['year']} | {r['price']//10000:.1f}万/㎡ | 在售{r['on_sale']}套 | 90天{r['sold_90d']}套 | {m}\")
" 2>/dev/null
  
  # 合并到总候选列表
  echo "$RESULT" | python3 -c "
import sys, json
new = json.load(sys.stdin).get('candidates', [])
with open('$ALL_CANDIDATES_JSON') as f: existing = json.load(f)
existing.extend(new)
with open('$ALL_CANDIDATES_JSON', 'w') as f: json.dump(existing, f, ensure_ascii=False, indent=2)
" 2>/dev/null
  
  sleep 5  # 板块间冷却
done

# 去重排序
python3 -c "
import json
with open('$ALL_CANDIDATES_JSON') as f: data = json.load(f)
# 按名称去重
seen = set()
unique = []
for x in data:
    if x['name'] not in seen:
        seen.add(x['name'])
        unique.append(x)
unique.sort(key=lambda x: (-x['sold_90d'], -x['on_sale'], x['price']))
with open('$ALL_CANDIDATES_JSON', 'w') as f: json.dump(unique, f, ensure_ascii=False, indent=2)
print(f'总候选小区: {len(unique)} 个（去重后）')
" 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 候选小区总排名"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import json
with open('$ALL_CANDIDATES_JSON') as f: data = json.load(f)
print(f'共 {len(data)} 个小区\n')
for i, r in enumerate(data, 1):
    m = r.get('metro', '')
    metro_s = f\"地铁{m}\" if m else '无地铁'
    print(f'{i:2}. [{r.get(\"board\",\"\")}] {r[\"name\"]} | {r[\"year\"]} | {r[\"price\"]//10000:.1f}万/㎡ | 在售{r[\"on_sale\"]}套 | 90天{r[\"sold_90d\"]}套 | {metro_s}')
" 2>/dev/null

# ── Phase 2：抓取详情（可选） ─────────────────────────────────────────────
DETAIL_DIR="$OUTDIR/details"
if [ "$DO_DETAIL" = true ]; then
  mkdir -p "$DETAIL_DIR"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🏠 Phase 2：抓取详情页"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  NAMES=$(python3 -c "
import json
with open('$ALL_CANDIDATES_JSON') as f: data = json.load(f)
for r in data: print(r['name'])
" 2>/dev/null)

  while IFS= read -r name; do
    [ -z "$name" ] && continue
    echo ""
    echo "  ── $name ──"
    
    # 找小区链接
    nav "https://${CITY}.ke.com/ershoufang/rs${name}/"
    XURL=$(get_xiaoqu_link | head -1)
    
    if [ -z "$XURL" ]; then
      echo "  ❌ 未找到小区链接，跳过"
      continue
    fi
    
    XID=$(echo "$XURL" | grep -oE '[0-9]+')
    echo "  ID: $XID"
    
    # 读小区详情
    nav "$XURL"
    DETAIL_FILE="$DETAIL_DIR/${name}_xiaoqu.txt"
    read_text > "$DETAIL_FILE"
    
    if check_captcha "$DETAIL_FILE"; then
      handle_captcha "$DETAIL_FILE" || continue
    fi
    
    # 解析
    python3 "$SCRIPT_DIR/parse_beike.py" xiaoqu < "$DETAIL_FILE" \
      > "$DETAIL_DIR/${name}_xiaoqu.json" 2>/dev/null
    
    # 更新候选列表中的小区ID
    python3 -c "
import json
with open('$ALL_CANDIDATES_JSON') as f: data = json.load(f)
for x in data:
    if x['name'] == '$name':
        x['xiaoqu_id'] = '$XID'
        x['detail_file'] = '${name}_xiaoqu.json'
        # 补充详情数据
        try:
            with open('$DETAIL_DIR/${name}_xiaoqu.json') as f2:
                detail = json.load(f2)
            x['building_type'] = detail.get('building_type', '')
            x['total_units']   = detail.get('total_units', '')
            x['far']           = detail.get('far', '')
            x['green_rate']    = detail.get('green_rate', '')
            x['mgmt_company']  = detail.get('mgmt_company', '')
            x['mgmt_fee']      = detail.get('mgmt_fee', '')
            x['views_30d']     = detail.get('views_30d', '')
        except: pass
        break
with open('$ALL_CANDIDATES_JSON', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
" 2>/dev/null
    
    SIZE=$(wc -c < "$DETAIL_FILE" | tr -d ' ')
    echo "  ✅ 详情: ${SIZE} bytes"
    sleep 10  # 冷却，减少验证码
    
  done <<< "$NAMES"
fi

# ── 导出 CSV ──────────────────────────────────────────────────────────────
CSV_FILE="$OUTDIR/candidates_$(date +%Y-%m-%d).csv"
python3 -c "
import json, csv
with open('$ALL_CANDIDATES_JSON') as f: data = json.load(f)

fields = ['小区名','板块','均价(元/㎡)','建年','最新建年','在售套数','90天成交','地铁',
          '建筑类型','总户数','容积率','绿化率','物业公司','物业费','30天带看','小区ID']
with open('$CSV_FILE', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in data:
        w.writerow({
            '小区名':      r.get('name',''),
            '板块':        r.get('board',''),
            '均价(元/㎡)': r.get('price',''),
            '建年':        r.get('year',''),
            '最新建年':    r.get('max_year',''),
            '在售套数':    r.get('on_sale',''),
            '90天成交':    r.get('sold_90d',''),
            '地铁':        r.get('metro',''),
            '建筑类型':    r.get('building_type',''),
            '总户数':      r.get('total_units',''),
            '容积率':      r.get('far',''),
            '绿化率':      r.get('green_rate',''),
            '物业公司':    r.get('mgmt_company',''),
            '物业费':      r.get('mgmt_fee',''),
            '30天带看':    r.get('views_30d',''),
            '小区ID':      r.get('xiaoqu_id',''),
        })
print(f'✅ CSV: $CSV_FILE')
" 2>/dev/null

# ── Phase 3：PAL MCP Consensus 评估（可选） ───────────────────────────────
if [ "$DO_CONSENSUS" = true ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🤖 Phase 3：PAL MCP 多模型 Consensus 评估"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  python3 "$SCRIPT_DIR/consensus_analyze.py" \
    --data-file "$ALL_CANDIDATES_JSON" \
    --output "$OUTDIR/consensus_report.md"
  
  echo ""
  echo "📄 Consensus 报告: $OUTDIR/consensus_report.md"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 完成！输出文件目录: $OUTDIR/"
echo "   候选清单: $ALL_CANDIDATES_JSON"
echo "   CSV:     $CSV_FILE"
[ "$DO_DETAIL" = true ] && echo "   详情数据: $DETAIL_DIR/"

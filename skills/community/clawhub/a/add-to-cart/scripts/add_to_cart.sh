#!/usr/bin/env bash
# =============================================================================
# add_to_cart.sh — 多平台搜索 + 加购物车/收藏脚本
# 用法:
#   搜索:   ./add_to_cart.sh <platform> <keyword> [sort]
#   收藏:   ./add_to_cart.sh pdd-fav <goods_id>    (拼多多商品收藏)
#   详情页: ./add_to_cart.sh detail <platform> <url> (导航到商品详情)
#
# platform: taobao | jd | pdd | xianyu
# keyword:  搜索关键词
# sort:     price-asc | price-desc | sale-desc | default (默认: default)
#
# ⚠️ 不涉及支付，只做到加购物车/收藏为止。
# =============================================================================

set -euo pipefail

# ── 配置 ─────────────────────────────────────────────────────────────────────
BRAVE_AGENT_DIR="$HOME/.openclaw/groups/workspace-oc_96ba3f8c3476edac2fb64ee89f842f4e/skills/brave-browser-agent"
CDP_SCRIPT="$BRAVE_AGENT_DIR/scripts/cdp_exec.py"
WAIT_SECONDS=5
MAX_CHARS=8000

# ── 通用函数 ──────────────────────────────────────────────────────────────────

# 从CDP获取第一个可用tab ID
get_tab_id() {
  local tab_list
  tab_list=$(python3 "$CDP_SCRIPT" list 2>&1) || {
    echo "❌ 无法连接 Brave 浏览器 CDP"
    echo "   请确认 Brave 已以 --remote-debugging-port=9222 启动"
    exit 1
  }
  
  local tab_id
  tab_id=$(echo "$tab_list" | grep -oE 'tab_id=[^ ]+' | head -1 | cut -d= -f2 || echo "")
  
  if [[ -z "$tab_id" ]]; then
    tab_id=$(echo "$tab_list" | python3 -c "
import sys, json, re
try:
    data = json.load(sys.stdin)
    if isinstance(data, list) and len(data) > 0:
        print(data[0].get('id', ''))
    elif isinstance(data, dict):
        tabs = data.get('tabs', data.get('result', []))
        if tabs:
            print(tabs[0].get('id', ''))
except:
    text = sys.stdin.read() if hasattr(sys.stdin, 'read') else str(data)
    m = re.search(r'[\"\\']([A-F0-9]+)[\"\\']', text)
    if m: print(m.group(1))
" 2>/dev/null || echo "")
  fi
  
  echo "$tab_id"
}

# 导航到指定URL
navigate_to_url() {
  local target_url="$1"
  local tab_id="$2"
  
  python3 "$CDP_SCRIPT" eval "$tab_id" "window.location.href = '$target_url'" 2>&1
}

# ── 帮助信息 ─────────────────────────────────────────────────────────────────
usage() {
  cat <<'EOF'
用法:
  ./add_to_cart.sh <platform> <keyword> [sort]        搜索商品
  ./add_to_cart.sh pdd-fav <goods_id>                 拼多多商品收藏
  ./add_to_cart.sh detail <platform> <url>            导航到商品详情页

平台 (platform):
  taobao   淘宝
  jd       京东
  pdd      拼多多 (移动版页面)
  xianyu   闲鱼 (goofish.com)

排序 (sort):
  default    综合排序 (默认)
  price-asc  价格从低到高
  price-desc 价格从高到低
  sale-desc  销量从高到低

示例:
  ./add_to_cart.sh taobao "牛奶"
  ./add_to_cart.sh jd "耳机" price-asc
  ./add_to_cart.sh pdd "纸巾" sale-desc
  ./add_to_cart.sh pdd-fav 753946420431             # 拼多多收藏商品
  ./add_to_cart.sh detail taobao "https://item.taobao.com/item.htm?id=xxx"

⚠️ 前置要求:
  1. Brave 浏览器以 --remote-debugging-port=9222 启动
  2. brave-browser-agent skill 已安装
  3. 淘宝/拼多多/闲鱼需提前在浏览器中登录
EOF
  exit 1
}

# ── 参数校验 ─────────────────────────────────────────────────────────────────
if [[ $# -lt 2 ]]; then
  usage
fi

PLATFORM="$1"
KEYWORD="$2"
SORT="${3:-default}"

# ── 特殊模式检查 ──────────────────────────────────────────────────────────
if [[ "$PLATFORM" == "pdd-fav" ]]; then
  # 拼多多收藏模式: ./add_to_cart.sh pdd-fav <goods_id>
  GOODS_ID="$KEYWORD"
  URL="https://mobile.yangkeduo.com/goods1.html?goods_id=${GOODS_ID}"
  echo "═══════════════════════════════════════════════════"
  echo "⭐ 拼多多商品收藏"
  echo "═══════════════════════════════════════════════════"
  echo "  商品ID: $GOODS_ID"
  echo "  URL:    $URL"
  echo "═══════════════════════════════════════════════════"
  
  # 获取tab ID
  TAB_ID=$(get_tab_id)
  echo "📌 使用 tab: $TAB_ID"
  
  # 导航到商品详情页
  navigate_to_url "$URL" "$TAB_ID"
  sleep $WAIT_SECONDS
  
  # 提取商品信息
  echo ""
  echo "📄 商品详情..."
  python3 "$CDP_SCRIPT" eval "$TAB_ID" "document.body.innerText.substring(0, ${MAX_CHARS})" 2>&1
  
  # 截图
  python3 "$CDP_SCRIPT" screenshot "$TAB_ID" /tmp/pdd_goods.png 2>/dev/null || true
  
  # 点击"收藏"按钮（已验证方法）
  echo ""
  echo "⭐ 正在收藏..."
  FAV_RESULT=$(python3 "$CDP_SCRIPT" eval "$TAB_ID" \
    "(function(){
      var spans = document.querySelectorAll('span');
      for(var i=0; i<spans.length; i++){
        if(spans[i].innerText === '收藏'){
          spans[i].scrollIntoView({behavior: 'instant', block: 'center'});
          setTimeout(function(){ spans[i].click(); }, 500);
          return '找到收藏按钮，正在点击...';
        }
      }
      return '未找到收藏按钮';
    })()" 2>&1)
  echo "  结果: $FAV_RESULT"
  
  sleep 2
  
  # 验证
  CONFIRM=$(python3 "$CDP_SCRIPT" eval "$TAB_ID" \
    "(function(){
      var spans = document.querySelectorAll('span');
      for(var i=0; i<spans.length; i++){
        if(spans[i].innerText === '已收藏'){
          return '✅ 收藏成功！';
        }
      }
      return '⚠️ 收藏验证未通过';
    })()" 2>&1)
  echo "  验证: $CONFIRM"
  
  echo ""
  echo "💡 打开拼多多App → 收藏夹即可查看"
  exit 0
fi

if [[ "$PLATFORM" == "detail" ]]; then
  # 导航到商品详情页模式: ./add_to_cart.sh detail <platform> <url>
  DETAIL_PLATFORM="$KEYWORD"
  DETAIL_URL="${3:-}"
  if [[ -z "$DETAIL_URL" ]]; then
    echo "❌ 缺少商品详情页URL"
    exit 1
  fi
  URL="$DETAIL_URL"
  PLATFORM="$DETAIL_PLATFORM"
  echo "═══════════════════════════════════════════════════"
  echo "🔗 导航到商品详情页"
  echo "═══════════════════════════════════════════════════"
  echo "  平台: $PLATFORM"
  echo "  URL:  $URL"
  echo "═══════════════════════════════════════════════════"
  
  TAB_ID=$(get_tab_id)
  echo "📌 使用 tab: $TAB_ID"
  
  navigate_to_url "$URL" "$TAB_ID"
  sleep $WAIT_SECONDS
  python3 "$CDP_SCRIPT" screenshot "$TAB_ID" /tmp/detail.png 2>/dev/null || true
  exit 0
fi

# ── URL编码 ──────────────────────────────────────────────────────────────────
url_encode() {
  local raw="$1"
  # 使用 python3 做URL编码（兼容性最好）
  python3 -c "import urllib.parse; print(urllib.parse.quote('$raw'))" 2>/dev/null || \
  python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$raw"
}

ENCODED_KW=$(url_encode "$KEYWORD")

# ── 平台配置 ─────────────────────────────────────────────────────────────────
declare -A SEARCH_URLS SORT_PARAMS NAMES

# 搜索URL模板
SEARCH_URLS[taobao]="https://s.taobao.com/search?q=${ENCODED_KW}"
SEARCH_URLS[jd]="https://search.jd.com/Search?keyword=${ENCODED_KW}"
SEARCH_URLS[pdd]="https://mobile.yangkeduo.com/search_result.html?search_key=${ENCODED_KW}"
SEARCH_URLS[xianyu]="https://www.goofish.com/search?q=${ENCODED_KW}"

# 排序参数
SORT_PARAMS[taobao]="&sort="
SORT_PARAMS[jd]="&psort="
SORT_PARAMS[pdd]="&sort="
SORT_PARAMS[xianyu]="&sort="

# 平台中文名
NAMES[taobao]="淘宝"
NAMES[jd]="京东"
NAMES[pdd]="拼多多"
NAMES[xianyu]="闲鱼"

# 排序值映射
sort_value() {
  local platform="$1" sort="$2"
  case "$platform" in
    taobao)
      case "$sort" in
        price-asc)  echo "price-asc" ;;
        price-desc) echo "price-desc" ;;
        sale-desc)  echo "sale-desc" ;;
        *)          echo "default" ;;
      esac
      ;;
    jd)
      case "$sort" in
        price-asc)  echo "3" ;;
        price-desc) echo "4" ;;
        sale-desc)  echo "5" ;;
        *)          echo "0" ;;
      esac
      ;;
    pdd)
      case "$sort" in
        price-asc)  echo "price-asc" ;;
        price-desc) echo "price-desc" ;;
        sale-desc)  echo "sale-desc" ;;
        *)          echo "default" ;;
      esac
      ;;
    xianyu)
      # 闲鱼排序支持有限
      echo ""
      ;;
  esac
}

# ── 验证平台 ─────────────────────────────────────────────────────────────────
if [[ -z "${SEARCH_URLS[$PLATFORM]:-}" ]]; then
  echo "❌ 不支持的平台: $PLATFORM"
  echo "   支持的平台: taobao, jd, pdd, xianyu"
  exit 1
fi

# ── 构建完整URL ──────────────────────────────────────────────────────────────
SV=$(sort_value "$PLATFORM" "$SORT")
URL="${SEARCH_URLS[$PLATFORM]}"
if [[ -n "$SV" && "$SV" != "default" && "$SV" != "0" ]]; then
  URL="${URL}${SORT_PARAMS[$PLATFORM]}${SV}"
fi

echo "═══════════════════════════════════════════════════"
echo "🛒 多平台商品搜索"
echo "═══════════════════════════════════════════════════"
echo "  平台:   ${NAMES[$PLATFORM]} ($PLATFORM)"
echo "  关键词: $KEYWORD"
echo "  排序:   $SORT"
echo "  URL:    $URL"
echo "═══════════════════════════════════════════════════"

# ── 检查CDP脚本 ──────────────────────────────────────────────────────────────
if [[ ! -f "$CDP_SCRIPT" ]]; then
  echo "❌ 找不到 CDP 脚本: $CDP_SCRIPT"
  echo "   请确认 brave-browser-agent skill 已安装"
  exit 1
fi

# ── 获取 tab ID ──────────────────────────────────────────────────────
TAB_ID=$(get_tab_id)
echo "📌 使用 tab: $TAB_ID"

# ── 导航到搜索页 ─────────────────────────────────────────────────────────────
echo ""
echo "🔍 正在打开搜索页..."
NAV_RESULT=$(navigate_to_url "$URL" "$TAB_ID")
echo "   导航结果: $NAV_RESULT"

# ── 等待加载 ─────────────────────────────────────────────────────────────────
echo ""
echo "⏳ 等待 ${WAIT_SECONDS} 秒加载页面..."
sleep "$WAIT_SECONDS"

# ── 提取搜索结果 ─────────────────────────────────────────────────────────────
echo ""
echo "📄 提取搜索结果..."
RESULT=$(python3 "$CDP_SCRIPT" eval "$TAB_ID" "document.body.innerText.substring(0, $MAX_CHARS)" 2>&1)

echo "═══════════════════════════════════════════════════"
echo "🔍 ${NAMES[$PLATFORM]} 搜索结果: \"$KEYWORD\""
echo "═══════════════════════════════════════════════════"
echo "$RESULT"
echo "═══════════════════════════════════════════════════"
echo ""
echo "💡 下一步:"
echo "   1. 从上面的结果中找到目标商品"
echo "   2. 用 cdp_exec.py 进入商品详情页"
echo "   3. 选择规格（如有）"
echo "   4. 点击加入购物车/收藏按钮"
echo ""
echo "   ⚠️ 加购物车/收藏操作需根据实际页面调整选择器"
echo "   参考: references/platform-selectors.md"

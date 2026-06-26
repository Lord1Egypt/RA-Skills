#!/bin/bash
# 公司平台接口 — Token 自动管理（支持账号密码登录）
# 用法: ./api.sh <endpoint> [参数...]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/.api-config.json"
TOKEN_FILE="$SKILL_DIR/.token-cache.json"
API_BASE=""  # 运行时从配置读取

# ===== 初次配置 =====
if [ ! -f "$CONFIG_FILE" ]; then
  echo ""
  echo "========================================"
  echo "  🔧 陀螺匠 · 公司平台接口 首次配置"
  echo "========================================"
  echo ""
  echo "请运行 setup 命令进行配置："
  echo "  $0 setup"
  echo ""
  echo "或者手动创建 $CONFIG_FILE"
  cat << 'REF'
{
  "base_url": "你的API地址",
  "access_key": "你的开放平台 access_key",
  "secret_key": "你的开放平台 secret_key",
  "account": "你的登录手机号",
  "password": "你的登录密码"
}
REF
  echo ""
  exit 1
fi

# ===== 读取配置 =====
load_config() {
  ACCOUNT=$(jq -r '.account // ""' "$CONFIG_FILE")
  PASSWORD=$(jq -r '.password // ""' "$CONFIG_FILE")
}

# ===== Token：开放平台 =====
get_open_token() {
  local base_url ak sk
  base_url=$(jq -r '.base_url' "$CONFIG_FILE")
  ak=$(jq -r '.access_key' "$CONFIG_FILE")
  sk=$(jq -r '.secret_key' "$CONFIG_FILE")

  if [ -f "$TOKEN_FILE" ]; then
    local exp t
    exp=$(jq -r '.open_token.expires_at // 0' "$TOKEN_FILE")
    t=$(jq -r '.open_token.token // ""' "$TOKEN_FILE")
    if [ "$(date +%s)" -lt "$exp" ] && [ -n "$t" ]; then echo "$t"; return 0; fi
  fi

  local r; r=$(curl -s -X POST "$base_url/open/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"access_key\":\"$ak\",\"secret_key\":\"$sk\"}")
  local s; s=$(echo "$r" | jq -r '.status')
  if [ "$s" = "200" ]; then
    local nt ei; nt=$(echo "$r" | jq -r '.data.token'); ei=$(echo "$r" | jq -r '.data.expires_in')
    local ea=$(( $(date +%s) + ei - 300 ))
    local tmp; tmp=$(mktemp)
    if [ -f "$TOKEN_FILE" ]; then
      jq --arg t "$nt" --argjson e "$ea" '.open_token={"token":$t,"expires_at":$e}' "$TOKEN_FILE" > "$tmp"
    else
      echo "{\"open_token\":{\"token\":\"$nt\",\"expires_at\":$ea}}" > "$tmp"
    fi
    mv "$tmp" "$TOKEN_FILE"
    echo "$nt"
  else
    echo "OPEN_TOKEN_ERR" >&2; return 1
  fi
}

# ===== Token：用户登录（账号密码→Token）=====
do_login() {
  local api_base; api_base=$(jq -r '.base_url // ""' "$CONFIG_FILE" 2>/dev/null)
  load_config
  local r; r=$(curl -s -X POST "${api_base}/ent/user/login" \
    -H "accept: application/json" -H "content-type: application/json" \
    -H "user-agent: Mozilla/5.0" \
    -d "{\"account\":\"$ACCOUNT\",\"password\":\"$PASSWORD\"}")
  local s; s=$(echo "$r" | jq -r '.status')
  if [ "$s" = "200" ]; then
    local nt ei; nt=$(echo "$r" | jq -r '.data.token'); ei=$(echo "$r" | jq -r '.data.expires_in')
    local ea=$(( $(date +%s) + ei - 300 ))
    local tmp; tmp=$(mktemp)
    if [ -f "$TOKEN_FILE" ]; then
      jq --arg t "$nt" --argjson e "$ea" '.user_token={"token":$t,"expires_at":$e}' "$TOKEN_FILE" > "$tmp"
    else
      echo "{\"user_token\":{\"token\":\"$nt\",\"expires_at\":$ea}}" > "$tmp"
    fi
    mv "$tmp" "$TOKEN_FILE"
    echo "✅ 登录成功，Token过期: $(date -d @$ea '+%Y-%m-%d %H:%M:%S')" >&2
    echo "$nt"
  else
    echo "LOGIN_FAILED: $r" >&2; return 1
  fi
}

# ===== Token：获取用户Token（自动登录）=====
get_user_token() {
  if [ -f "$TOKEN_FILE" ]; then
    local exp t
    exp=$(jq -r '.user_token.expires_at // 0' "$TOKEN_FILE")
    t=$(jq -r '.user_token.token // ""' "$TOKEN_FILE")
    if [ "$(date +%s)" -lt "$exp" ] && [ -n "$t" ] && [ "$t" != "null" ]; then
      echo "$t"; return 0
    fi
  fi
  # Token过期，自动登录
  echo "🔄 Token过期，自动登录..." >&2
  do_login
}

# ===== 通用请求 =====
# ===== 通用请求（自动处理Token过期重试）=====
api_get() {
  local ep="$1" q="$2" t result
  t=$(get_user_token 2>/dev/null) || t=$(do_login 2>/dev/null) || return 1
  result=$(curl -s "$(jq -r ".base_url" "$CONFIG_FILE" 2>/dev/null)${ep}?${q}" -H "accept: application/json" \
    -H "authorization: Bearer $t" -H "user-agent: Mozilla/5.0")
  # Token过期则重新登录重试
  if echo "$result" | jq -e '.status == 410003 or (.message // "") | test("Login expired|登录过期")' >/dev/null 2>&1; then
    t=$(do_login 2>/dev/null) || return 1
    curl -s "$(jq -r ".base_url" "$CONFIG_FILE" 2>/dev/null)${ep}?${q}" -H "accept: application/json" \
      -H "authorization: Bearer $t" -H "user-agent: Mozilla/5.0"
  else
    echo "$result"
  fi
}

api_post() {
  local ep="$1" body="$2" t result
  t=$(get_user_token 2>/dev/null) || t=$(do_login 2>/dev/null) || return 1
  result=$(curl -s -X POST "$(jq -r ".base_url" "$CONFIG_FILE" 2>/dev/null)${ep}" \
    -H "accept: application/json" -H "content-type: application/json" \
    -H "authorization: Bearer $t" -H "user-agent: Mozilla/5.0" -d "$body")
  # Token过期则重新登录重试
  if echo "$result" | jq -e '.status == 410003 or (.message // "") | test("Login expired|登录过期")' >/dev/null 2>&1; then
    t=$(do_login 2>/dev/null) || return 1
    curl -s -X POST "$(jq -r ".base_url" "$CONFIG_FILE" 2>/dev/null)${ep}" \
      -H "accept: application/json" -H "content-type: application/json" \
      -H "authorization: Bearer $t" -H "user-agent: Mozilla/5.0" -d "$body"
  else
    echo "$result"
  fi
}

# ===== 接口：日报 =====
cmd_daily() {
  local p="${1:-1}" l="${2:-15}" t="${3:-2026/05/01-2026/05/31}" uid="${4:-}" sc="${5:-all}"
  t=$(echo "$t" | sed 's/\//%2F/g')
  api_get "/ent/daily" "page=$p&limit=$l&type=1&types=0&time=$t&user_id=$uid&scope_frame=$sc&sort_value=&sort_field="
}

# ===== 接口：项目列表 =====
cmd_projects() {
  local p="${1:-1}" l="${2:-15}" types="${3:-0}" st="${4:-}" sc="${5:-all}" nm="${6:-0}"
  api_get "/ent/program" "page=$p&limit=$l&types=$types&status=$st&scope_frame=$sc&scope_normal=$nm"
}

# ===== 接口：财务/账单 =====

# ===== 接口：客户列表 =====

# ===== 接口：合同列表 =====

# ===== 接口：产品列表 =====

# ===== 接口：添加产品 =====
cmd_product_add() {
  local name="${1}" path="${2:-3}" unit="${3:-套}"
  local body; body=$(printf '{"name":"%s","path":[%s],"unit_name":"%s","types":"1","number":"%s","is_show":"1","description":"<p>%s</p>","sort":1,"spec_type":0,"attr":[],"attrValue":[]}' "$name" "$path" "$unit" "$(date +%Y%m%d%H%M%S)" "$name")
  api_post "/ent/client/products" "$body"
}
cmd_products() {
  local p="${1:-1}" l="${2:-15}" types="${3:-product}"
  local body; body=$(printf '{"page":%d,"limit":%d,"types":"%s","sort_field":"created_at","sort_value":"desc","view_search":""}' "$p" "$l" "$types")
  api_post "/ent/client/products/list" "$body"
}
cmd_contracts() {
  local p="${1:-1}" l="${2:-15}"
  local body; body=$(printf '{"page":%d,"limit":%d,"view_search":1,"sort_field":"created_at","sort_value":"desc"}' "$p" "$l")
  api_post "/ent/client/contracts/list" "$body"
}
cmd_customers() {
  local p="${1:-1}" l="${2:-15}" types="${3:-customer}"
  local body; body=$(printf '{"page":%d,"limit":%d,"sort_field":"created_at","sort_value":"desc","view_search":1,"types":"%s"}' "$p" "$l" "$types")
  api_post "/ent/client/customer/list" "$body"
}
cmd_bills() {
  local p="${1:-1}" l="${2:-15}" sort="${3:-id}" types="${4:-}" time="${5:-2026/05/01-2026/05/31}"
  local body; body=$(printf '{"page":%d,"limit":%d,"sort":"%s","types":"%s","time":"%s"}' "$p" "$l" "$sort" "$types" "$time")
  api_post "/ent/bill/list" "$body"
}


# ===== 接口：合同创建页数据（拿客户ID、分类ID）=====
cmd_contract_form() {
  local odds="${1}" eid="${2}"
  api_get "/ent/client/contracts/create" "odds_id=$odds&eid=$eid"
}

# ===== 接口：产品属性/SKU（拿unique ID用于签合同）=====
cmd_product_attrs() {
  local p="${1:-1}" l="${2:-10}" pid="${3:-}" name="${4:-}" attr="${5:-}"
  api_get "/ent/client/products/attrs" "page=$p&limit=$l&pid=$pid&name=$name&attr=$attr"
}


# ===== 接口：创建项目 =====
cmd_project_add() {
  local name="${1}" eid="${2}" cid="${3}" uid="${4:-7}" start="${5:-$(date +%Y-%m-%d)}" end="${6:-$(date -d '+5 days' +%Y-%m-%d)}"
  local body
  # 从配置读取管理员模板
  local admin_template
  admin_template=$(jq -r '.admin_template // empty' "$CONFIG_FILE" 2>/dev/null)
  if [ -z "$admin_template" ]; then
    admin_template=$(jq -r ".admin_template // empty" "$CONFIG_FILE" 2>/dev/null)
  if [ -z "$admin_template" ]; then
    echo "⚠️  请先在配置文件中设置 admin_template（管理员模板）" >&2
    echo "   或者运行 setup 重新配置" >&2
    return 1
  fi
  fi
  body=$(python3 -c "
import json, sys
adm = json.loads('$admin_template')
# 更新uid和value为用户选择的值
adm['value'] = $uid
d = {
    'status': 0,
    'cid': $cid,
    'name': '$name',
    'uid': $uid,
    'admins': [adm],
    'members': [5, 7],
    'start_date': '$start',
    'end_date': '$end',
    'eid': $eid,
    'describe': ''
}
print(json.dumps(d, ensure_ascii=False))
")
  api_post "/ent/program" "$body"
}

# ===== 接口：产品分类 =====
cmd_product_cate() {
  api_get "/ent/client/product/cate" ""
}


# ===== 接口：项目详情（含成员、客户）=====
cmd_project_info() {
  local id="${1}"
  api_get "/ent/program/info/$id" ""
}

# ===== 接口：创建项目任务 =====
cmd_task_add() {
  local pid="${1}" name="${2}" uid="${3:-7}" start="${4:-$(date +%Y-%m-%d)}" end="${5:-$(date -d '+5 days' +%Y-%m-%d)}"
  local body; body=$(python3 -c "
import json
d = {'program_id': $pid, 'pid': 0, 'name': '$name', 'uid': $uid,
     'plan_start': '$start', 'plan_end': '$end', 'status': 0,
     'describe': '<p>自动创建</p>', 'members': []}
print(json.dumps(d, ensure_ascii=False))
")
  api_post "/ent/program_task" "$body"
}

# ===== 接口：交互式配置 =====
cmd_setup() {
  if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件已存在: $CONFIG_FILE"
    echo "   如需重新配置，请先删除后再运行 setup"
    exit 1
  fi

  echo ""
  echo "========================================"
  echo "  🔧 陀螺匠 · 公司平台接口 配置向导"
  echo "========================================"
  echo ""

  read -p "接口地址（如 https://yourdomain.com/api）: " base_url
  base_url="${base_url}"
  while [ -z "$base_url" ]; do
    read -p "接口地址不能为空，请重新输入: " base_url
  done

  read -p "开放平台 access_key: " ak
  read -p "开放平台 secret_key: " sk
  read -p "登录手机号: " acct
  read -s -p "登录密码: " pwd
  echo ""

  echo ""
  echo "正在验证...请稍候"

  # 先尝试开放平台登录
  local r; r=$(curl -s -X POST "$base_url/open/auth/login"     -H "Content-Type: application/json"     -d "{"access_key":"$ak","secret_key":"$sk"}")
  local s; s=$(echo "$r" | jq -r '.status')
  if [ "$s" = "200" ]; then
    echo "✅ 开放平台验证通过"
  else
    echo "⚠️  开放平台验证失败，请检查 key"
  fi

  # 尝试用户登录
  r=$(curl -s -X POST "$base_url/ent/user/login"     -H "accept: application/json" -H "content-type: application/json"     -H "user-agent: Mozilla/5.0"     -d "{"account":"$acct","password":"$pwd"}")
  s=$(echo "$r" | jq -r '.status')
  if [ "$s" = "200" ]; then
    echo "✅ 用户登录验证通过"
  else
    echo "❌ 用户登录失败: $(echo "$r" | jq -r '.message')"
    exit 1
  fi

  # 保存配置
  cat > "$CONFIG_FILE" << EOF
{
  "base_url": "$base_url",
  "access_key": "$ak",
  "secret_key": "$sk",
  "account": "$acct",
  "password": "$pwd"
}
EOF
  echo ""
  echo "✅ 配置已保存到: $CONFIG_FILE"
  echo "   现在可以正常使用各接口了"
}

# ===== 主入口 =====
CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
  setup)       cmd_setup ;;
  auth)        get_open_token ;;
  login)       do_login ;;
  save-token)
    TOK="${1}" EXPR="${2:-86400}"
    EA=$(( $(date +%s) + EXPR ))
    TMPF=$(mktemp)
    if [ -f "$TOKEN_FILE" ]; then
      jq --arg t "$TOK" --argjson e "$EA" '.user_token={"token":$t,"expires_at":$e}' "$TOKEN_FILE" > "$TMPF"
    else
      echo "{\"user_token\":{\"token\":\"$TOK\",\"expires_at\":$EA}}" > "$TMPF"
    fi
    mv "$TMPF" "$TOKEN_FILE"
    echo "✅ Token已保存，过期: $(date -d @$EA '+%Y-%m-%d %H:%M:%S')"
    ;;
  daily)       cmd_daily "$@" ;;
  projects)    cmd_projects "$@" ;;
  bills)       cmd_bills "$@" ;;
  customers)   cmd_customers "$@" ;;
  contracts)   cmd_contracts "$@" ;;
  products)    cmd_products "$@" ;;
  product-attrs) cmd_product_attrs "$@" ;;
  product-cate)  cmd_product_cate "$@" ;;
  project-info)  cmd_project_info "$@" ;;
  project-add)   cmd_project_add "$@" ;;
  task-add)      cmd_task_add "$@" ;;
  contract-form) cmd_contract_form "$@" ;;
  product-add)   cmd_product_add "$@" ;;
  product-add) cmd_product_add "$@" ;;
  status)
    echo "=== Token 状态 ==="
    if [ -f "$TOKEN_FILE" ]; then
      echo "开放平台: $(jq -r '.open_token.token[:20] + "..."' "$TOKEN_FILE" 2>/dev/null || echo '无')"
      echo "过期: $(jq -r '.open_token.expires_at | strftime("%Y-%m-%d %H:%M:%S")' "$TOKEN_FILE" 2>/dev/null || echo '无')"
      echo "用户Token: $(jq -r '.user_token.token[:20] + "..."' "$TOKEN_FILE" 2>/dev/null || echo '未设置')"
      echo "过期: $(jq -r '.user_token.expires_at | strftime("%Y-%m-%d %H:%M:%S")' "$TOKEN_FILE" 2>/dev/null || echo '无')"
    else
      echo "未初始化"
    fi
    ;;
  help|*)
    echo "用法: $0 <命令> [参数]"
    echo "命令: setup | auth | login | save-token <token> | daily | projects | project-info <id> | project-add | task-add | bills | customers | contracts | contract-form | products | product-add | product-attrs | product-cate | status"
    ;;
esac

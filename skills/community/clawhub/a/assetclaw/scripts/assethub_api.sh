#!/usr/bin/env bash
set -euo pipefail

# AssetClaw Direct API Helper Script (v1.7.0)
# 用法: bash scripts/assethub_api.sh <command> [args...]
#
# v1.7.0 增量升级（2026-07-29，基于 backend swagger 101 模块 / 1,809 ops 同步）：
#   - 新增 domains / stats / redirects 命令（基于 15 业务域分组）
#   - 新增旧路径 → 新路径 自动警告（warn_deprecated_path）
#   - 新增 IoT token 注入（ASSETHUB_IOT_TOKEN）
#   - 新增 ASSETHUB_HIGH_RISK_CONFIRM 显式控制高风险重放（默认 OFF）
#   - 新增 Idempotency-Key 可由 ASSETHUB_IDEMPOTENCY_KEY 注入（自动生成仍为默认）
#   - 保留 v1.6.0 的全部能力（login/logout/session/set-tenant/login_from_temp_session/
#     自动 401 重登、两段式 X-Risk-Confirm-Token 重放、临时凭证文件支持）
#
# 与 references/api-modules-overview.md / references/auth-and-workflows.md /
# references/endpoint-quick-ref.md 协同使用。

API_URL="${ASSETHUB_API_URL:-http://localhost:13579/api}"
SESSION_FILE="${ASSETHUB_SESSION_FILE:-/tmp/assethub-claw-session.json}"
TEMP_SESSION_FILE="/tmp/assethub-claw-temp-session.json"
TEMP_SESSION_FILE="/tmp/assethub-claw-temp-session.json"

# 旧路径 → 新路径 映射（v1.7.0 加入：仅警告，不强制替换）
PATH_OLD_KEYS=(
  "maintenance"
  "adverse-events"
  "transfer"
  "assets/transfer-requests"
  "compliance/special-equipment"
  "compliance/staff-qualification"
  "compliance/uptime-statistics"
  "compliance/safety-inspection"
  "iot-devices"
  "asset-location"
  "asset-images"
  "asset-labels"
  "procurement"
  "acceptance"
  "ai"
  "chat"
  "asset-ai-analysis"
  "asset-depreciation"
  "sms-verification"
)
PATH_NEW_VALUES=(
  "maintenance-management"
  "adverse-reaction"
  "asset-allocation"
  "asset-allocation"
  "key-equipment"
  "staff"
  "uptime"
  "safety-inspection"
  "iot/devices"
  "iot/locations"
  "assets/images"
  "assets/labels"
  "tendering/procurement-requests"
  "acceptance-management"
  "asset-ai-assistant"
  "asset-ai-assistant"
  "asset-ai-assistant"
  "depreciation"
  "(removed)"
)

warn_deprecated_path() {
  local target="$1"
  local stripped="${target#/api}"
  stripped="${stripped#/}"
  local first_segment="${stripped%%/*}"
  local i
  for ((i = 0; i < ${#PATH_OLD_KEYS[@]}; i++)); do
    local old="${PATH_OLD_KEYS[$i]}"
    local new="${PATH_NEW_VALUES[$i]}"
    if [[ "$stripped" == "$old" || "$stripped" == "$old/"* || "$first_segment" == "$old" ]]; then
      echo "⚠️  DEPRECATED PATH: /api/$old → use /api/$new" >&2
      return 0
    fi
  done
  return 1
}

high_risk_confirm_enabled() {
  local value="${ASSETHUB_HIGH_RISK_CONFIRM:-}"
  case "$value" in
    YES|yes|true|TRUE|1)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

print_help() {
  cat <<'EOF'
AssetClaw Direct API Helper (v1.7.0)

Usage:
  bash scripts/assethub_api.sh login
  bash scripts/assethub_api.sh logout
  bash scripts/assethub_api.sh session
  bash scripts/assethub_api.sh set-tenant <序号>
  bash scripts/assethub_api.sh modules
  bash scripts/assethub_api.sh module <path>
  bash scripts/assethub_api.sh endpoints
  bash scripts/assethub_api.sh domains                # v1.7.0 新增
  bash scripts/assethub_api.sh stats                  # v1.7.0 新增
  bash scripts/assethub_api.sh redirects              # v1.7.0 新增
  bash scripts/assethub_api.sh request <METHOD> <PATH> [JSON_BODY]

Environment:
  ASSETHUB_API_URL           API基础地址 (默认: http://localhost:13579/api)
  ASSETHUB_API_USERNAME      登录用户名
  ASSETHUB_API_PASSWORD      登录密码
  ASSETHUB_TENANT_ID         显式租户ID（super_admin 跨租户必填）
  ASSETHUB_SESSION_FILE      会话缓存文件 (默认: /tmp/assethub-claw-session.json)
  ASSETHUB_IDEMPOTENCY_KEY   写操作幂等键（v1.7.0 新增，留空则自动生成）
  ASSETHUB_HIGH_RISK_CONFIRM YES|true|1 仅用于 428 二次重放（v1.7.0 新增，默认 OFF）
  ASSETHUB_IOT_TOKEN         IoT ingest 路径专用 token（v1.7.0 新增，可选）

Examples:
  # 登录
  bash scripts/assethub_api.sh login

  # 列出所有模块
  bash scripts/assethub_api.sh modules

  # 查看 assets 模块接口
  bash scripts/assethub_api.sh module assets

  # GET 请求
  bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20"

  # POST 请求
  bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" \
    '{"asset_code":"A001","fault_description":"无法开机","issue_description":"无法开机","source":"assetclaw","intent":"repair_request"}'

  # PUT 请求
  bash scripts/assethub_api.sh request PUT "/assets/123" \
    '{"asset_name":"新名称"}'

  # DELETE 请求
  bash scripts/assethub_api.sh request DELETE "/assets/123"
EOF
}

normalize_url() {
  local raw="${1:-/}"
  raw="${raw## }"
  raw="${raw%% }"

  if [[ "$raw" =~ ^https?:// ]]; then
    printf '%s\n' "$raw"
    return
  fi

  if [[ "$raw" != /* ]]; then
    raw="/$raw"
  fi

  # 避免重复 /api
  if [[ "$raw" == /api/* ]]; then
    raw="${raw:4}"
  fi

  printf '%s%s\n' "${API_URL%/}" "$raw"
}

read_session_field() {
  local field="$1"
  SESSION_FILE="$SESSION_FILE" FIELD_NAME="$field" node <<'NODE'
const fs = require('node:fs');
const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
const fieldName = process.env.FIELD_NAME;

if (!fs.existsSync(sessionFile)) process.exit(1);
const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
const value = session[fieldName];
if (value === undefined || value === null) process.exit(1);
process.stdout.write(String(value));
NODE
}

login() {
  local username="${ASSETHUB_API_USERNAME:-}"
  local password="${ASSETHUB_API_PASSWORD:-}"

  # 如果未设置环境变量，尝试从临时会话文件读取凭证
  if [[ -z "$username" || -z "$password" ]]; then
    if [[ -f "$TEMP_SESSION_FILE" ]]; then
      username="$(node -e "
const fs=require('fs');const s=JSON.parse(fs.readFileSync('$TEMP_SESSION_FILE','utf8'));
process.stdout.write(s.username||'');" 2>/dev/null || true)"
      password="$(node -e "
const fs=require('fs');const s=JSON.parse(fs.readFileSync('$TEMP_SESSION_FILE','utf8'));
process.stdout.write(s.password||'');" 2>/dev/null || true)"
    fi
  fi

  if [[ -z "$username" || -z "$password" ]]; then
    echo "Missing ASSETHUB_API_USERNAME or ASSETHUB_API_PASSWORD" >&2
    echo "请设置环境变量: export ASSETHUB_API_USERNAME=<用户名>" >&2
    echo "                 export ASSETHUB_API_PASSWORD=<密码>" >&2
    exit 1
  fi

  local response
  response="$(curl -sS -X POST "$(normalize_url /users/login)" \
    -H 'Content-Type: application/json' \
    --data-binary "{\"username\":\"${username}\",\"password\":\"${password}\"}")"

  RESPONSE_JSON="$response" SESSION_FILE="$SESSION_FILE" ASSETHUB_API_URL="$API_URL" node <<'NODE'
const fs = require('node:fs');
const raw = process.env.RESPONSE_JSON || '';
let payload;
try { payload = JSON.parse(raw); } catch { console.error(raw); process.exit(1); }

if (!payload || payload.success === false || !payload.data || !payload.data.token) {
  console.error('Login failed:', raw);
  process.exit(1);
}

const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
const apiUrl = process.env.ASSETHUB_API_URL || 'http://localhost:13579/api';
const session = {
  apiUrl: apiUrl,
  token: payload.data.token,
  user: payload.data.user || null,
  enterprises: payload.data.enterprises || [],
  tenant_id: process.env.ASSETHUB_TENANT_ID || payload.data.user?.tenant_id || null,
  saved_at: new Date().toISOString(),
};

fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2), 'utf8');

// 输出企业列表供选择
const enterprises = payload.data.enterprises || [];
if (enterprises.length > 1) {
  console.log('\n=== 多租户企业列表 ===');
  enterprises.forEach((e, i) => {
    console.log(`  ${i + 1}. ${e.tenant_name} (ID: ${e.id})`);
  });
  console.log('\n请使用以下命令选择租户:');
  console.log(`  bash ${process.argv[1]} set-tenant <序号>`);
}

console.log(JSON.stringify({
  success: true,
  session_file: sessionFile,
  tenant_id: session.tenant_id,
  user: session.user?.username || 'unknown',
  enterprises_count: enterprises.length,
}, null, 2));
NODE

  echo ""
  echo "✅ 登录成功，会话已保存到: $SESSION_FILE"
}

# 从临时会话凭证文件自动登录（登录后将临时凭证升级为正式 Token）
login_from_temp_session() {
  if [[ ! -f "$TEMP_SESSION_FILE" ]]; then
    echo "临时凭证文件不存在: $TEMP_SESSION_FILE" >&2
    exit 1
  fi

  local username password
  username="$(node -e "
const fs=require('fs');const s=JSON.parse(fs.readFileSync('$TEMP_SESSION_FILE','utf8'));
process.stdout.write(s.username||'');" 2>/dev/null || true)"
  password="$(node -e "
const fs=require('fs');const s=JSON.parse(fs.readFileSync('$TEMP_SESSION_FILE','utf8'));
process.stdout.write(s.password||'');" 2>/dev/null || true)"

  if [[ -z "$username" || -z "$password" ]]; then
    echo "临时凭证文件中未找到用户名或密码" >&2
    exit 1
  fi

  local response
  response="$(curl -sS -X POST "$(normalize_url /users/login)" \
    -H 'Content-Type: application/json' \
    --data-binary "{\"username\":\"${username}\",\"password\":\"${password}\"}")"

  RESPONSE_JSON="$response" SESSION_FILE="$SESSION_FILE" ASSETHUB_API_URL="$API_URL" node <<'NODE'
const fs = require('node:fs');
const raw = process.env.RESPONSE_JSON || '';
let payload;
try { payload = JSON.parse(raw); } catch { console.error(raw); process.exit(1); }

if (!payload || payload.success === false || !payload.data || !payload.data.token) {
  console.error('登录失败:', raw);
  process.exit(1);
}

const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
const apiUrl = process.env.ASSETHUB_API_URL || 'http://localhost:13579/api';
const session = {
  apiUrl: apiUrl,
  token: payload.data.token,
  user: payload.data.user || null,
  enterprises: payload.data.enterprises || [],
  tenant_id: process.env.ASSETHUB_TENANT_ID || payload.data.user?.tenant_id || null,
  saved_at: new Date().toISOString(),
};

fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2), 'utf8');

const enterprises = payload.data.enterprises || [];
if (enterprises.length > 1) {
  console.log('\n=== 多租户企业列表 ===');
  enterprises.forEach((e, i) => {
    console.log('  ' + (i+1) + '. ' + e.tenant_name + ' (ID: ' + e.id + ')');
  });
  console.log('\n请使用以下命令选择租户:');
  console.log('  bash ' + process.argv[1] + ' set-tenant <序号>');
}

console.log(JSON.stringify({
  success: true,
  session_file: sessionFile,
  tenant_id: session.tenant_id,
  user: session.user?.username || 'unknown',
  enterprises_count: enterprises.length,
}, null, 2));
NODE

  echo ""
  echo "✅ 临时凭证登录成功，会话已保存到: $SESSION_FILE"
}

ensure_session() {
  # 优先检查临时会话凭证文件（来自 prompt 传入，仅当前会话有效）
  if [[ -f "$TEMP_SESSION_FILE" ]]; then
    local tmp_token tmp_user
    tmp_token="$(node -e "
const fs=require('fs');const s=JSON.parse(fs.readFileSync('$TEMP_SESSION_FILE','utf8'));
process.stdout.write(s.token||'');" 2>/dev/null || true)"
    # 有凭证但无 token，或 token 已过期 -> 自动登录
    if [[ -z "$tmp_token" ]]; then
      echo "[临时凭证检测] 自动登录中..." >&2
      login_from_temp_session
      return
    fi
    # 有 token，直接使用
    return 0
  fi

  if [[ ! -f "$SESSION_FILE" ]]; then
    echo "会话文件不存在，正在登录..." >&2
    login
  fi
}

perform_request() {
  local method="$1"
  local target_path="$2"
  local body="${3:-}"

  ensure_session

  local token
  token="$(read_session_field token)" || {
    echo "Token 读取失败，正在重新登录..." >&2
    login
    token="$(read_session_field token)"
  }

  local tenant_id="${ASSETHUB_TENANT_ID:-}"
  if [[ -z "$tenant_id" ]]; then
    tenant_id="$(read_session_field tenant_id 2>/dev/null || true)"
  fi

  local url
  url="$(normalize_url "$target_path")"

  # 自动生成 Idempotency-Key（写操作必须，防重复提交）
  # v1.7.0: 允许调用方通过 ASSETHUB_IDEMPOTENCY_KEY 显式 pin（保证重试幂等）
  local idempotency_key="${ASSETHUB_IDEMPOTENCY_KEY:-}"
  if [[ "$method" == "POST" || "$method" == "PUT" || "$method" == "DELETE" ]]; then
    if [[ -z "$idempotency_key" ]]; then
      idempotency_key="op-$(date +%s)-$RANDOM"
    fi
  fi

  local -a curl_args
  curl_args=(
    -sS
    -X "$method"
    "$url"
    -H "Authorization: Bearer $token"
    -w $'\n__STATUS__:%{http_code}'
  )

  if [[ -n "$tenant_id" ]]; then
    curl_args+=(-H "X-Tenant-Id: $tenant_id")
  fi

  # v1.7.0: IoT ingest 路径使用专用 token（ASSETHUB_IOT_TOKEN），不影响其它路径
  # 重建数组以避免留下空元素
  if [[ -n "${ASSETHUB_IOT_TOKEN:-}" && "$target_path" == */iot/* ]]; then
    _old_auth="Authorization: Bearer $token"
    _new_args=()
    _i=0
    while [[ $_i -lt ${#curl_args[@]} ]]; do
      if [[ "${curl_args[$_i]}" == "-H" ]] \
         && [[ $((_i+1)) -lt ${#curl_args[@]} ]] \
         && [[ "${curl_args[$((_i+1))]}" == "$_old_auth" ]]; then
        _new_args+=("-H" "Authorization: Bearer ${ASSETHUB_IOT_TOKEN}")
        _i=$((_i+2))
      else
        _new_args+=("${curl_args[$_i]}")
        _i=$((_i+1))
      fi
    done
    curl_args=("${_new_args[@]}")
    unset _old_auth _new_args _i
  fi

  if [[ -n "$idempotency_key" ]]; then
    curl_args+=(-H "Idempotency-Key: $idempotency_key")
  fi

  # v1.7.0: 旧路径警告（不拦截，只提示到 stderr）
  warn_deprecated_path "$target_path" || true

  if [[ -n "$body" ]]; then
    curl_args+=(-H 'Content-Type: application/json' --data-binary "$body")
  fi

  local response
  # 使用 printf 保留末尾换行（命令替换会吞掉 \n，导致 __STATUS__ 匹配失败）
  response="$(printf '%s\n' "$(curl "${curl_args[@]}")")"

  # 用 awk 提取 status（macOS bash 3.2 $'\n' 对中文响应有 bug，awk 更可靠）
  local status
  local payload
  status="$(echo "$response" | awk '/__STATUS__:/ {split($NF, a, ":"); print a[2]}')"
  payload="$(echo "$response" | awk '/__STATUS__:/ {found=1} found==0 {buf=$0} /__STATUS__:/ {print buf}')"

  # 检查是否触发二次确认（普通端点，非 AI 入口）
  local confirm_token=""
  if [[ "$method" == "POST" || "$method" == "PUT" || "$method" == "DELETE" ]]; then
    confirm_token="$(echo "$payload" | node -e "
const stdin = require('fs').readFileSync(0, 'utf8');
try {
  const j = JSON.parse(stdin);
  if (j.confirmToken) process.stdout.write(j.confirmToken);
} catch(e) {}
" 2>/dev/null || true)"
  fi

  # v1.7.0: 两段式确认需要 ASSETHUB_HIGH_RISK_CONFIRM=YES 显式开启（默认 OFF，避免静默重放）
  if [[ -n "$confirm_token" ]]; then
    if ! high_risk_confirm_enabled; then
      printf '%s\n' "$payload"
      echo "[高风险] 检测到 confirmToken，需要 ASSETHUB_HIGH_RISK_CONFIRM=YES 才自动重放（当前 OFF）" >&2
      echo "[高风险] 如需重放，请人工确认后设置环境变量再调用，或在 Web 管理后台完成。" >&2
      exit 1
    fi
    echo "[两段式确认] 检测到 confirmToken，自动重放请求..." >&2
    local -a retry_args
    retry_args=(
      -sS
      -X "$method"
      "$url"
      -H "Authorization: Bearer $token"
      -H "Idempotency-Key: $idempotency_key"
      -H "X-Risk-Confirm-Token: $confirm_token"
      -H 'Content-Type: application/json'
      --data-binary "$body"
      -w $'\n__STATUS__:%{http_code}'
    )
    if [[ -n "$tenant_id" ]]; then
      retry_args+=(-H "X-Tenant-Id: $tenant_id")
    fi
    response="$(curl "${retry_args[@]}")"
    status="${response##*$'\n'__STATUS__:*}"
    payload="${response%$'\n'__STATUS__:*}"
  fi

  # 401 -> 重新登录重试
  if [[ "$status" == "401" ]]; then
    rm -f "$SESSION_FILE"
    echo "Token 已过期，正在重新登录..." >&2
    login
    perform_request "$method" "$target_path" "$body"
    return
  fi

  printf '%s\n' "$payload"

  if [[ "$status" -ge 400 ]]; then
    # 提供友好的错误诊断提示
    local hint=""
    case "$status" in
      400) hint="请求参数有误，请检查 JSON 格式或必填字段" ;;
      401) hint="认证失败，Token 无效或已过期（应自动重试，如仍失败请重新登录）" ;;
      403) hint="权限不足，当前用户无权执行此操作" ;;
      404) hint="接口不存在，请检查 PATH 是否正确，或确认该模块是否对当前租户开放" ;;
      409) hint="资源冲突，可能已存在相同的记录（如重复提交）" ;;
      422) hint="请求格式正确但语义有误，请检查字段约束（如资产编码重复）" ;;
      429) hint="请求过于频繁，已被限流，请稍后重试" ;;
      500) hint="服务器内部错误，请联系系统管理员" ;;
      502|503) hint="网关错误，服务暂时不可用" ;;
      *)   hint="请检查请求参数和网络连接" ;;
    esac
    echo "[HTTP $status] $hint" >&2
    echo "请求路径: $method $target_path" >&2
    if [[ "$payload" == *'"message":'* ]]; then
      local msg
      msg="$(echo "$payload" | node -e "
const stdin = require('fs').readFileSync(0,'utf8');
try {
  const j = JSON.parse(stdin);
  if (j.message) process.stdout.write(j.message);
  if (j.error) process.stdout.write(' | ' + j.error);
} catch(e){}
" 2>/dev/null || true)"
      [[ -n "$msg" ]] && echo "错误信息: $msg" >&2
    fi
    exit 1
  fi
}

main() {
  local command="${1:-}"

  case "$command" in
    ""|-h|--help)
      print_help
      ;;
    login)
      login
      ;;
    logout)
      # 删除会话缓存文件
      if [[ -f "$SESSION_FILE" ]]; then
        rm -f "$SESSION_FILE"
      fi
      # 清除 node 缓存的 session 数据（防止内存残留）
      node -e "
const fs = require('fs');
const cachePaths = [
  '/tmp/assethub-claw-session.json',
  '/tmp/assethub-claw-token-cache.json',
  process.env.HOME + '/.assethub_session'
];
cachePaths.forEach(p => { try { fs.unlinkSync(p); } catch(e) {} });
" 2>/dev/null || true
      echo "✅ 已注销，所有登录信息已清除"
      ;;
    session)
      if [[ ! -f "$SESSION_FILE" ]]; then
        echo "未登录（无会话文件）"
        exit 1
      fi
      SESSION_FILE="$SESSION_FILE" node <<'NODE'
const fs = require('node:fs');
const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
if (!fs.existsSync(sessionFile)) { console.log('未登录'); process.exit(1); }
const s = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
console.log('=== 当前会话 ===');
console.log('  API 地址:', s.apiUrl || '(未设置)');
console.log('  Token:', s.token ? s.token.substring(0, 20) + '...' : '(无)');
console.log('  租户 ID:', s.tenant_id || '(无)');
console.log('  用户:', s.user?.username || s.user?.real_name || '(未知)');
console.log('  角色:', s.user?.role || '(未知)');
console.log('  保存时间:', s.saved_at || '(未知)');
if (s.enterprises && s.enterprises.length > 0) {
  console.log('  企业列表:');
  s.enterprises.forEach((e, i) => {
    const mark = e.id === s.tenant_id ? ' ← 当前' : '';
    console.log(`    ${i+1}. ${e.tenant_name} (ID: ${e.id})${mark}`);
  });
}
NODE
      ;;
    set-tenant)
      local idx="${2:-}"
      if [[ ! -f "$SESSION_FILE" ]]; then
        echo "未登录，无法选择租户" >&2
        exit 1
      fi
      if [[ -z "$idx" ]]; then
        echo "用法: bash scripts/assethub_api.sh set-tenant <序号>" >&2
        SESSION_FILE="$SESSION_FILE" node <<'NODE'
const fs = require('node:fs');
const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
const s = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
const ents = s.enterprises || [];
if (ents.length === 0) { console.log('无可用企业'); process.exit(1); }
console.log('当前企业列表:');
ents.forEach((e, i) => console.log(`  ${i+1}. ${e.tenant_name} (ID: ${e.id})`));
NODE
        exit 1
      fi
      SESSION_FILE="$SESSION_FILE" node <<NODE
const fs = require('node:fs');
const sessionFile = process.env.SESSION_FILE || '/tmp/assethub-claw-session.json';
const s = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
const ents = s.enterprises || [];
const n = parseInt('${idx}');
if (isNaN(n) || n < 1 || n > ents.length) {
  console.error('序号无效: ${idx}');
  process.exit(1);
}
const selected = ents[n - 1];
s.tenant_id = selected.id;
fs.writeFileSync(sessionFile, JSON.stringify(s, null, 2), 'utf8');
console.log('✅ 已切换到租户:', selected.tenant_name, '(ID:', selected.id + ')');
NODE
      ;;
    modules)
      perform_request GET /api-documentation/modules
      ;;
    module)
      local module_path="${2:-}"
      if [[ -z "$module_path" ]]; then
        echo "module path is required (e.g. assets, maintenance, inventory)" >&2
        exit 1
      fi
      # 路径直接拼接到 /api-documentation/module/ 后
      perform_request GET "/api-documentation/module/$module_path"
      ;;
    endpoints)
      perform_request GET /api-documentation/endpoints
      ;;
    domains)
      # v1.7.0: 15 业务域速查（基于 2026-07-29 swagger 同步）
      cat <<'EOF'
AssetHub 15 业务域速查:

  1. core-assets       核心资产              assets, asset-allocation, idle, scrapping, ...
  2. maintenance       维修与保养            maintenance-management, warranty, daily-maintenance, ...
  3. procurement       采购/合同/供应商        tendering, supplier, contracts
  4. quality           质量管理              quality-control, poct-quality-control, metrology, adverse-reaction
  5. inspection        巡检/合规/安全          inspection, compliance, risk, key-equipment, staff
  6. equipment         设备/备件/技术资料      iot, technical-documents, knowledge-base, large-equipment
  7. acceptance        验收/事件/PDCA        acceptance-management, event-reminder, pdca, ...
  8. org               用户/权限/组织          users, departments, tenants, roles-permissions
  9. finance           财务/折旧              finance, depreciation
 10. notification      通知/消息              notifications, in-app-notifications
 11. system            工作流/审计/分析        workflow, audit-logs, dashboard
 12. ai                AI 智能                asset-ai-assistant
 13. integration       第三方集成              feishu, wechat-mp, wx-cloud
 14. auth              认证/系统              auth, service-tokens, health
 15. deprecated        已弃用/迁移(勿引用)     inventory, materials, ...

详细代表 API 见 ../references/api-modules-overview.md 和 references/endpoint-quick-ref.md
EOF
      ;;
    stats)
      # v1.7.0: 显示文档统计（运行时拉取 /api/api-documentation/modules 计算）
      perform_request GET /api-documentation/modules > /tmp/_assethub_modules.json
      if [[ -s /tmp/_assethub_modules.json ]]; then
        MODULES_FILE=/tmp/_assethub_modules.json node <<'NODE'
const fs = require('node:fs');
let payload;
try { payload = JSON.parse(fs.readFileSync(process.env.MODULES_FILE, 'utf8')); } catch { process.exit(1); }
const mods = (payload && payload.data && payload.data.modules) || payload.modules || payload.data || [];
const arr = Array.isArray(mods) ? mods : [];
console.log(`AssetHub API 运行时统计（${new Date().toISOString()}）`);
console.log(`  总模块数: ${arr.length}`);
const byPrefix = {};
for (const m of arr) {
  const p = (m.path || m.module || '').split('/')[0] || '(root)';
  byPrefix[p] = (byPrefix[p] || 0) + 1;
}
console.log('\n  按一级路径分组:');
Object.entries(byPrefix).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => {
  console.log(`    ${k.padEnd(28)} ${String(v).padStart(4)} 个模块`);
});
NODE
      else
        echo "无法拉取模块列表，请确认已登录 (bash scripts/assethub_api.sh login)" >&2
      fi
      rm -f /tmp/_assethub_modules.json
      ;;
    redirects)
      # v1.7.0: 列出旧路径 → 新路径 重定向
      echo "旧路径 → 新路径 重定向表（v1.7.0 同步，调用时请用新路径）："
      local i
      for ((i = 0; i < ${#PATH_OLD_KEYS[@]}; i++)); do
        printf '  %-45s → %s\n' "/api/${PATH_OLD_KEYS[$i]}" "${PATH_NEW_VALUES[$i]}"
      done
      echo ""
      echo "详细说明见 references/endpoint-quick-ref.md 路径消歧表"
      ;;
    request)
      local method="${2:-}"
      local target_path="${3:-}"
      local body="${4:-}"
      if [[ -z "$method" || -z "$target_path" ]]; then
        echo "request requires METHOD and PATH" >&2
        echo "Example: bash scripts/assethub_api.sh request GET /assets?page=1" >&2
        echo "Example: bash scripts/assethub_api.sh request POST /assets '{\"asset_name\":\"test\"}'" >&2
        exit 1
      fi
      # 方法名统一大写
      method="$(printf '%s' "$method" | tr '[:lower:]' '[:upper:]')"
      perform_request "$method" "$target_path" "$body"
      ;;
    *)
      echo "Unknown command: $command" >&2
      echo "Run without args to see help." >&2
      exit 1
      ;;
  esac
}

main "$@"

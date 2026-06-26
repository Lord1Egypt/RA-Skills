#!/bin/bash
# ============================================================================
# AiPPT API 集成脚本 v4.0.1
# 官方文档: https://open.aippt.cn/docs/zh/
# 作者: 小龙 for OpenClaw | 版本: 4.0.1
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${SKILL_DIR}/.env"
TOKEN_CACHE="${SKILL_DIR}/.token_cache.json"
BASE_URL="https://co.aippt.cn"

[ -f "$ENV_FILE" ] && source "$ENV_FILE"
APP_KEY="${AIPPT_APP_KEY:-}"
SECRET_KEY="${AIPPT_SECRET_KEY:-}"
UID_VALUE="${AIPPT_UID:-openclaw_default}"
die() { echo "{\"error\": \"$1\"}" >&2; exit 1; }

require_keys() {
    [ -n "$APP_KEY" ] && [ -n "$SECRET_KEY" ] || die "未设置 AIPPT_APP_KEY / AIPPT_SECRET_KEY。请在技能设置或安全凭证入口配置，不要在聊天中粘贴 AK/SK。"
}

# 解析 API 响应，非0 code 时输出友好错误信息并退出
check_resp() {
    local resp="$1" context="${2:-}"
    local code msg
    code=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
    msg=$(echo "$resp"  | python3 -c "import sys,json;print(json.load(sys.stdin).get('msg',''))"  2>/dev/null)
    [ "$code" = "0" ] && return 0
    local hint=""
    case "$code" in
        40007) hint="账户余额不足，请充值后重试" ;;
        40008) hint="该功能未开通，请联系管理员开通服务；禁止自动切换到其他生成模式，除非用户明确确认改用 fallback" ;;
        10307) hint="企业模板未配置，已自动回退到普通模板" ;;
        43101) hint="Token 已过期，请删除 .token_cache.json 后重试" ;;
        43102) hint="签名错误，请检查 AIPPT_SECRET_KEY 是否正确" ;;
        12100) hint="AI 内容生成失败，请换个标题或稍后重试" ;;
        12101) hint="内容审核未通过，请修改标题/内容后重试" ;;
        12102) hint="任务不存在，可能对文件任务误调用了 outline/content 接口" ;;
        20003) hint="导出队列已满，等待后自动重试" ;;
        20001) hint="导出任务不存在或已过期，请重新触发导出" ;;
        30001) hint="模板不存在或无权限使用该模板" ;;
        50000) hint="服务器内部错误，请稍后重试" ;;
        *)     hint="未知错误码 ${code}" ;;
    esac
    local prefix="${context:+[${context}] }"
    die "${prefix}${hint}（code=${code}, msg=${msg}）"
}

# 收集 SSE 流式大纲：逐行解析，返回完整大纲文本
collect_outline() {
    python3 -u -c "
import sys, json
parts = []
for line in sys.stdin:
    line = line.rstrip()
    if not line.startswith('data:'):
        continue
    data = line[5:].strip()
    if not data or data == '[DONE]':
        continue
    try:
        obj = json.loads(data)
        content = obj.get('content', '') or obj.get('text', '')
    except Exception:
        content = data
    if content:
        parts.append(content)
sys.stdout.write(''.join(parts))
"
}

generate_signature() {
    local sign_str="${1}@${2}@${3}"
    echo -n "$sign_str" | openssl dgst -sha1 -hmac "$SECRET_KEY" -binary | base64
}

get_token() {
    require_keys
    local now; now=$(date +%s)
    if [ -f "$TOKEN_CACHE" ]; then
        local t e
        t=$(python3 - "$TOKEN_CACHE" <<'PYEOF'
import sys, json
try:
    d = json.load(open(sys.argv[1]))
    print(d.get('token', ''))
except Exception:
    print('')
PYEOF
)
        e=$(python3 - "$TOKEN_CACHE" <<'PYEOF'
import sys, json
try:
    d = json.load(open(sys.argv[1]))
    print(d.get('expire_time', 0))
except Exception:
    print(0)
PYEOF
)
        [ -n "$t" ] && [ "$e" -gt "$now" ] 2>/dev/null && { echo "$t"; return 0; }
    fi
    local ts; ts=$(date +%s)
    local sig; sig=$(generate_signature "GET" "/api/grant/token/" "$ts")
    local resp; resp=$(curl -sL "${BASE_URL}/api/grant/token/?uid=${UID_VALUE}" \
        -H "x-api-key: ${APP_KEY}" -H "x-timestamp: ${ts}" -H "x-signature: ${sig}")
    local token exp cached_at
    token=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")
    exp=$(echo "$resp" | python3 - "$ts" <<'PYEOF'
import sys, json
data = json.load(sys.stdin)['data']
base = int(sys.argv[1])
print(base + int(data.get('time_expire', 259200)))
PYEOF
)
    cached_at=$(date +%s)
    python3 - "$TOKEN_CACHE" "$token" "$exp" "$cached_at" <<'PYEOF'
import sys, json
path, token, exp, cached_at = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
json.dump({'token': token, 'expire_time': exp, 'cached_at': cached_at}, open(path, 'w'), indent=2)
PYEOF
    echo "$token"
}

api_get() {
    local path="$1"; shift
    local token; token=$(get_token)
    curl -s "${BASE_URL}${path}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}" "$@"
}

api_post() {
    local path="$1"; shift
    local token; token=$(get_token)
    curl -s -X POST "${BASE_URL}${path}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}" "$@"
}

# === 命令 ===

cmd_auth() {
    [ -n "$APP_KEY" ] && [ -n "$SECRET_KEY" ] || die "未设置 AIPPT_APP_KEY / AIPPT_SECRET_KEY"
    local ts=$(date +%s)
    local sig=$(generate_signature "GET" "/api/grant/token/" "$ts")
    curl -sL "${BASE_URL}/api/grant/token/?uid=${UID_VALUE}" \
        -H "x-api-key: ${APP_KEY}" -H "x-timestamp: ${ts}" -H "x-signature: ${sig}"
}

cmd_create() {
    local title="${1:?用法: create <标题> [type] [model] [senior_options_json] [is_web_search] [preset_id]}"
    local type="${2:-1}"
    local model="${3:-}"          # glm4.5-air | deepSeek-v3 | doubao-1.5-pro-32k
    local senior_opts="${4:-}"    # JSON 对象字符串, 如 {"page":3,"group":6,"scene":18,"tone":40,"language":47}
    local is_web_search="${5:-}"  # true/false，仅部分 type 支持
    local preset_id="${6:-}"      # 预置词 id，部分 type 必填
    local token; token=$(get_token)
    local curl_args=(-s -X POST "${BASE_URL}/api/ai/chat/v2/task"
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
        --data-urlencode "title=${title}"
        --data-urlencode "type=${type}")
    [ -n "$model" ]       && curl_args+=(--data-urlencode "model=${model}")
    [ -n "$senior_opts" ] && curl_args+=(--data-urlencode "senior_options=${senior_opts}")
    [ -n "$is_web_search" ] && curl_args+=(--data-urlencode "is_web_search=${is_web_search}")
    [ -n "$preset_id" ] && curl_args+=(--data-urlencode "id=${preset_id}")
    curl "${curl_args[@]}"
}

cmd_create_with_file() {
    local file="${1:?用法: create_with_file <文件路径> [type] [model] [senior_options_json] [is_web_search] [preset_id]}"
    local type="${2:-}"
    local model="${3:-}"
    local senior_opts="${4:-}"
    local is_web_search="${5:-}"
    local preset_id="${6:-}"
    [ -f "$file" ] || die "文件不存在: $file"
    if [ -z "$type" ]; then
        case "${file##*.}" in
            doc|docx) type=3  ;;   # Word        → word SSE
            xmind)    type=4  ;;   # XMind       → direct save
            mm)       type=5  ;;   # FreeMind    → direct save
            md)       type=7  ;;   # MD 粘贴      → direct save（传 content 文本字段）
            pdf)      type=9  ;;   # PDF         → word SSE（支持 model）
            txt)      type=10 ;;   # TXT         → word SSE（支持 model）
            ppt|pptx) type=12 ;;   # PPTX        → word SSE
            wps)      type=18 ;;   # WPS         → word SSE（支持 model）
            *) die "不支持的文件格式: ${file##*.}（支持: doc/docx/xmind/mm/md/pdf/txt/ppt/pptx/wps）";;
        esac
    fi
    local token; token=$(get_token)
    case "$type" in
        7)
            # Markdown 粘贴：传文本内容（content 字段）
            local curl_args=(-s -X POST "${BASE_URL}/api/ai/chat/v2/task"
                -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
                --data-urlencode "type=${type}"
                --data-urlencode "content@${file}")
            [ -n "$senior_opts" ] && curl_args+=(--data-urlencode "senior_options=${senior_opts}")
            [ -n "$is_web_search" ] && curl_args+=(--data-urlencode "is_web_search=${is_web_search}")
            [ -n "$preset_id" ] && curl_args+=(--data-urlencode "id=${preset_id}")
            curl "${curl_args[@]}"
            ;;
        *)
            # 其余类型：文件上传（file 字段）
            local curl_args=(-s -X POST "${BASE_URL}/api/ai/chat/v2/task"
                -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
                -F "type=${type}" -F "file=@${file}")
            [ -n "$model" ]       && curl_args+=(-F "model=${model}")
            [ -n "$senior_opts" ] && curl_args+=(-F "senior_options=${senior_opts}")
            [ -n "$is_web_search" ] && curl_args+=(-F "is_web_search=${is_web_search}")
            [ -n "$preset_id" ] && curl_args+=(-F "id=${preset_id}")
            curl "${curl_args[@]}"
            ;;
    esac
}

cmd_create_from_url() {
    local url="${1:?用法: create_from_url <URL>}"
    api_post "/api/ai/chat/v2/task" --data-urlencode "type=16" --data-urlencode "link=${url}"
}

cmd_outline() {
    local task_id="${1:?用法: outline <task_id>}"
    local token=$(get_token)
    curl -s --max-time 120 -N "${BASE_URL}/api/ai/chat/outline?task_id=${task_id}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

cmd_content() {
    local task_id="${1:?用法: content <task_id> [template_id]}"
    local tpl="${2:-}"
    local url="/api/ai/chat/v2/content?task_id=${task_id}"
    [ -n "$tpl" ] && url="${url}&template_id=${tpl}"
    api_get "$url"
}

cmd_check() {
    local ticket="${1:?用法: check <ticket> (注意: 参数是ticket, 不是task_id!)}"
    api_get "/api/ai/chat/v2/content/check?ticket=${ticket}"
}

cmd_wait() {
    local ticket="${1:?用法: wait <ticket> [timeout_seconds]}"
    local timeout="${2:-120}"
    local elapsed=0
    while [ "$elapsed" -lt "$timeout" ]; do
        local resp=$(cmd_check "$ticket")
        local status=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('status',''))" 2>/dev/null)
        if [ "$status" = "2" ]; then
            echo "$resp"
            return 0
        fi
        sleep 3; elapsed=$((elapsed + 3))
    done
    die "等待内容生成超时 (${timeout}秒)"
}

cmd_options() {
    api_get "/api/template_component/suit/select"
}

# 获取 AI 生成高级配置选项（真实枚举来自接口，不要硬编码）
cmd_senior_options() {
    api_get "/api/ai/chat/senior/option"
}

# 获取 AI 生成高级配置选项，并格式化为可读清单，方便 Agent 询问用户
cmd_senior_options_pretty() {
    cmd_senior_options | python3 -c "
import sys, json

try:
    raw = json.load(sys.stdin)
except Exception as e:
    print('解析高级配置失败：%s' % e)
    sys.exit(1)

code = raw.get('code')
if code != 0:
    print(json.dumps(raw, ensure_ascii=False))
    sys.exit(0)

for group in raw.get('data') or []:
    name = group.get('name', '')
    key = group.get('key', '')
    gid = group.get('id', '')
    print(f'## {name} ({key}) parent_id={gid}')
    children = group.get('children') or []
    for item in children:
        default = ' default' if item.get('is_default') else ''
        beta = ' beta' if item.get('is_beta') else ''
        print(f\"- id={item.get('id')} name={item.get('name')}{default}{beta}\")
    print()
"
}

cmd_templates() {
    local page="${1:-1}" size="${2:-10}" color="${3:-}" style="${4:-}" task_id="${5:-}"
    local url="/api/template_component/suit/search?page=${page}&size=${size}"
    [ -n "$color" ]   && url="${url}&colour_id=${color}"
    [ -n "$style" ]   && url="${url}&style_id=${style}"
    [ -n "$task_id" ] && url="${url}&task_id=${task_id}"
    api_get "$url"
}

cmd_enterprise_templates() {
    api_get "/api/template_component/enterprise/suit/list"
}

# SSE 流式接口：等待完成后返回（type=3 Word）
cmd_word() {
    local task_id="${1:?用法: word <task_id>}"
    local token=$(get_token)
    curl -s --max-time 180 -N "${BASE_URL}/api/ai/chat/v2/word?task_id=${task_id}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

# SSE 流式接口：等待完成后返回（type=16 URL链接）
cmd_link() {
    local task_id="${1:?用法: link <task_id>}"
    local token=$(get_token)
    curl -s --max-time 180 -N "${BASE_URL}/api/ai/chat/link?task_id=${task_id}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

# SSE 流式接口：等待完成后返回（参考文档模式）
cmd_refer() {
    local task_id="${1:?用法: refer <task_id>}"
    local token=$(get_token)
    curl -s --max-time 180 -N "${BASE_URL}/api/ai/chat/refer?task_id=${task_id}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

# 文件解析（type=4/5/7 XMind/FreeMind/Markdown → 返回 Markdown 文本）
cmd_conver_file() {
    local task_id="${1:?用法: conver_file <task_id> <type>}"
    local type="${2:?用法: conver_file <task_id> <type>}"
    local token=$(get_token)
    curl -s "${BASE_URL}/api/ai/conver/file?task_id=${task_id}&type=${type}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

cmd_save() {
    local task_id="${1:?用法: save <task_id> <template_id> [name] [template_type]}"
    local tpl_id="${2:?用法: save <task_id> <template_id> [name] [template_type]}"
    local name="${3:-}"
    local tpl_type="${4:-}"  # 模板类型: enterprise=企业模板, 空=普通模板
    local token
    token=$(get_token)
    local curl_args=(-s -X POST "${BASE_URL}/api/design/v2/save"
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
        --data-urlencode "task_id=${task_id}"
        --data-urlencode "template_id=${tpl_id}")
    [ -n "$name" ]     && curl_args+=(--data-urlencode "name=${name}")
    [ -n "$tpl_type" ] && curl_args+=(--data-urlencode "template_type=${tpl_type}")
    curl "${curl_args[@]}"
}

# 获取 PPT 树形结构（智能生成大纲后、文件/链接内容生成后均会使用）
cmd_ppt_data() {
    local task_id="${1:?task_id required}"
    local token; token=$(get_token)
    curl -s -X POST "${BASE_URL}/api/generate/data" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}" \
        --data-urlencode "task_id=${task_id}"
}

# 提交大纲（save 前必须调用）
# content 参数：type=1 传完整大纲数据；其他类型传大纲+内容数据（均为 JSON 字符串）
cmd_outline_save() {
    local task_id="${1:?task_id required}"
    local content="${2:?content required}"
    local token; token=$(get_token)
    curl -s -X POST "${BASE_URL}/api/ai/chat/v2/outline/save" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}" \
        --data-urlencode "task_id=${task_id}" \
        --data-urlencode "content=${content}"
}

# 将 generate/data 返回的树形 JSON 转换为可读 Markdown 大纲文本
tree_to_outline() {
    python3 -u -c "
import sys, json

def tree_to_md(node, depth=0):
    lines = []
    val = (node.get('value') or '').strip()
    ntype = node.get('type', '')
    if val and ntype not in ('catalog', 'ending'):
        prefix = '#' * min(depth + 1, 4)
        lines.append(prefix + ' ' + val)
    for child in node.get('children', []):
        lines.extend(tree_to_md(child, depth + 1))
    return lines

try:
    data = json.load(sys.stdin)
    tree = data.get('data', {})
    lines = tree_to_md(tree)
    sys.stdout.write('\n'.join(lines))
except Exception:
    sys.stdout.write('')
"
}

cmd_export() {
    local design_id="${1:?用法: export <design_id> [format] [edit]}"
    local format="${2:-ppt}" edit="${3:-true}"
    api_post "/api/download/export/file" -d "id=${design_id}" -d "format=${format}" -d "edit=${edit}" -d "files_to_zip=false"
}

cmd_export_result() {
    local task_key="${1:?用法: export_result <task_key>}"
    api_post "/api/download/export/file/result" -d "task_key=${task_key}"
}

cmd_wait_export() {
    local task_key="${1:?用法: wait_export <task_key> [timeout_seconds]}"
    local timeout="${2:-120}"
    local elapsed=0
    while [ "$elapsed" -lt "$timeout" ]; do
        local resp=$(cmd_export_result "$task_key")
        local parsed=$(echo "$resp" | python3 -c "
import sys, json
d = json.load(sys.stdin)
code = d.get('code', '')
msg  = d.get('msg', '')
data = d.get('data', [])

def clean_url(u):
    # 修复 \& 转义（OSS 预签名 URL 中 & 被反斜杠转义导致 Expires 参数解析失败）
    return u.replace('\\\\&', '&').replace('\\&', '&').strip()

if code == 20003:
    print('QUEUE_FULL')
elif code == 0:
    url = ''
    if isinstance(data, list) and data and isinstance(data[0], str) and data[0].startswith('http'):
        url = data[0]
    elif isinstance(data, str) and data.startswith('http'):
        url = data
    elif isinstance(data, dict):
        # 新版 API：URL 在 data.fileUrl 字段
        url = data.get('fileUrl') or data.get('file_url') or data.get('url') or ''
    if url:
        print(clean_url(url))
    else:
        print('PENDING')
else:
    print(f'ERROR:{code}:{msg}')
" 2>/dev/null)
        case "$parsed" in
            http*)
                echo "$parsed"
                return 0
                ;;
            QUEUE_FULL)
                echo '{"step":"wait_export","msg":"导出队列已满，等待中..."}' >&2
                sleep 5; elapsed=$((elapsed + 5))
                ;;
            PENDING)
                sleep 3; elapsed=$((elapsed + 3))
                ;;
            ERROR:*)
                die "导出失败: $parsed"
                ;;
            *)
                sleep 3; elapsed=$((elapsed + 3))
                ;;
        esac
    done
    die "等待导出超时 (${timeout}秒)"
}

# 文件名去重：已存在则追加 _1 _2 ...
unique_output_path() {
    local base="$1" ext="$2"
    local path="${base}.${ext}"
    local n=1
    while [ -f "$path" ]; do
        path="${base}_${n}.${ext}"
        n=$((n + 1))
    done
    echo "$path"
}

verify_file() {
    local file="$1" format="$2"
    [ -f "$file" ] || return 1
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    [ "$size" -gt 1000 ] 2>/dev/null || return 1  # 文件太小，可能是错误页
    local magic=$(head -c 4 "$file" | xxd -p 2>/dev/null)
    case "$format" in
        ppt)  [[ "$magic" == "504b0304" ]] || return 1 ;;  # PK (zip)
        pdf)  [[ "$magic" == "25504446" ]] || return 1 ;;  # %PDF
        *)    return 0 ;;  # png/word 不检查
    esac
}

cmd_download() {
    local task_id="${1:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local tpl_id="${2:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local output="${3:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local format="${4:-ppt}"
    local name="${5:-}"

    echo '{"step":"save","msg":"正在生成PPT作品..."}' >&2
    local save_resp=$(cmd_save "$task_id" "$tpl_id" "$name")
    local design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    echo '{"step":"export","msg":"正在导出文件..."}' >&2
    local export_resp=$(cmd_export "$design_id" "$format")
    local export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
    local task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
    
    # 如果队列满, 等待后重试 (最多3次)
    local retries=0
    while [ "$export_code" = "20003" ] && [ "$retries" -lt 3 ]; do
        echo '{"step":"export","msg":"导出队列已满，等待10秒后重试..."}' >&2
        sleep 10
        export_resp=$(cmd_export "$design_id" "$format")
        export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
        task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
        retries=$((retries + 1))
    done
    [ -n "$task_key" ] && [ "$task_key" != "" ] || die "触发导出失败: $export_resp"

    echo '{"step":"wait_export","msg":"等待导出完成..."}' >&2
    local download_url=$(cmd_wait_export "$task_key" 180)
    [ -n "$download_url" ] || die "获取下载链接失败"

    echo '{"step":"downloading","msg":"正在下载文件..."}' >&2
    curl -sL -o "$output" "$download_url" || die "下载失败"
    
    # 验证下载文件
    if ! verify_file "$output" "$format"; then
        local actual_size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output" 2>/dev/null || echo "0")
        die "文件验证失败: 格式不正确或文件损坏 (size=${actual_size}字节)"
    fi
    
    local size=$(ls -l "$output" | awk '{print $5}')
    echo "{\"step\":\"done\",\"file\":\"${output}\",\"size\":${size},\"design_id\":\"${design_id}\"}"
}

cmd_generate() {
    # 预提取无值标志，避免被位置参数吞掉
    local outline_only=false
    local _pre_args=()
    for _a in "$@"; do [ "$_a" = "--outline-only" ] && outline_only=true || _pre_args+=("$_a"); done
    set -- "${_pre_args[@]+"${_pre_args[@]}"}"

    local title="${1:?用法: generate <标题> [template_id] [output_dir] [formats] [template_type] [--model <m>] [--options <json>]}"
    shift
    local model="" senior_opts="" is_web_search="" preset_id=""
    local -a positional=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --model)        model="$2";        shift 2 ;;
            --options)      senior_opts="$2";  shift 2 ;;
            --web-search)   is_web_search="true"; shift ;;
            --no-web-search) is_web_search="false"; shift ;;
            --preset-id)    preset_id="$2"; shift 2 ;;
            *)              positional+=("$1"); shift ;;
        esac
    done
    local tpl_id="${positional[0]:-}"
    local output_dir="${positional[1]:-$HOME/Desktop}"
    local formats="${positional[2]:-ppt}"  # 逗号分隔: ppt,pdf,word,png
    local tpl_type="${positional[3]:-}"    # enterprise=企业模板, 空=普通模板

    echo '{"step":"create","msg":"创建任务..."}' >&2
    local create_resp; create_resp=$(cmd_create "$title" 1 "$model" "$senior_opts" "$is_web_search" "$preset_id")
    check_resp "$create_resp" "create"
    local task_id=$(echo "$create_resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
    [ -n "$task_id" ] || die "创建任务失败（无 task_id）: $create_resp"
    echo "{\"step\":\"created\",\"task_id\":\"${task_id}\"}" >&2

    echo '{"step":"outline","msg":"正在生成大纲..."}' >&2
    local outline_text outline_json title_json
    outline_text=$(cmd_outline "$task_id" | collect_outline)
    outline_json=$(echo "$outline_text" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
    title_json=$(echo "$title"        | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
    echo "{\"step\":\"outline_ready\",\"task_id\":\"${task_id}\",\"title\":${title_json},\"outline\":${outline_json}}" >&2
    [ "$outline_only" = "true" ] && exit 0

    echo '{"step":"content","msg":"生成内容..."}' >&2
    local content_resp
    content_resp=$(cmd_content "$task_id" "$tpl_id")
    local ticket
    ticket=$(echo "$content_resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
v=d.get('data')
print(v if v and str(v) != 'None' else '')
" 2>/dev/null)
    [ -n "$ticket" ] || die "触发内容生成失败: $content_resp"
    echo "{\"step\":\"content_triggered\",\"ticket\":\"${ticket}\"}" >&2

    echo '{"step":"wait_content","msg":"等待内容生成完成，约25秒..."}' >&2
    cmd_wait "$ticket" > /dev/null
    echo '{"step":"content_done","msg":"内容生成完成"}' >&2

    # 一键完整生成路径：用户明确跳过大纲编辑时，content 完成后仍需在 save 前提交结构
    echo '{"step":"outline_save","msg":"提交大纲..."}' >&2
    local ppt_data_resp_g outline_save_resp_g
    ppt_data_resp_g=$(cmd_ppt_data "$task_id")
    check_resp "$ppt_data_resp_g" "ppt_data"
    outline_save_resp_g=$(cmd_outline_save "$task_id" "$(echo "$ppt_data_resp_g" | python3 -c "import sys,json;d=json.load(sys.stdin);print(json.dumps(d.get('data','')))")")
    check_resp "$outline_save_resp_g" "outline_save"
    echo '{"step":"outline_saved","msg":"大纲提交完成"}' >&2
    echo '{"step":"composing","msg":"合成中，请稍候..."}' >&2

    # 如果没有指定模板, 从前20个里随机选一个
    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"随机选择模板..."}' >&2
        tpl_id=$(cmd_templates 1 20 "" "" "$task_id" | python3 -c "
import sys,json,random
d=json.load(sys.stdin)
items=d.get('data',{}).get('list',[])
if items:
    print(random.choice(items)['id'])
else:
    print('')
" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    # 生成 PPT 作品 (只需一次)
    echo '{"step":"save","msg":"正在生成PPT作品..."}' >&2
    local save_resp=$(cmd_save "$task_id" "$tpl_id" "$title" "$tpl_type")
    local design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"
    local results="["

    # 按格式顺序导出 (不能并行, 会导致队列满)
    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local ext="pptx"
        case "$fmt" in
            ppt)  ext="pptx" ;;
            pdf)  ext="pdf" ;;
            word) ext="docx" ;;
            png)  ext="png" ;;
        esac
        local outfile
        outfile=$(unique_output_path "${output_dir}/${safe_title}" "$ext")

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2
        
        # 触发导出 (带重试)
        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10
                retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成...\"}" >&2
        local download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2
            continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

cmd_generate_continue() {
    local task_id="${1:?用法: generate_continue <task_id> <title> [template_id] [output_dir] [formats] [template_type]}"
    local title="${2:?用法: generate_continue <task_id> <title> [template_id] [output_dir] [formats] [template_type]}"
    local tpl_id="${3:-}"
    local output_dir="${4:-$HOME/Desktop}"
    local formats="${5:-ppt}"
    local tpl_type="${6:-}"

    # 智能生成正确顺序：先取树形结构/编辑大纲 → 选模板 → 提交大纲 → 带模板请求内容
    echo '{"step":"ppt_data","msg":"获取PPT结构数据..."}' >&2
    local ppt_data_resp_c outline_save_resp_c
    ppt_data_resp_c=$(cmd_ppt_data "$task_id")
    check_resp "$ppt_data_resp_c" "ppt_data"

    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"随机选择模板..."}' >&2
        tpl_id=$(cmd_templates 1 20 "" "" "$task_id" | python3 -c "
import sys,json,random
d=json.load(sys.stdin)
items=d.get('data',{}).get('list',[])
if items:
    print(random.choice(items)['id'])
else:
    print('')
" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    echo '{"step":"outline_save","msg":"提交编辑后大纲..."}' >&2
    outline_save_resp_c=$(cmd_outline_save "$task_id" "$(echo "$ppt_data_resp_c" | python3 -c "import sys,json;d=json.load(sys.stdin);print(json.dumps(d.get('data','')))")")
    check_resp "$outline_save_resp_c" "outline_save"
    echo '{"step":"outline_saved","msg":"大纲提交完成"}' >&2

    echo '{"step":"content","msg":"按确认后大纲和模板生成内容..."}' >&2
    local content_resp ticket
    content_resp=$(cmd_content "$task_id" "$tpl_id")
    ticket=$(echo "$content_resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
v=d.get('data')
print(v if v and str(v) != 'None' else '')
" 2>/dev/null)
    [ -n "$ticket" ] || die "触发内容生成失败: $content_resp"
    echo "{\"step\":\"content_triggered\",\"ticket\":\"${ticket}\"}" >&2

    echo '{"step":"wait_content","msg":"等待内容生成完成，约25秒..."}' >&2
    cmd_wait "$ticket" > /dev/null
    echo '{"step":"content_done","msg":"内容生成完成"}' >&2

    echo '{"step":"composing","msg":"合成中，请稍候..."}' >&2

    echo '{"step":"save","msg":"正在生成PPT作品..."}' >&2
    local save_resp design_id
    save_resp=$(cmd_save "$task_id" "$tpl_id" "$title" "$tpl_type")
    design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title results="["
    safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"

    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local ext="pptx"
        case "$fmt" in
            ppt)  ext="pptx" ;;
            pdf)  ext="pdf"  ;;
            word) ext="docx" ;;
            png)  ext="png"  ;;
        esac
        local outfile
        outfile=$(unique_output_path "${output_dir}/${safe_title}" "$ext")

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2
        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp"    | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))"  2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10; retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "None" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成...\"}" >&2
        local download_url
        download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2; continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize; fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

cmd_generate_save() {
    # 文件类任务续跑：outline_save → pick_template → composing → save → export
    # 用于文件类任务在 word/refer SSE 完成后续跑，或参考文档模式续跑
    local task_id="${1:?用法: generate_save <task_id> <title> [template_id] [output_dir] [formats] [template_type]}"
    local title="${2:?用法: generate_save <task_id> <title> [template_id] [output_dir] [formats] [template_type]}"
    local tpl_id="${3:-}"
    local output_dir="${4:-$HOME/Desktop}"
    local formats="${5:-ppt}"
    local tpl_type="${6:-}"

    # 提交大纲（官方流程必须步骤，save 前必须调用）
    echo '{"step":"outline_save","msg":"提交大纲..."}' >&2
    local ppt_data_resp outline_content outline_save_resp
    ppt_data_resp=$(cmd_ppt_data "$task_id")
    check_resp "$ppt_data_resp" "ppt_data"
    outline_content=$(echo "$ppt_data_resp" | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin).get('data','')))")
    outline_save_resp=$(cmd_outline_save "$task_id" "$(echo "$ppt_data_resp" | python3 -c "import sys,json;d=json.load(sys.stdin);print(json.dumps(d.get('data','')))")")
    check_resp "$outline_save_resp" "outline_save"
    echo '{"step":"outline_saved","msg":"大纲提交完成"}' >&2

    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"随机选择模板..."}' >&2
        tpl_id=$(cmd_templates 1 20 "" "" "$task_id" | python3 -c "
import sys,json,random
d=json.load(sys.stdin)
items=d.get('data',{}).get('list',[])
if items:
    print(random.choice(items)['id'])
else:
    print('')
" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    echo '{"step":"composing","msg":"合成中，请稍候..."}' >&2

    local save_resp design_id
    save_resp=$(cmd_save "$task_id" "$tpl_id" "$title" "$tpl_type")
    check_resp "$save_resp" "save"
    design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "None" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title results="["
    safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"

    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local ext="pptx"
        case "$fmt" in
            ppt)  ext="pptx" ;;
            pdf)  ext="pdf"  ;;
            word) ext="docx" ;;
            png)  ext="png"  ;;
        esac
        local outfile
        outfile=$(unique_output_path "${output_dir}/${safe_title}" "$ext")

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2
        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp"    | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))"  2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10; retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "None" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成...\"}" >&2
        local download_url
        download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2; continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize; fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

cmd_generate_from_file() {
    # 预提取无值标志，避免被位置参数吞掉
    local outline_only=false
    local _pre_args=()
    for _a in "$@"; do [ "$_a" = "--outline-only" ] && outline_only=true || _pre_args+=("$_a"); done
    set -- "${_pre_args[@]+"${_pre_args[@]}"}"

    local file="${1:?用法: generate_from_file <文件路径> [template_id] [output_dir] [formats] [template_type] [--model <m>] [--options <json>]}"
    shift
    local model="" senior_opts="" is_web_search="" preset_id=""
    local -a positional=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --model)        model="$2";        shift 2 ;;
            --options)      senior_opts="$2";  shift 2 ;;
            --web-search)   is_web_search="true"; shift ;;
            --no-web-search) is_web_search="false"; shift ;;
            --preset-id)    preset_id="$2"; shift 2 ;;
            *)              positional+=("$1"); shift ;;
        esac
    done
    local tpl_id="${positional[0]:-}"
    local output_dir="${positional[1]:-$HOME/Desktop}"
    local formats="${positional[2]:-ppt}"
    local tpl_type="${positional[3]:-}"  # enterprise=企业模板, 空=普通模板

    [ -f "$file" ] || die "文件不存在: $file"
    local filename=$(basename "$file")
    local title="${filename%.*}"

    # 根据扩展名推断 type（严格按 API 文档）
    local file_ext="${file##*.}"
    local file_type
    case "$file_ext" in
        doc|docx) file_type=3  ;;   # Word  → word SSE
        xmind)    file_type=4  ;;   # XMind → direct save
        mm)       file_type=5  ;;   # FreeMind → direct save
        md)       file_type=7  ;;   # MD 粘贴  → direct save
        pdf)      file_type=9  ;;   # PDF  → word SSE
        txt)      file_type=10 ;;   # TXT  → word SSE
        ppt|pptx) file_type=12 ;;   # PPTX → word SSE
        wps)      file_type=18 ;;   # WPS  → word SSE
        *) die "不支持的文件格式: $file_ext（支持: doc/docx/xmind/mm/md/pdf/txt/ppt/pptx/wps）" ;;
    esac

    echo '{"step":"create","msg":"从文件创建任务..."}' >&2
    local create_resp
    create_resp=$(cmd_create_with_file "$file" "" "$model" "$senior_opts" "$is_web_search" "$preset_id")
    check_resp "$create_resp" "create"
    local task_id
    task_id=$(echo "$create_resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
    [ -n "$task_id" ] || die "创建任务失败（无 task_id）: $create_resp"
    echo "{\"step\":\"created\",\"task_id\":\"${task_id}\",\"file_type\":${file_type}}" >&2

    # 按文件类型选择正确的内容生成接口（严格按 API 文档）
    # type=3/9/10/12/18 (Word/PDF/TXT/PPTX/WPS) → word SSE
    # type=4/5/7 (XMind/FreeMind/MD) → 直接 save
    case "$file_type" in
        3|9|10|12|18)
            echo '{"step":"word","msg":"解析文档并生成大纲+内容，约30秒..."}' >&2
            local word_resp
            word_resp=$(cmd_word "$task_id")
            if echo "$word_resp" | grep -q '"code"[[:space:]]*:[[:space:]]*40008'; then
                die "文档导入接口未开通（code=40008）。请联系管理员开通 Word/文档导入能力；不要自动切换到智能生成模式，除非用户明确确认改用 fallback。"
            fi
            # 触发服务端内容生成，结果通过 generate/data 拉取
            # 调 generate/data 拿树形结构，转换为可读大纲
            echo '{"step":"ppt_data","msg":"获取PPT结构数据..."}' >&2
            local ppt_data_resp outline_text outline_json title_json
            ppt_data_resp=$(cmd_ppt_data "$task_id")
            check_resp "$ppt_data_resp" "ppt_data"
            outline_text=$(echo "$ppt_data_resp" | tree_to_outline)
            outline_json=$(echo "$outline_text" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            title_json=$(echo "$title"          | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            echo "{\"step\":\"outline_ready\",\"task_id\":\"${task_id}\",\"title\":${title_json},\"outline\":${outline_json}}" >&2
            [ "$outline_only" = "true" ] && exit 0
            ;;
        4|5)
            # XMind/FreeMind: 调 conver_file 触发内容解析，再用 generate/data 获取树形大纲
            echo '{"step":"file_parsed","msg":"解析文件内容..."}' >&2
            cmd_conver_file "$task_id" "$file_type" > /dev/null 2>&1 || true
            echo '{"step":"ppt_data","msg":"获取PPT结构数据..."}' >&2
            local ppt_data_resp outline_text outline_json title_json
            ppt_data_resp=$(cmd_ppt_data "$task_id")
            check_resp "$ppt_data_resp" "ppt_data"
            outline_text=$(echo "$ppt_data_resp" | tree_to_outline)
            outline_json=$(echo "$outline_text" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            title_json=$(echo "$title"          | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            echo "{\"step\":\"outline_ready\",\"task_id\":\"${task_id}\",\"title\":${title_json},\"outline\":${outline_json}}" >&2
            [ "$outline_only" = "true" ] && exit 0
            ;;
        7)
            # Markdown: 任务创建后直接调 generate/data 获取树形大纲
            echo '{"step":"ppt_data","msg":"获取PPT结构数据..."}' >&2
            local ppt_data_resp outline_text outline_json title_json
            ppt_data_resp=$(cmd_ppt_data "$task_id")
            check_resp "$ppt_data_resp" "ppt_data"
            outline_text=$(echo "$ppt_data_resp" | tree_to_outline)
            outline_json=$(echo "$outline_text" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            title_json=$(echo "$title"          | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
            echo "{\"step\":\"outline_ready\",\"task_id\":\"${task_id}\",\"title\":${title_json},\"outline\":${outline_json}}" >&2
            [ "$outline_only" = "true" ] && exit 0
            ;;
    esac

    echo '{"step":"composing","msg":"合成中，请稍候..."}' >&2

    # 选择模板，从前20个里随机选一个
    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"随机选择模板..."}' >&2
        tpl_id=$(cmd_templates 1 20 "" "" "$task_id" | python3 -c "
import sys,json,random
d=json.load(sys.stdin)
items=d.get('data',{}).get('list',[])
if items:
    print(random.choice(items)['id'])
else:
    print('')
" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    # 生成 PPT 作品（直接 save，无需 outline+content 步骤）
    echo '{"step":"save","msg":"正在生成PPT作品，约10秒..."}' >&2
    local save_resp
    save_resp=$(cmd_save "$task_id" "$tpl_id" "$title" "$tpl_type")
    check_resp "$save_resp" "save"
    local design_id
    design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "None" ] || die "生成PPT作品失败（无 design_id）: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title
    safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"
    local results="["

    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local out_ext="pptx"
        case "$fmt" in
            ppt)  out_ext="pptx" ;;
            pdf)  out_ext="pdf" ;;
            word) out_ext="docx" ;;
            png)  out_ext="png" ;;
        esac
        local outfile
        outfile=$(unique_output_path "${output_dir}/${safe_title}" "$out_ext")

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2

        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10
                retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "None" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败: $export_resp\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成，约30秒...\"}" >&2
        local download_url
        download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2
            continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize
            fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

cmd_generate_with_refer() {
    # 用法: generate_with_refer <PPT主题> <文件1> [文件2...文件5] [--output_dir <dir>] [--formats <fmts>] [--template_id <id>] [--template_type <type>]
    # 参考文档 B端规则：最多5个文件，每个文件 ≤ 10MB，支持 Word/PDF/TXT/WPS
    local title="${1:?用法: generate_with_refer <PPT主题> <文件1> [文件2..文件5]}"
    shift

    local tpl_id="" output_dir="$HOME/Desktop" formats="ppt" tpl_type="" outline_only=false
    local -a refer_files=()

    # 解析剩余参数：文件路径 或 --key value 选项
    while [ $# -gt 0 ]; do
        case "$1" in
            --template_id)   tpl_id="$2";        shift 2 ;;
            --output_dir)    output_dir="$2";     shift 2 ;;
            --formats)       formats="$2";        shift 2 ;;
            --template_type) tpl_type="$2";       shift 2 ;;
            --outline-only)  outline_only=true;   shift ;;
            -*)              die "未知选项: $1" ;;
            *)               refer_files+=("$1"); shift ;;
        esac
    done

    [ ${#refer_files[@]} -gt 0 ] || die "至少需要提供一个参考文档文件路径"
    [ ${#refer_files[@]} -le 5 ] || die "参考文档最多支持 5 个文件（B端限制），当前传入 ${#refer_files[@]} 个"

    # 校验每个文件：存在 + ≤ 10MB
    local max_size=$((10 * 1024 * 1024))
    for f in "${refer_files[@]}"; do
        [ -f "$f" ] || die "文件不存在: $f"
        local fsz
        fsz=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo 0)
        if [ "$fsz" -gt "$max_size" ]; then
            local fmb; fmb=$(echo "scale=1; $fsz / 1048576" | bc)
            die "文件超过大小限制（${fmb}MB > 10MB）: $f\n请压缩后重试，或改用「文档转PPT」模式。"
        fi
    done

    # 用 type=17 创建参考文档任务，title 必传，files[] 多文件上传
    echo '{"step":"create","msg":"上传参考文档，创建任务（type=17）..."}' >&2
    local token; token=$(get_token)
    local curl_args=(-s -X POST "${BASE_URL}/api/ai/chat/v2/task"
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
        -F "type=17"
        -F "title=${title}")
    for f in "${refer_files[@]}"; do
        curl_args+=(-F "files=@${f}")
    done
    local create_resp
    create_resp=$(curl "${curl_args[@]}")
    check_resp "$create_resp" "create"
    local task_id
    task_id=$(echo "$create_resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
    [ -n "$task_id" ] || die "创建任务失败（无 task_id）: $create_resp"
    echo "{\"step\":\"created\",\"task_id\":\"${task_id}\",\"files\":${#refer_files[@]}}" >&2

    # refer SSE：以文件为背景素材，围绕 title 生成内容
    echo '{"step":"refer","msg":"参考文档模式生成内容，约30秒..."}' >&2
    local outline_text outline_json title_json
    outline_text=$(cmd_refer "$task_id" | collect_outline)
    outline_json=$(echo "$outline_text" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
    title_json=$(echo "$title"          | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))")
    echo "{\"step\":\"outline_ready\",\"task_id\":\"${task_id}\",\"title\":${title_json},\"outline\":${outline_json}}" >&2
    [ "$outline_only" = "true" ] && exit 0
    echo '{"step":"refer_done","msg":"参考文档内容生成完成"}' >&2

    # 随机选模板
    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"随机选择模板..."}' >&2
        tpl_id=$(cmd_templates 1 20 "" "" "$task_id" | python3 -c "
import sys,json,random
d=json.load(sys.stdin)
items=d.get('data',{}).get('list',[])
if items:
    print(random.choice(items)['id'])
else:
    print('')
" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    echo '{"step":"save","msg":"正在生成PPT作品，约10秒..."}' >&2
    local save_resp
    save_resp=$(cmd_save "$task_id" "$tpl_id" "$title" "$tpl_type")
    check_resp "$save_resp" "save"
    local design_id
    design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "None" ] || die "生成PPT作品失败（无 design_id）: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title
    safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"
    local results="["

    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local out_ext="pptx"
        case "$fmt" in
            ppt)  out_ext="pptx" ;;
            pdf)  out_ext="pdf" ;;
            word) out_ext="docx" ;;
            png)  out_ext="png" ;;
        esac
        local outfile
        outfile=$(unique_output_path "${output_dir}/${safe_title}" "$out_ext")

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2

        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10; retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "None" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成，约30秒...\"}" >&2
        local download_url
        download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2; continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize; fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

# === 入口 ===
cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
    auth)                  cmd_auth "$@" ;;
    create)                cmd_create "$@" ;;
    create_with_file)      cmd_create_with_file "$@" ;;
    create_from_url)       cmd_create_from_url "$@" ;;
    outline)               cmd_outline "$@" ;;
    content)               cmd_content "$@" ;;
    check)                 cmd_check "$@" ;;
    wait)                  cmd_wait "$@" ;;
    options)               cmd_options "$@" ;;
    senior_options)        cmd_senior_options "$@" ;;
    senior_options_pretty) cmd_senior_options_pretty "$@" ;;
    templates)             cmd_templates "$@" ;;
    enterprise_templates)  cmd_enterprise_templates "$@" ;;
    word)                  cmd_word "$@" ;;
    link)                  cmd_link "$@" ;;
    refer)                 cmd_refer "$@" ;;
    conver_file)           cmd_conver_file "$@" ;;
    ppt_data)              cmd_ppt_data "$@" ;;
    outline_save)          cmd_outline_save "$@" ;;
    save)                  cmd_save "$@" ;;
    export)                cmd_export "$@" ;;
    export_result)         cmd_export_result "$@" ;;
    wait_export)           cmd_wait_export "$@" ;;
    download)              cmd_download "$@" ;;
    generate)              cmd_generate "$@" ;;
    generate_continue)     cmd_generate_continue "$@" ;;
    generate_save)         cmd_generate_save "$@" ;;
    generate_from_file)    cmd_generate_from_file "$@" ;;
    generate_with_refer)   cmd_generate_with_refer "$@" ;;
    help|*)
        cat <<EOF
AiPPT API 集成脚本 v4.0.1

一键完整生成 (仅在用户明确不编辑大纲时使用):
  generate <标题> [template_id] [output_dir] [formats] [template_type]
    从标题一键生成PPT并下载。v4.0.1 默认应先用 --outline-only 展示/编辑大纲。
    formats用逗号分隔: ppt,pdf,word,png
    template_type: enterprise=企业模板，空=普通模板
    示例: generate "年终总结" "" ~/Desktop "ppt,pdf"

  generate_from_file <文件路径> [template_id] [output_dir] [formats] [template_type]
    从文件一键生成PPT并下载（文档转PPT）。支持 Word/PDF/TXT/MD/PPTX/XMind
    template_type: enterprise=企业模板，空=普通模板
    示例: generate_from_file ~/Desktop/report.pdf "" ~/Desktop "ppt"

  generate_with_refer <PPT主题> <文件1> [文件2..文件5] [--output_dir <dir>] [--formats <fmts>] [--template_id <id>]
    以文件为背景素材，围绕指定主题重新生成PPT（参考文档模式，type=17）
    B端限制：最多5个文件，每个文件 ≤ 10MB，支持 Word/PDF/TXT/WPS
    示例: generate_with_refer "2025年战略规划" ~/Desktop/report.pdf ~/Desktop/data.docx

高级配置 (可附加到 generate / generate_from_file):
  --model <模型>     AI 模型：glm4.5-air | deepSeek-v3 | doubao-1.5-pro-32k
                     仅 type=1(标题)/9(PDF)/10(TXT)/18(WPS) 支持
  --options <json>   高级配置 JSON 对象字符串，如 '{"page":3,"group":6,"scene":18,"tone":40,"language":47}'
                     先调 senior_options 查询可用 ID，再按 key 组装对象
  --web-search       开启联网搜索（仅 type=1/17 可传）
  --no-web-search    关闭联网搜索
  --preset-id <id>   预置词 id（部分 type 必填）
  senior_options            获取高级配置原始 JSON（真实枚举）
  senior_options_pretty     获取高级配置可读清单（先看这里，再询问用户）

模板:
  templates [page] [size] [color] [style]   搜索普通模板
  enterprise_templates                       获取企业模板列表（B端配置的专属模板）
  options                                    获取模板颜色/风格筛选选项

分步操作（type=1 智能生成专用）:
  create <标题> [type]                       创建任务
  outline <task_id>                          获取大纲 (SSE流式) ← 仅type=1
  content <task_id> [template_id]            触发内容生成 ← 仅type=1
  check <ticket>                             检查生成状态
  wait <ticket> [timeout]                    等待内容生成完成

分步操作（文件/URL 导入专用）:
  create_with_file <文件> [type]             从文件创建 (3=Word,7=MD,9=PDF,10=TXT,12=PPTX,18=WPS)
  create_from_url <URL>                      从网页创建 (type=16)
  word <task_id>                             Word文档解析+生成 (SSE，type=3专用)
  link <task_id>                             URL链接解析+生成 (SSE，type=16专用)
  refer <task_id>                            参考文档模式生成 (SSE)
  conver_file <task_id> <type>               解析MD/XMind/FreeMind为Markdown

通用分步操作:
  save <task_id> <template_id> [name] [template_type]  生成PPT作品 → design_id
  export <design_id> [format] [edit]         触发导出 (ppt/pdf/png/word)
  export_result <task_key>                   查询导出结果
  wait_export <task_key> [timeout]           等待导出完成 → 返回下载URL
  auth                                       获取/刷新 Token

环境变量 (.env):
  AIPPT_APP_KEY      API Key (必需)
  AIPPT_SECRET_KEY   Secret Key (必需)
  AIPPT_UID          用户标识 (默认: openclaw_default)
EOF
        ;;
esac

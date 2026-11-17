#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────────
# MCP Tool 通讯脚本 — bash + curl + python3（零外部依赖）
#
# 用法:
#   bash call_tool.sh <tool_name> "<message>" ['<context_json>'] [conversation_id]
#
# 参数:
#   tool_name         工具名（如 requirements_elicitation）
#   message           用户消息/请求内容
#   context           JSON 字符串，含 stage 等阶段控制参数（可选，默认 ""）
#   conversation_id   CCID，首次调用省略，后续从响应头 [Conversation-ID: ...] 提取并回传
#
# 输出:
#   服务端响应原文（纯文本）到 stdout
#   错误信息到 stderr，退出码 1
#
# 设计:
#   远程 MCP 服务端使用 stateless_http 模式，无需维护 Mcp-Session-Id。
#   会话通过 CCID（Conversation ID）在应用层管理：
#     - 首次调用 conversation_id 留空，服务端在响应文本中返回 [Conversation-ID: ...]
#     - 后续调用将 CCID 作为第 4 个参数回传
#   本脚本直接发送 tools/call JSON-RPC 请求，解析 SSE/JSON 响应并提取文本。
# ─────────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── 参数解析 ──
TOOL_NAME="${1:?用法: bash call_tool.sh <tool_name> \"<message>\" ['<context_json>'] [conversation_id]}"
MESSAGE="${2:?缺少参数: message}"
CONTEXT="${3:-}"
CCID="${4:-}"

# ── 定位配置文件 ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: 配置文件不存在: $CONFIG_FILE" >&2
    exit 1
fi

# 从 config.json 提取 remote_url 和 api_key
REMOTE_URL=$(python3 -c "
import json
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
    print(cfg['remote_url'])
")
API_KEY=$(python3 -c "
import json
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
    print(cfg.get('api_key', ''))
")

# ── 临时文件（使用脚本目录下的 .tmp 避免系统 tmp 权限问题） ──
TMP_DIR="$SCRIPT_DIR/.tmp"
mkdir -p "$TMP_DIR"
TMP_BODY="$TMP_DIR/.body"
TMP_HEADERS="$TMP_DIR/.headers"
trap 'rm -f "$TMP_BODY" "$TMP_HEADERS"' EXIT

# ── 构造 tools/call JSON-RPC payload（用 python3 安全转义） ──
CALL_PAYLOAD=$(python3 -c "
import json, sys
sys.stdout.write(json.dumps({
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'tools/call',
    'params': {
        'name': sys.argv[1],
        'arguments': {
            'message': sys.argv[2],
            'context': sys.argv[3] if len(sys.argv) > 3 else '',
            'conversation_id': sys.argv[4] if len(sys.argv) > 4 else ''
        }
    }
}, ensure_ascii=False))
" "$TOOL_NAME" "$MESSAGE" "$CONTEXT" "$CCID")

# ── 发送请求 ──
# ── 构造请求头 ──
CURL_HEADERS=(
    -H "Content-Type: application/json"
    -H "Accept: application/json, text/event-stream"
)
if [[ -n "$API_KEY" ]]; then
    CURL_HEADERS+=(-H "Authorization: Bearer $API_KEY")
fi

# ── 发送请求 ──
HTTP_CODE=$(curl -s -o "$TMP_BODY" -D "$TMP_HEADERS" -w "%{http_code}" \
    --max-time 300 \
    "${CURL_HEADERS[@]}" \
    -d "$CALL_PAYLOAD" \
    "$REMOTE_URL")

if [[ "$HTTP_CODE" -ge 400 ]]; then
    echo "Error: 请求失败 (HTTP $HTTP_CODE)" >&2
    cat "$TMP_BODY" >&2
    exit 1
fi

# ── 获取 Content-Type ──
CONTENT_TYPE=$(grep -i "^content-type:" "$TMP_HEADERS" | tail -1 | sed 's/^[^:]*: *//;s/\r//g;s/ *$//')

# ── 提取响应文本并输出 ──
python3 -c "
import json, sys

content_type = '''$CONTENT_TYPE'''
body_file = '$TMP_BODY'

with open(body_file, 'r', encoding='utf-8') as f:
    raw = f.read()

if not raw.strip():
    print('Error: 空响应', file=sys.stderr)
    sys.exit(1)

obj = None

if 'text/event-stream' in content_type:
    # SSE 流式响应：逐行解析 data: 行，取最后一个含 result 或 error 的
    last_data = ''
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith('data: '):
            last_data = stripped[6:]
    if last_data:
        try:
            obj = json.loads(last_data)
        except json.JSONDecodeError:
            # JSON 解析失败，直接输出原始数据
            print(last_data)
            sys.exit(0)
    else:
        # 无有效 data 行，输出原始内容
        print(raw)
        sys.exit(0)
else:
    # 普通 JSON 响应
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        print(raw)
        sys.exit(0)

# ── 从 JSON-RPC 响应中提取文本 ──
if not isinstance(obj, dict):
    print(str(obj))
    sys.exit(0)

# JSON-RPC error
if 'error' in obj:
    err = obj['error']
    msg = err.get('message', 'Unknown error')
    detail = err.get('data', '')
    if detail:
        print(f'Error: {msg} — {detail}', file=sys.stderr)
    else:
        print(f'Error: {msg}', file=sys.stderr)
    sys.exit(1)

# JSON-RPC result
result = obj.get('result', {})
content_list = result.get('content', [])

text = ''
if content_list and isinstance(content_list, list):
    text = content_list[0].get('text', '')
elif isinstance(result, str):
    text = result
else:
    text = json.dumps(result, ensure_ascii=False, indent=2)

sys.stdout.write(text)
if text and not text.endswith('\n'):
    sys.stdout.write('\n')
"

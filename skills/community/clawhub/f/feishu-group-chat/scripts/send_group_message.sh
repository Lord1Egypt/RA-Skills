#!/bin/bash
# send_group_message.sh - 通用飞书群聊消息构造器
#
# 用法:
#   bash scripts/send_group_message.sh <群标识> <联系人key> "正文内容"
#   bash scripts/send_group_message.sh <群标识> <联系人key> "正文内容" --image /path/to/image.png
#   bash scripts/send_group_message.sh <群标识> <联系人key> "" --image /path/to/image.png
#
# 使用方式:
#   source <(bash scripts/send_group_message.sh moltpool ray "你好")
#   # 然后用 feishu_im_user_message 工具发送，参数从环境变量取：
#   #   CHAT_ID, MSG_TYPE, MSG_CONTENT, HAS_IMAGE, IMAGE_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG="$SKILL_DIR/config.json"
TEMPLATE="$SKILL_DIR/config-template.json"

if [ $# -lt 3 ]; then
    echo "用法: send_group_message.sh <群标识> <联系人key> <正文内容> [--image /path]" >&2
    exit 1
fi

GROUP_KEY="$1"
CONTACT_KEY="$2"
shift 2

# ── 自动初始化 config.json ──
if [ ! -f "$CONFIG" ]; then
    if [ -f "$TEMPLATE" ]; then
        cp "$TEMPLATE" "$CONFIG"
        echo "已从模板创建 config.json，请编辑后重试: $CONFIG" >&2
    else
        echo "错误: 配置文件不存在且无模板: $CONFIG" >&2
    fi
    exit 1
fi

MERGED=$(python3 -c "
import json, sys
with open('$CONFIG') as f:
    cfg = json.load(f)
group = cfg.get('groups', {}).get('$GROUP_KEY')
contact = cfg.get('contacts', {}).get('$CONTACT_KEY')
if not group:
    print(f'错误: 群 $GROUP_KEY 不在 config.json 中', file=sys.stderr); sys.exit(1)
if not contact:
    print(f'错误: 联系人 $CONTACT_KEY 不在 config.json 中', file=sys.stderr); sys.exit(1)
should_at = group.get('at_rules', {}).get('$CONTACT_KEY', True)
print(json.dumps({
    'chat_id': group['chat_id'],
    'open_id': contact['open_id'],
    'name': contact.get('name', '$CONTACT_KEY'),
    'at': should_at
}))
" 2>/dev/null) || { echo "错误: 配置读取失败" >&2; exit 1; }

CHAT_ID=$(echo "$MERGED" | python3 -c "import json,sys; print(json.load(sys.stdin)['chat_id'])")
OPEN_ID=$(echo "$MERGED" | python3 -c "import json,sys; print(json.load(sys.stdin)['open_id'])")
SHOULD_AT=$(echo "$MERGED" | python3 -c "import json,sys; print(json.load(sys.stdin)['at'])")

# ── Agent 前缀自动从 IDENTITY.md / SOUL.md 读取 ──
AGENT_PREFIX=$(python3 -c "
import os, re
for f in ['$HOME/.openclaw/workspace/IDENTITY.md', '$HOME/.openclaw/workspace/SOUL.md']:
    if os.path.exists(f):
        for line in open(f):
            if 'Name:' in line or 'name:' in line:
                name = line.split(':')[-1].strip().rstrip('.').rstrip(',')
                name = re.sub(r'\*+', '', name).strip()
                print(name + ': ')
                exit()
print('')
" 2>/dev/null)

# ── 参数解析 ──
BODY=""
IMAGE_PATH=""
IMAGE_KEY=""
HAS_IMAGE="false"

while [ $# -gt 0 ]; do
    case "$1" in
        --image)
            shift; IMAGE_PATH="${1:-}" ;;
        --image-key)
            shift; IMAGE_KEY="$1"; HAS_IMAGE="true" ;;
        *)
            BODY="$1" ;;
    esac
    shift
done

if [ -z "$BODY" ] && [ -z "$IMAGE_PATH" ] && [ -z "$IMAGE_KEY" ]; then
    echo "错误: 正文和图片不能同时为空" >&2; exit 1
fi

# ── 图片上传（如果提供本地文件） ──
if [ -n "$IMAGE_PATH" ]; then
    if [ ! -f "$IMAGE_PATH" ]; then
        echo "错误: 图片文件不存在: $IMAGE_PATH" >&2; exit 1
    fi

    CREDS=$(python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
ch = cfg.get('channels', {}).get('feishu', {})
print(json.dumps({'appId': ch.get('appId',''), 'appSecret': ch.get('appSecret','')}))
" 2>/dev/null)

    if [ -z "$CREDS" ]; then
        echo "错误: 无法读取飞书应用凭证" >&2; exit 1
    fi

    APP_ID=$(echo "$CREDS" | python3 -c "import json,sys; print(json.load(sys.stdin)['appId'])")
    APP_SECRET=$(echo "$CREDS" | python3 -c "import json,sys; print(json.load(sys.stdin)['appSecret'])")

    TOKEN_RESP=$(curl -sf -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
        -H 'Content-Type: application/json' \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" 2>/dev/null)

    ACCESS_TOKEN=$(echo "$TOKEN_RESP" | python3 -c "
import json, sys
r = json.load(sys.stdin)
if r.get('code') == 0: print(r['tenant_access_token'])
else: print(f\"获取 token 失败: {r.get('msg','unknown')}\", file=sys.stderr); sys.exit(1)
" 2>/dev/null) || true

    if [ -z "$ACCESS_TOKEN" ]; then
        echo "错误: 获取 tenant_access_token 失败" >&2; exit 1
    fi

    UPLOAD_RESP=$(curl -sf -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -F "image_type=message" \
        -F "image=@$IMAGE_PATH" 2>/dev/null)

    IMAGE_KEY=$(echo "$UPLOAD_RESP" | python3 -c "
import json, sys
r = json.load(sys.stdin)
if r.get('code') == 0: print(r['data']['image_key'])
else: print(f\"图片上传失败: {r.get('msg','unknown')}\", file=sys.stderr); sys.exit(1)
" 2>/dev/null) || true

    if [ -z "$IMAGE_KEY" ]; then
        echo "错误: 图片上传失败" >&2; exit 1
    fi

    HAS_IMAGE="true"
fi

# ── 构造 content JSON ──
# 格式（at=true）：text(prefix) → at(对方) → text(" " + body) → [img]
# 格式（at=false）：text(prefix + body) → [img]

if [ "$SHOULD_AT" = "True" ]; then
    if [ -n "$BODY" ] && [ "$HAS_IMAGE" = "true" ]; then
        MSG_CONTENT=$(jq -n -c \
            --arg prefix "$AGENT_PREFIX" \
            --arg uid "$OPEN_ID" \
            --arg body "$BODY" \
            --arg img "$IMAGE_KEY" \
            '{zh_cn:{title:"",content:[[
                {tag:"text",text:$prefix},
                {tag:"at",user_id:$uid},
                {tag:"text",text:(" "+$body)},
                {tag:"img",image_key:$img}
            ]]}}')
    elif [ -n "$BODY" ] && [ "$HAS_IMAGE" = "false" ]; then
        MSG_CONTENT=$(jq -n -c \
            --arg prefix "$AGENT_PREFIX" \
            --arg uid "$OPEN_ID" \
            --arg body "$BODY" \
            '{zh_cn:{title:"",content:[[
                {tag:"text",text:$prefix},
                {tag:"at",user_id:$uid},
                {tag:"text",text:(" "+$body)}
            ]]}}')
    elif [ -z "$BODY" ] && [ "$HAS_IMAGE" = "true" ]; then
        MSG_CONTENT=$(jq -n -c \
            --arg prefix "$AGENT_PREFIX" \
            --arg uid "$OPEN_ID" \
            --arg img "$IMAGE_KEY" \
            '{zh_cn:{title:"",content:[[
                {tag:"text",text:$prefix},
                {tag:"at",user_id:$uid},
                {tag:"img",image_key:$img}
            ]]}}')
    else
        echo "错误: 正文和图片不能同时为空" >&2; exit 1
    fi
else
    FULL_TEXT="${AGENT_PREFIX}${BODY}"
    if [ "$HAS_IMAGE" = "true" ]; then
        MSG_CONTENT=$(jq -n -c \
            --arg txt "$FULL_TEXT" \
            --arg img "$IMAGE_KEY" \
            '{zh_cn:{title:"",content:[[
                {tag:"text",text:$txt},
                {tag:"img",image_key:$img}
            ]]}}')
    else
        MSG_CONTENT=$(jq -n -c \
            --arg txt "$FULL_TEXT" \
            '{zh_cn:{title:"",content:[[{tag:"text",text:$txt}]]}}')
    fi
fi

# ── 输出环境变量（source-friendly） ──
echo "CHAT_ID='$CHAT_ID'"
echo "MSG_TYPE='post'"
echo "MSG_CONTENT='${MSG_CONTENT}'"
echo "HAS_IMAGE='$HAS_IMAGE'"
echo "IMAGE_KEY='$IMAGE_KEY'"

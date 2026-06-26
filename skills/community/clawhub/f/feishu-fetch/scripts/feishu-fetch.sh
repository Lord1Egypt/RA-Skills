#!/usr/bin/env bash
# feishu-fetch.sh — 下载飞书群消息中的 file/image/audio 附件
#
# 用法：feishu-fetch.sh <message_id> [options]
# 选项：--type TYPE  --output PATH  --agent NAME  --print-key  -h
#
# stdout（成功）：下载后的本地文件绝对路径
# 凭据 / token / file_key 不会出现在 stdout（除 --print-key 外），不会写入日志。
# 所有 API 调用仅 open.feishu.cn。

set -euo pipefail

usage() {
  cat <<'INNER_EOF'
feishu-fetch.sh — 下载飞书群消息中的 file/image/audio 附件

Usage:
  feishu-fetch.sh <message_id> [options]

Arguments:
  message_id        飞书消息 ID (om_xxx)。必须是 file/image/audio 消息本身，
                    不是 thread 里的文本 reply。

Options:
  --type TYPE       资源类型：file (默认) / image / audio
  --output PATH     输出文件路径（默认 /tmp/<file_name>）
  --agent NAME      飞书账户名（覆盖 $AGENT_NAME，回退 main）
  --print-key       只打印 file_key 后退出（调试用，正常流程不要用）
  -h, --help        显示此帮助

Output:
  stdout            下载的本地文件绝对路径
  stderr            错误信息
  exit 0  成功 | exit 1 API 错误 | exit 2 参数错 | exit 3 msg 不存在 | exit 4 权限不足

Env:
  AGENT_NAME        默认账户名（被 --agent 覆盖）
INNER_EOF
}

# ---- 参数解析 ----
MSG_ID=""
RES_TYPE=""  # 空 = auto-detect from msg_type
OUTPUT=""
AGENT_NAME_OPT="${AGENT_NAME:-main}"
PRINT_KEY_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)        RES_TYPE="$2"; shift 2;;
    --output)      OUTPUT="$2"; shift 2;;
    --agent)       AGENT_NAME_OPT="$2"; shift 2;;
    --print-key)   PRINT_KEY_ONLY=1; shift;;
    -h|--help)     usage; exit 0;;
    --)            shift; break;;
    -*)            echo "error: unknown option: $1" >&2; usage; exit 2;;
    *)             MSG_ID="$1"; shift;;
  esac
done

if [[ -z "$MSG_ID" ]]; then
  echo "error: message_id required" >&2
  usage; exit 2
fi
if [[ -n "$RES_TYPE" ]] && [[ ! "$RES_TYPE" =~ ^(file|image|audio)$ ]]; then
  echo "error: invalid type: $RES_TYPE (must be file|image|audio or empty for auto)" >&2
  exit 2
fi

# RES_TYPE 空表示 auto-detect（从消息体拿 msg_type 后决定）
AUTO_TYPE=0
if [[ -z "$RES_TYPE" ]]; then
  AUTO_TYPE=1
fi

# ---- 临时目录（脚本退出时 trap 清理）----
TMPDIR="$(mktemp -d)"
cleanup() { rm -rf "$TMPDIR" 2>/dev/null || true; }
trap cleanup EXIT

# ---- Step 1: 读 credentials + 拿 token ----
# 凭据从 openclaw.json 读（runtime），不硬编码
CONFIG="$HOME/.openclaw/openclaw.json"
if [[ ! -f "$CONFIG" ]]; then
  echo "error: openclaw config not found: $CONFIG" >&2
  exit 1
fi

read -r APP_ID APP_SECRET < <(AGENT="$AGENT_NAME_OPT" CONFIG="$CONFIG" python3 -c '
import json, os
c = json.load(open(os.environ["CONFIG"]))
accs = c.get("channels", {}).get("feishu", {}).get("accounts", {})
name = os.environ["AGENT"] if os.environ["AGENT"] in accs else "main"
a = accs.get(name, {})
print(a.get("appId",""), a.get("appSecret",""))
')

if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  echo "error: app credentials missing for agent: $AGENT_NAME_OPT" >&2
  exit 1
fi

# 拿 token（secret 通过 stdin 喂 curl，命令行不出现）
printf '{"app_id":"%s","app_secret":"%s"}' "$APP_ID" "$APP_SECRET" \
  | curl -fsS -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
        -H 'Content-Type: application/json' \
        --data-binary @- \
  > "$TMPDIR/tok.json"

TOKEN="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tenant_access_token"])' "$TMPDIR/tok.json")"

# ---- Step 2: 拿 message body 取 file_key ----
# 注意：HTTP 4xx 时飞书也会返 body 错误码（不是 200+230020），所以不用 -f
curl -sS -X GET "https://open.feishu.cn/open-apis/im/v1/messages/$MSG_ID" \
  -H "Authorization: Bearer $TOKEN" > "$TMPDIR/msg.json"

# 校验 API 返回
ERR_CODE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("code",-1))' "$TMPDIR/msg.json")"
if [[ "$ERR_CODE" != "0" ]]; then
  ERR_MSG="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("msg","unknown"))' "$TMPDIR/msg.json")"
  echo "error: message API $ERR_CODE: $ERR_MSG" >&2
  case "$ERR_CODE" in
    230027) exit 4 ;;  # 权限不足
    230020|9999*) exit 3 ;;  # message 不存在 / ID 格式不合法
    *)      exit 1 ;;
  esac
fi

# 提取 msg_type + key 字段（image 消息是 image_key，file/audio 是 file_key）
# 使用 auto-detect 或用户显式 --type；不匹配报错
MSG_TYPE="$(python3 -c '
import json, sys
print(json.load(open(sys.argv[1]))["data"]["items"][0]["msg_type"])
' "$TMPDIR/msg.json")"

if [[ $AUTO_TYPE -eq 1 ]]; then
  RES_TYPE="$MSG_TYPE"
  if [[ ! "$RES_TYPE" =~ ^(file|image|audio)$ ]]; then
    echo "error: unsupported msg_type: $RES_TYPE (auto-detect from message body)" >&2
    exit 1
  fi
else
  if [[ "$RES_TYPE" != "$MSG_TYPE" ]]; then
    echo "warning: --type=$RES_TYPE but message msg_type=$MSG_TYPE, using --type" >&2
  fi
fi

# 提取 key / name（按 RES_TYPE 取对应字段）
FILE_KEY="$(python3 -c '
import json, sys
d = json.load(open(sys.argv[1]))
content = json.loads(d["data"]["items"][0]["body"]["content"])
t = sys.argv[2]
key_field = "image_key" if t == "image" else "file_key"
print(content[key_field])
' "$TMPDIR/msg.json" "$RES_TYPE")"
FILE_NAME="$(python3 -c '
import json, sys
d = json.load(open(sys.argv[1]))
content = json.loads(d["data"]["items"][0]["body"]["content"])
t = sys.argv[2]
if t == "image":
    # image 消息没有 file_name，默认按 key 命名
    print("image_" + content["image_key"][:12] + ".jpg")
else:
    print(content.get("file_name", "attachment"))
' "$TMPDIR/msg.json" "$RES_TYPE")"

if [[ $PRINT_KEY_ONLY -eq 1 ]]; then
  printf '%s\n' "$FILE_KEY"
  exit 0
fi

# ---- Step 3: 下载资源 ----
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="/tmp/$FILE_NAME"
fi
mkdir -p "$(dirname "$OUTPUT")"

# 同样：下载失败时飞书可能返 HTTP 4xx + body 错误码，先拿 body 再判断
curl -sS -X GET \
  "https://open.feishu.cn/open-apis/im/v1/messages/$MSG_ID/resources/$FILE_KEY?type=$RES_TYPE" \
  -H "Authorization: Bearer $TOKEN" \
  -o "$TMPDIR/dl.body"

# 校验下载响应：以 { 开头的 body 是 JSON 错误码；否则是文件字节 = 成功
DL_CODE="$(python3 -c '
import json, sys
content = open(sys.argv[1], "rb").read(1).decode("utf-8", errors="ignore")
if content == "{":
    d = json.load(open(sys.argv[1]))
    print(d.get("code", -1))
else:
    print(0)  # 非 JSON 开头 = 文件字节 = 成功
' "$TMPDIR/dl.body")"

if [[ "$DL_CODE" != "0" ]]; then
  DL_MSG="$(python3 -c '
import json, sys
d = json.load(open(sys.argv[1]))
print(d.get("msg", "download failed"))
' "$TMPDIR/dl.body")"
  echo "error: download $DL_CODE: $DL_MSG" >&2
  case "$DL_CODE" in
    230027) exit 4 ;;  # 权限不足
    230020|9999*) exit 3 ;;  # resource 不存在
    *)      exit 1 ;;
  esac
fi

# 成功：写到 OUTPUT
mv "$TMPDIR/dl.body" "$OUTPUT"

# 成功：输出绝对路径
printf '%s\n' "$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"

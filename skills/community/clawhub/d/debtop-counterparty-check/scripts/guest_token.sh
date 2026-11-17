#!/usr/bin/env bash
# 取游客令牌：**先复用缓存**（刷新），缓存不可用才新建 —— 同一个用户短时间反复使用
# 只会换发令牌，不会每次都建出一个新游客。
#
# 用法:
#   bash scripts/guest_token.sh [输出文件] [BASE] [客户端标识]
#   默认输出 $HOME/.cache/debtop/guest.json, 默认 BASE https://agent.debtop.com
#
# 退出码: 0 成功（stdout 为 access_token）；非 0 失败（stderr 为原因，含服务端错误码）。
# 注意: 只有缓存不可用时才会创建游客（配额: 单 IP 3 次/小时、全局 500 次/天），
#       不要把本脚本当"连通性探测"反复执行。
set -euo pipefail

# 凭据落盘的权限约束（ClawHub 安全审查 T09）：guest.json 里是可直接调用后端的
# access/refresh token 与设备标识，等同口令，一律按私密文件处理。
# umask 077 保证本脚本新建的目录与文件都只允许属主访问（不受调用方 umask 影响）。
umask 077

# 依赖检查：缺失时给出明确提示（而不是让调用方去猜 curl/python3 的报错）
for bin in curl python3; do
  # 注意: 变量后跟全角字符必须用 ${} 括起, 否则在 UTF-8 locale 下 bash 会把全角字符并进变量名
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "缺少依赖: ${bin}（见 references/guest-access.md「运行前提与替代方案」）" >&2
    exit 127
  fi
done

OUT="${1:-$HOME/.cache/debtop/guest.json}"
BASE="${2:-https://agent.debtop.com}"
# 客户端标识(可选, 第 3 个参数): 取值见 references/client-source-ids.md, 与链接 source 同一套。
# 只在"新建游客"时上报。这个字段是**锦上添花**, 绝不为它阻断取令牌:
# 省略或不合法都只是"忽略"(服务端记 public_web), 打印提示后继续创建。
SKILL_ID="${3:-}"
case "$SKILL_ID" in
  "")
    ;;
  *[!A-Za-z0-9._-]*)
    # 该值要进 JSON 与内网头: 含引号/空白/全角字符会破坏报文, 一律忽略并提示
    echo "客户端标识不合法，已忽略（只允许字母/数字与 . _ -）：${SKILL_ID}" >&2
    SKILL_ID=""
    ;;
  *)
    SKILL_ID="$(printf '%s' "$SKILL_ID" | tr '[:upper:]' '[:lower:]')"
    ;;
esac
# 技能包标识(第 4 个参数; 默认=本 SKILL 的包名, 一般不用传):
# 让后端把游客与其后的调用记录归到"本 SKILL"上(skillCode → 令牌 claim → 内网头 X-MCP-Skill-Code)。
# 与上面的客户端标识是两个维度, 不要互相替代。
SKILL_CODE="${4:-debtop-counterparty-check}"
case "$SKILL_CODE" in
  *[!A-Za-z0-9._-]*)
    echo "技能包标识不合法，已忽略（只允许字母/数字与 . _ -）：${SKILL_CODE}" >&2
    SKILL_CODE=""
    ;;
  *)
    SKILL_CODE="$(printf '%s' "$SKILL_CODE" | tr '[:upper:]' '[:lower:]')"
    ;;
esac
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 客户端标识缺省时按规则生成（规则见 references/client-source-ids.md「生成规则」）:
# 宿主平台给了产品名(DEBTOP_CLIENT_NAME)就按规则算, 否则兜底 mcp; 显式传入第 3 个参数时以传入值为准。
if [ -z "$SKILL_ID" ]; then
  if [ -n "${DEBTOP_CLIENT_NAME:-}" ]; then
    SKILL_ID="$(python3 "$DIR/client_id.py" --name "$DEBTOP_CLIENT_NAME" 2>/dev/null || true)"
  fi
  if [ -z "$SKILL_ID" ]; then
    SKILL_ID="mcp"
  fi
  echo "客户端标识未显式传入，已按规则取用: ${SKILL_ID}${DEBTOP_CLIENT_NAME:+ (产品名: $DEBTOP_CLIENT_NAME)}" >&2
fi

# 缓存目录: 本次新建时直接建为 0700; 已存在的目录不动（可能是共享目录, 改权限会伤到别处）。
# 老版本以宽松权限落过盘的缓存文件, 下面用 secure_file 就地收紧到 0600。
CACHE_DIR="$(dirname "$OUT")"
if [ ! -d "$CACHE_DIR" ]; then
  mkdir -p -m 700 "$CACHE_DIR"
fi

# 只收紧"已存在的普通文件"; 符号链接与特殊文件跳过, 避免改到别处的目标
secure_file() {
  if [ -f "$1" ] && [ ! -L "$1" ]; then
    chmod 600 "$1" 2>/dev/null || true
  fi
}
secure_file "$OUT"

# 同一份缓存必须串行使用: refresh 一次性轮换, 并发刷新会被判重放并撤销整条授权链。
# 有 flock 就锁住; 没有时退化为"无锁", 此时务必保证同一份缓存只被一个进程使用。
if command -v flock >/dev/null 2>&1; then
  exec 9>"$OUT.lock"
  flock 9
fi

TMP="$OUT.tmp"
rm -f "$TMP"

# 从响应文件取 accessToken: 成功打印到 stdout 并返回 0; 失败把服务端错误打到 stderr 并返回 1
emit_token() {
  python3 - "$1" <<'PY'
import json, sys
try:
    payload = json.load(open(sys.argv[1]))
except Exception as exc:  # noqa: BLE001
    sys.exit(f"响应无法解析: {exc}")
data = payload.get("data") or {}
token = data.get("accessToken")
if not token:
    code = payload.get("code") or payload.get("error") or "UNKNOWN"
    detail = payload.get("message") or payload.get("error_description") or ""
    sys.exit(f"取游客令牌失败: {code} {detail}".strip())
print(token)
PY
}

# 读缓存里的 refreshToken（缓存不存在或结构不符时打印空串）
read_refresh() {
  python3 - "$1" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1])).get("data") or {}
except Exception:  # noqa: BLE001
    sys.exit(0)
print(data.get("refreshToken") or "")
PY
}

# ① 复用缓存: 本机取过令牌且 refreshToken 仍有效 → 刷新（一次性轮换 → 必须原地覆盖写回）。
#    刷新失败静默落到"新建": 服务端在同一设备标识的去重窗口内会复用既有游客换发令牌，
#    不会因此多建一个游客。
if [ -s "$OUT" ]; then
  RT="$(read_refresh "$OUT")"
  if [ -n "$RT" ]; then
    if curl -sS --max-time 20 -X POST -H 'Content-Type: application/json' \
         -d "{\"refreshToken\":\"$RT\"}" -o "$TMP" \
         "$BASE/bff/v1/guest-access/refresh" \
       && TOKEN="$(emit_token "$TMP" 2>/dev/null)"; then
      mv "$TMP" "$OUT"
      secure_file "$OUT"
      printf '%s\n' "$TOKEN"
      exit 0
    fi
    rm -f "$TMP"
  fi
fi

# ② 稳定设备标识: 首次生成后落盘复用。服务端据此把"短时间内反复使用"识别为同一游客，
#    窗口内直接复用既有游客换发令牌，而不是每次新建（详见 references/guest-access.md）。
FP_FILE="$(dirname "$OUT")/device.id"
if [ ! -s "$FP_FILE" ]; then
  python3 -c 'import secrets; print(secrets.token_hex(16))' > "$FP_FILE"
fi
secure_file "$FP_FILE"
FP="$(cat "$FP_FILE")"

# ③ 取一次性挑战（difficulty 一般为 16）
CHAL="$(curl -sS --max-time 20 "$BASE/bff/v1/guest-access/challenge")"
read -r CH DIFF <<<"$(printf '%s' "$CHAL" | python3 -c '
import json, sys
d = json.load(sys.stdin).get("data") or {}
print(d.get("challenge", ""), d.get("difficulty", ""))
')"
if [ -z "$CH" ] || [ -z "$DIFF" ]; then
  echo "取挑战失败（服务端可能未开放免凭据创建, 如 404 FEATURE_DISABLED）：$CHAL" >&2
  exit 1
fi

# ④ 解 PoW
NONCE="$(python3 "$DIR/pow_solve.py" "$CH" "$DIFF")"

# ⑤ 创建游客（source 固定 "web" 是公开通道的要求；挑战一次性，重复提交会被拒）
curl -sS --max-time 20 -X POST "$BASE/bff/v1/guest-access" \
  -H 'Content-Type: application/json' \
  -d "{\"source\":\"web\",\"skillId\":\"$SKILL_ID\",\"skillCode\":\"$SKILL_CODE\",\"deviceFingerprint\":\"$FP\",\"pow\":{\"challenge\":\"$CH\",\"nonce\":\"$NONCE\"}}" \
  -o "$TMP"

# ⑥ 成功才落盘：避免把错误响应写进缓存（否则下一次会拿错误体当缓存用）
if TOKEN="$(emit_token "$TMP")"; then
  mv "$TMP" "$OUT"
  secure_file "$OUT"
  printf '%s\n' "$TOKEN"
else
  rm -f "$TMP"
  exit 1
fi

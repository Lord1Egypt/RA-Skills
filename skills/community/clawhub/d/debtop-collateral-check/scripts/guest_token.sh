#!/usr/bin/env bash
# 取游客令牌：**先复用缓存**（刷新），缓存不可用才新建 —— 同一个用户短时间反复使用
# 只会换发令牌，不会每次都建出一个新游客。
#
# 用法:
#   bash scripts/guest_token.sh [输出文件] [BASE] [客户端标识] [技能包标识]
#   默认输出 $HOME/.cache/debtop/guest.json, 默认 BASE https://agent.debtop.com
#
# 退出码: 0 成功（令牌**只写入输出文件**, 不再打印到 stdout）；非 0 失败（stderr 为原因, 含服务端错误码）。
#   64 = 拒绝执行（地址不在白名单 / 输出路径越界 / 远端字段不合法）
# 注意: 只有缓存不可用时才会创建游客（配额: 单 IP 3 次/小时、全局 500 次/天）,
#       不要把本脚本当"连通性探测"反复执行。
#
# 安全约束（远端响应与调用方入参一律当不可信输入）:
#   ① 地址白名单: BASE 必须是 https 且主机恰为 ALLOWED_HOST, 否则中止 —— 令牌只发给本服务;
#   ② 输出路径收敛: 输出文件解析后必须落在 CACHE_ROOT 之内, 且不得是符号链接;
#   ③ 请求体用 JSON 序列化生成（不做字符串拼接）: 远端字段含引号也无法注入报文;
#   ④ 令牌不打印到 stdout: 避免进入命令行（ps 可见）、工具输出与会话记录;
#      调用方从 0600 的输出文件读取, 用 curl -K 配置文件传 Authorization 头。
set -euo pipefail

# 凭据落盘的权限约束：guest.json 里是可直接调用后端的 access/refresh token 与设备标识,
# 等同口令, 一律按私密文件处理。
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

# 端点白名单: 本服务的域名（固定值, 不接受调用方改写）。任何带令牌的请求都会先校验。
ALLOWED_HOST="agent.debtop.com"
# 缓存根目录: 输出文件必须落在它之内; 需要改位置时由运行方设置 DEBTOP_CACHE_DIR
# （例如把它指到会话工作区内）, 而不是由调用方随意指定绝对路径。
CACHE_ROOT="${DEBTOP_CACHE_DIR:-$HOME/.cache/debtop}"
# PoW 求解护栏（难度与时间上限; 远端返回异常难度时直接拒绝, 不做长时间求解）
POW_MAX_DIFFICULTY="${DEBTOP_POW_MAX_DIFFICULTY:-20}"
POW_MAX_SECONDS="${DEBTOP_POW_MAX_SECONDS:-30}"
case "$POW_MAX_DIFFICULTY" in
  "" | *[!0-9]*)
    echo "拒绝执行: DEBTOP_POW_MAX_DIFFICULTY 必须是非负整数（bit）：${POW_MAX_DIFFICULTY}" >&2
    exit 64
    ;;
esac
case "$POW_MAX_SECONDS" in
  "" | *[!0-9]*)
    echo "拒绝执行: DEBTOP_POW_MAX_SECONDS 必须是非负整数（秒）：${POW_MAX_SECONDS}" >&2
    exit 64
    ;;
esac

# 校验 URL: 必须是 https、主机恰为白名单域名、且不带 userinfo; 否则中止（退出码 64）
require_allowed_url() {
  if ! python3 - "$1" "$ALLOWED_HOST" <<'PY'
import sys
from urllib.parse import urlsplit
parts = urlsplit(sys.argv[1])
has_userinfo = parts.username is not None or parts.password is not None
ok = parts.scheme == "https" and parts.hostname == sys.argv[2] and not has_userinfo
sys.exit(0 if ok else 1)
PY
  then
    echo "拒绝执行: ${2} 的地址不在白名单内（只允许 https://${ALLOWED_HOST}）：${1}" >&2
    exit 64
  fi
}

OUT_RAW="${1:-$CACHE_ROOT/guest.json}"
BASE="${2:-https://agent.debtop.com}"
require_allowed_url "$BASE" "游客通道 BASE"
BASE="${BASE%/}"

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
SKILL_CODE="${4:-debtop-collateral-check}"
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

# 输出路径收敛: 解析真实路径后必须落在 CACHE_ROOT 之内, 且输出文件本身不得是符号链接。
# 这样"调用方/被注入的指令传入任意路径"最多只能落在本技能自己的缓存目录里。
if [ -L "$OUT_RAW" ]; then
  echo "拒绝执行: 输出路径是符号链接，已中止：${OUT_RAW}" >&2
  exit 64
fi
CACHE_ROOT="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$CACHE_ROOT")"
OUT_PARENT="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$(dirname "$OUT_RAW")")"
case "$OUT_PARENT" in
  "$CACHE_ROOT" | "$CACHE_ROOT"/*)
    ;;
  *)
    echo "拒绝执行: 输出文件必须位于 ${CACHE_ROOT} 之内（需要改位置请设置 DEBTOP_CACHE_DIR）：${OUT_RAW}" >&2
    exit 64
    ;;
esac
OUT="$OUT_PARENT/$(basename "$OUT_RAW")"

# 缓存目录: 本次新建时直接建为 0700; 已存在的目录不动（可能是共享目录, 改权限会伤到别处）。
# 老版本以宽松权限落过盘的缓存文件, 下面用 secure_file 就地收紧到 0600。
if [ ! -d "$OUT_PARENT" ]; then
  mkdir -p -m 700 "$OUT_PARENT"
fi

# 只收紧"已存在的普通文件"; 符号链接与特殊文件跳过, 避免改到别处的目标
secure_file() {
  if [ -f "$1" ] && [ ! -L "$1" ]; then
    chmod 600 "$1" 2>/dev/null || true
  fi
}
secure_file "$OUT"

# 同一份缓存必须串行使用: refresh 一次性轮换, 并发刷新会被判重放并撤销整条授权链。
# 优先用 flock; 平台没有 flock（如 macOS 默认）时退化为 mkdir 原子锁 + 退避重试, 依然串行。
if command -v flock >/dev/null 2>&1; then
  exec 9>"$OUT.lock"
  flock 9
else
  LOCK_DIR="$OUT.lock.d"
  waited=0
  while ! mkdir "$LOCK_DIR" 2>/dev/null; do
    # 残留锁（超过 2 分钟未释放）视为上一轮异常退出留下的, 直接接管
    if [ -n "$(find "$LOCK_DIR" -maxdepth 0 -mmin +2 2>/dev/null)" ]; then
      rm -rf "$LOCK_DIR"
      continue
    fi
    if [ "$waited" -ge 60 ]; then
      echo "等待缓存锁超时（${LOCK_DIR}）：请确认没有其它会话正在刷新同一份缓存" >&2
      exit 1
    fi
    sleep 0.5
    waited=$((waited + 1))
  done
  trap 'rm -rf "$LOCK_DIR"' EXIT
fi

# 临时文件按进程唯一（mktemp 同时保证 0600）: 并发时不会互相覆盖或删掉对方的临时文件
TMP="$(mktemp "$OUT_PARENT/guest.json.XXXXXX")"

# 从响应文件取 accessToken: 成功后打印到 stdout（仅供命令替换内部捕获, 不要展示给用户）;
# 失败把服务端错误打到 stderr 并返回 1 —— 因此"错误响应"永远走不到落盘那一步。
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

# 请求体一律用 JSON 序列化生成（绝不字符串拼接）: 远端字段含引号/反斜杠也无法注入或覆盖字段

# ① 复用缓存: 本机取过令牌且 refreshToken 仍有效 → 刷新（一次性轮换 → 必须原地覆盖写回）。
#    刷新失败静默落到"新建": 服务端在同一设备标识的去重窗口内会复用既有游客换发令牌，
#    不会因此多建一个游客。
if [ -s "$OUT" ]; then
  RT="$(read_refresh "$OUT")"
  if [ -n "$RT" ]; then
    REFRESH_BODY="$(REFRESH_TOKEN="$RT" python3 -c 'import json, os; print(json.dumps({"refreshToken": os.environ["REFRESH_TOKEN"]}))')"
    if curl -sS --max-time 20 -X POST \
         -H 'Content-Type: application/json' \
         -d "$REFRESH_BODY" -o "$TMP" \
         "$BASE/bff/v1/guest-access/refresh" \
       && TOKEN="$(emit_token "$TMP" 2>/dev/null)"; then
      mv "$TMP" "$OUT"
      secure_file "$OUT"
      echo "已刷新游客令牌并写回：${OUT}（权限 0600；未新建游客）" >&2
      exit 0
    fi
    rm -f "$TMP"
  fi
fi

# ② 稳定设备标识: 首次生成后落盘复用。服务端据此把"短时间内反复使用"识别为同一游客，
#    窗口内直接复用既有游客换发令牌，而不是每次新建（详见 references/guest-access.md）。
#    它是本机随机生成的匿名标识（不含硬件与个人信息），创建游客时作为 deviceFingerprint 上报。
FP_FILE="$OUT_PARENT/device.id"
if [ -L "$FP_FILE" ]; then
  echo "拒绝执行: 设备标识文件是符号链接，已中止：${FP_FILE}" >&2
  exit 64
fi
if [ ! -s "$FP_FILE" ]; then
  python3 -c 'import secrets; print(secrets.token_hex(16))' > "$FP_FILE"
fi
secure_file "$FP_FILE"
FP="$(cat "$FP_FILE")"

# ③ 取一次性挑战（difficulty 一般为 16）
CHAL_JSON="$(curl -sS --max-time 20 "$BASE/bff/v1/guest-access/challenge")"
read -r CH DIFF <<<"$(printf '%s' "$CHAL_JSON" | python3 -c '
import json, sys
d = json.load(sys.stdin).get("data") or {}
print(d.get("challenge", ""), d.get("difficulty", ""))
')"
if [ -z "$CH" ] || [ -z "$DIFF" ]; then
  echo "取挑战失败（服务端可能未开放免凭据创建, 如 404 FEATURE_DISABLED）：$CHAL_JSON" >&2
  exit 1
fi

# 远端返回的 challenge / difficulty 一律当不可信输入: 先做字符白名单与范围校验,
# 再交给求解器（求解器内部还有时间与迭代上限, 不会无限占用 CPU）。
case "$CH" in
  "" | *[!A-Za-z0-9._~+/=-]*)
    echo "拒绝执行: 挑战串含非预期字符，已中止（不接受远端注入）：${CH}" >&2
    exit 64
    ;;
esac
case "$DIFF" in
  "" | *[!0-9]*)
    echo "拒绝执行: 难度值不是整数，已中止：${DIFF}" >&2
    exit 64
    ;;
esac
if [ "$DIFF" -gt "$POW_MAX_DIFFICULTY" ]; then
  echo "拒绝执行: 难度值 ${DIFF} bit 超出上限 ${POW_MAX_DIFFICULTY} bit，已中止（不给远端异常难度值留出长时间占用 CPU 的机会）" >&2
  exit 64
fi

# ④ 解 PoW（外面再套一层硬超时; 求解器自身也有 --max-seconds 与迭代上限）
if command -v timeout >/dev/null 2>&1; then
  POW_CMD=(timeout "$POW_MAX_SECONDS" python3 "$DIR/pow_solve.py" "$CH" "$DIFF" --max-seconds "$POW_MAX_SECONDS")
else
  POW_CMD=(python3 "$DIR/pow_solve.py" "$CH" "$DIFF" --max-seconds "$POW_MAX_SECONDS")
fi
if ! NONCE="$("${POW_CMD[@]}")"; then
  echo "解 PoW 失败或达上限（难度 ${DIFF} bit / 上限 ${POW_MAX_SECONDS}s）：不解出就不继续，也不占用更多 CPU" >&2
  exit 1
fi
case "$NONCE" in
  "" | *[!0-9]*)
    echo "拒绝执行: 求解结果不是十进制整数，已中止：${NONCE}" >&2
    exit 64
    ;;
esac

# ⑤ 创建游客（source 固定 "web" 是公开通道的要求；挑战一次性，重复提交会被拒）
CREATE_BODY="$(SKILL_ID="$SKILL_ID" SKILL_CODE="$SKILL_CODE" DEVICE_FP="$FP" CHALLENGE="$CH" POW_NONCE="$NONCE" python3 - <<'PY'
import json, os
print(json.dumps({
    "source": "web",
    "skillId": os.environ["SKILL_ID"],
    "skillCode": os.environ["SKILL_CODE"],
    "deviceFingerprint": os.environ["DEVICE_FP"],
    "pow": {"challenge": os.environ["CHALLENGE"], "nonce": int(os.environ["POW_NONCE"])},
}, ensure_ascii=False))
PY
)"
curl -sS --max-time 20 -X POST "$BASE/bff/v1/guest-access" \
  -H 'Content-Type: application/json' \
  -d "$CREATE_BODY" -o "$TMP"

# ⑥ 成功才落盘：避免把错误响应写进缓存（否则下一次会拿错误体当缓存用）
if TOKEN="$(emit_token "$TMP")"; then
  mv "$TMP" "$OUT"
  secure_file "$OUT"
  echo "游客令牌已写入：${OUT}（权限 0600；请从该文件读取 accessToken，用 curl -K 配置文件传 Authorization 头，不要打印到会话输出）" >&2
else
  rm -f "$TMP"
  exit 1
fi

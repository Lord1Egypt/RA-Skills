#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPEC_FILE="${SCRIPT_DIR}/install-spec.sh"

if [[ ! -f "$SPEC_FILE" ]]; then
  printf '安装中止：缺少安装参数文件：%s\n' "$SPEC_FILE" >&2
  printf '修复建议：请重新解压完整的单 Skill 安装包。\n' >&2
  exit 1
fi

# Each skill owns only these product-specific values. All installation logic
# stays in this shared script.
# shellcheck source=/dev/null
source "$SPEC_FILE"

required_spec_vars=(
  SKILL_NAME
  SKILL_DISPLAY_NAME
  CATALOG_PATH
  CATALOG_LABEL
  SMOKE_PATH
  SMOKE_BODY_JSON
)
for spec_var in "${required_spec_vars[@]}"; do
  if [[ -z "${!spec_var:-}" ]]; then
    printf '安装中止：%s 缺少参数 %s。\n' "$SPEC_FILE" "$spec_var" >&2
    exit 1
  fi
done

if [[ "$SKILL_NAME" != "$(basename "$SCRIPT_DIR")" ]]; then
  printf '安装中止：安装目录与 SKILL_NAME 不一致。\n' >&2
  exit 1
fi
if [[ "$CATALOG_PATH" == /* || "$CATALOG_PATH" == *..* ]]; then
  printf '安装中止：CATALOG_PATH 必须是 Skill 内的安全相对路径。\n' >&2
  exit 1
fi
if [[ "$SMOKE_PATH" != /* || "$SMOKE_PATH" == *"://"* || "$SMOKE_PATH" == *..* ]]; then
  printf '安装中止：SMOKE_PATH 必须是以 / 开头的安全相对路径。\n' >&2
  exit 1
fi

PACKAGE_VERSION="3.0.0"
SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-${HOME}/.openclaw/workspace/skills}"
CREDENTIALS_DIR="${HOME}/.config/index-hub"
CREDENTIALS_FILE="${CREDENTIALS_DIR}/api_key"
API_KEY="${INDEX_HUB_API_KEY:-${ETF_API_KEY:-}}"
API_KEY_PROVIDED=0
DO_INSTALL=1
VERIFY_API=1

usage() {
  printf 'Install and initialize %s v3.0.0 (%s).\n\n' "$SKILL_DISPLAY_NAME" "$SKILL_NAME"
  cat <<'EOF'
Usage:
  ./install.sh --api-key KEY
  ./install.sh

Options:
  --skills-dir DIR        Target install directory. Default: ~/.openclaw/workspace/skills
  --api-key KEY           API key. If omitted, the script prompts for it.
  --no-install            Only update the API key in already-installed files.
  --skip-api-verify       Skip the final network smoke test.
  -h, --help              Show this help.
EOF
}

stage() { printf '\n==> 阶段 %s：%s\n' "$1" "$2"; }

fail() {
  local reason="$1" fix="$2" code="${3:-1}"
  printf '\n安装中止：%s\n' "$reason" >&2
  printf '修复建议：%s\n' "$fix" >&2
  exit "$code"
}

mask_key() {
  local key="$1"
  local len=${#key}
  if (( len <= 8 )); then printf '***'; else printf '%s***%s' "${key:0:4}" "${key: -4}"; fi
}

require_file() { [[ -f "$1" ]] || fail "缺少文件：$1" "$2"; }
require_dir()  { [[ -d "$1" ]] || fail "缺少目录：$1" "$2"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills-dir) SKILLS_DIR="${2-}"; if [[ $# -ge 2 ]]; then shift 2; else shift; fi ;;
    --api-key) API_KEY="${2-}"; API_KEY_PROVIDED=1; if [[ $# -ge 2 ]]; then shift 2; else shift; fi ;;
    --no-install) DO_INSTALL=0; shift ;;
    --skip-api-verify) VERIFY_API=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; fail "未知参数：$1" "运行 ./install.sh --help 查看支持的参数。" 2 ;;
  esac
done

stage 1 "环境检测"
command -v python3 >/dev/null 2>&1 || fail "未找到 python3。" "请先安装 Python 3.8 或更高版本。"
python3 - <<'PY' || fail "Python 版本过低。" "请升级到 Python 3.8 或更高版本。"
import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)
PY
if [[ "$DO_INSTALL" -eq 1 ]]; then
  mkdir -p "$SKILLS_DIR" || fail "无法创建安装目录：$SKILLS_DIR" "使用 --skills-dir 指定一个可写目录。"
  [[ -w "$SKILLS_DIR" ]] || fail "安装目录不可写：$SKILLS_DIR" "修复目录权限或使用 --skills-dir。"
fi
printf 'Python: %s\n' "$(python3 --version 2>&1)"
printf '安装目录: %s\n' "$SKILLS_DIR"
printf '版本: %s\n' "$PACKAGE_VERSION"

stage 2 "安装包完整性检查"
require_dir  "$SCRIPT_DIR" "请重新解压安装包，确保 ${SKILL_NAME} 目录存在。"
require_file "${SCRIPT_DIR}/SKILL.md" "请重新下载安装包，确保文件完整。"
require_file "${SCRIPT_DIR}/config.py" "请重新下载安装包，确保配置文件完整。"
require_file "${SCRIPT_DIR}/guardrails.py" "请重新下载安装包，确保回答校验文件完整。"
require_file "${SCRIPT_DIR}/${CATALOG_PATH}" "请重新解压安装包，确保 ${CATALOG_LABEL} 参考文件完整。"
require_file "${SCRIPT_DIR}/scripts/api_client.py" "请重新解压安装包，确保 v3.0.0 调用工具完整。"
printf '安装包检查通过：%s\n' "$SKILL_NAME"

if [[ "$DO_INSTALL" -eq 0 ]]; then
  installed_config="${SKILLS_DIR}/${SKILL_NAME}/config.py"
  require_file "$installed_config" "请使用当前安装包的安装入口执行完整安装，不要使用 --no-install。"
  if ! grep -q 'CREDENTIALS_FILE' "$installed_config"; then
    fail "当前已安装的 ${SKILL_NAME} 使用旧版凭据配置，不能只更新 API Key。" "请使用当前安装包的安装入口执行完整安装，不要使用 --no-install。"
  fi
fi

stage 3 "初始化 API Key"
if [[ -z "$API_KEY" && -f "$CREDENTIALS_FILE" ]]; then
  IFS= read -r API_KEY < "$CREDENTIALS_FILE" || true
fi
if [[ -z "$API_KEY" && "$API_KEY_PROVIDED" -eq 0 ]]; then
  read -r -s -p "请输入 API Key: " API_KEY; printf '\n'
fi
[[ -n "$API_KEY" ]] || fail "API Key 为空。" "重新运行 ./install.sh 并按提示隐藏输入有效 key。" 2
printf 'API Key 读取成功：%s\n' "$(mask_key "$API_KEY")"

stage 4 "安装功能"
if [[ "$DO_INSTALL" -eq 1 ]]; then
  rm -rf "${SKILLS_DIR:?}/${SKILL_NAME}"
  # -L turns symlinks into ordinary files. Installed skills are
  # therefore self-contained even when this script is run from the repository.
  cp -RL "$SCRIPT_DIR" "${SKILLS_DIR}/${SKILL_NAME}" || fail "复制 ${SKILL_NAME} 失败。" "检查 ${SKILLS_DIR} 权限。"
  find "${SKILLS_DIR}/${SKILL_NAME}" \( -name '.DS_Store' -o -name '__pycache__' \) -prune -exec rm -rf {} +
  require_file "${SKILLS_DIR}/${SKILL_NAME}/SKILL.md" "复制后文件不完整，请重新安装。"
  require_file "${SKILLS_DIR}/${SKILL_NAME}/config.py" "复制后文件不完整，请重新安装。"
  require_file "${SKILLS_DIR}/${SKILL_NAME}/guardrails.py" "复制后回答校验文件缺失，请重新安装。"
  printf '已安装功能：%s\n' "$SKILL_NAME"
fi

mkdir -p "$CREDENTIALS_DIR" || fail "无法创建凭据目录：$CREDENTIALS_DIR" "检查 HOME 目录权限。"
chmod 700 "$CREDENTIALS_DIR" || fail "无法收紧凭据目录权限。" "检查 $CREDENTIALS_DIR 的所有权。"
CREDENTIALS_TMP="$(mktemp "${CREDENTIALS_FILE}.tmp.XXXXXX")" || fail "无法创建临时凭据文件。" "检查 $CREDENTIALS_DIR 的写入权限。"
chmod 600 "$CREDENTIALS_TMP" || fail "无法设置临时凭据文件权限。" "检查文件系统权限。"
printf '%s\n' "$API_KEY" > "$CREDENTIALS_TMP" || fail "无法写入凭据文件。" "检查 $CREDENTIALS_DIR 的写入权限。"
mv "$CREDENTIALS_TMP" "$CREDENTIALS_FILE" || fail "无法保存凭据文件。" "检查 $CREDENTIALS_DIR 的写入权限。"
chmod 600 "$CREDENTIALS_FILE" || fail "无法收紧凭据文件权限。" "检查 $CREDENTIALS_FILE 的所有权。"
printf 'API Key 已保存到独立凭据文件：%s\n' "$CREDENTIALS_FILE"

stage 5 "能力校验"
config_path="${SKILLS_DIR}/${SKILL_NAME}/config.py"
require_file "$config_path" "确认安装目录中的 config.py 存在。"

BASE_URL="$(sed -nE 's/^BASE_URL[[:space:]]*=[[:space:]]*"([^"]+)".*/\1/p' "$config_path" | head -n 1)"
CALLER_TYPE="$(sed -nE 's/^CALLER_TYPE[[:space:]]*=[[:space:]]*"([^"]+)".*/\1/p' "$config_path" | head -n 1)"
if [[ -z "$CALLER_TYPE" ]]; then CALLER_TYPE="external"; fi

[[ "$BASE_URL" == https://* ]] || fail "本地配置校验失败：BASE_URL 无效。" "检查 config.py 中的 BASE_URL。"
[[ -n "$API_KEY" ]] || fail "本地配置校验失败：API_KEY 为空。" "请重新运行 ./install.sh 并按提示输入。"
printf '本地配置校验通过。\n'

if [[ "$VERIFY_API" -eq 1 ]]; then
  python3 - "$BASE_URL" "$API_KEY" "$CALLER_TYPE" "$SMOKE_PATH" "$SMOKE_BODY_JSON" <<'PY' || fail "接口连通性校验失败。" "确认网络、API Key 有效；离线环境可加 --skip-api-verify。"
import json
import ssl
import sys
import urllib.request

base_url, api_key, caller_type, path, payload_json = sys.argv[1:]
payload = json.loads(payload_json)
if not isinstance(payload, dict):
    raise ValueError("SMOKE_BODY_JSON must be a JSON object")

request = urllib.request.Request(
    base_url + path,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Caller-Type": caller_type,
    },
    method="POST",
)
with urllib.request.urlopen(request, context=ssl.create_default_context(), timeout=20) as response:
    body = json.loads(response.read())
if body.get("success") is not True or body.get("code") not in (0, "0", "0000", None):
    raise RuntimeError(body.get("message") or str(body)[:200])
PY
  printf '接口连通性校验通过。\n'
else
  printf '已跳过接口连通性校验。\n'
fi

stage 6 "完成"
printf '安装完成。\n'
printf '版本: %s\n' "$PACKAGE_VERSION"
printf '安装目录: %s\n' "$SKILLS_DIR"
printf '可用功能: %s\n' "$SKILL_NAME"

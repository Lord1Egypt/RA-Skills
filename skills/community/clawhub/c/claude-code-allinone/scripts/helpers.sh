#!/usr/bin/env bash
# helpers.sh — claude-code-allinone 共享工具函数
#
# 使用方式: . "$SCRIPT_DIR/helpers.sh"
#
# 不直接执行,只提供给其他脚本 source。

# ============================================================
# 常量
# ============================================================
CC_MIN_VERSION="2.1.0"
CC_NPM_PACKAGE="@anthropic-ai/claude-code"

CC_HOME="$HOME/.claude"
CC_PROFILES_DIR="$CC_HOME/profiles"
CC_SETTINGS="$CC_HOME/settings.json"
CC_TOKEN_FILE="$CC_HOME/.token"
CC_ACTIVE_FILE="$CC_HOME/active-profile"
CC_USER_JSON="$HOME/.claude.json"

# ============================================================
# 日志辅助
# ============================================================
cc_log()  { printf '\033[1;36m[claude-code]\033[0m %s\n' "$*"; }
cc_warn() { printf '\033[1;33m[claude-code]\033[0m %s\n' "$*"; }
cc_err()  { printf '\033[1;31m[claude-code]\033[0m %s\n' "$*" >&2; }

# ============================================================
# 版本比较: $1 >= $2 ?
# ============================================================
cc_version_ge() {
  [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

# ============================================================
# 安全 JSON 写文件 (没装 jq 也能用)
# ============================================================
cc_write_json_atomic() {
  local target="$1"
  local content="$2"
  local tmp
  tmp="$(mktemp "${target}.XXXXXX")"
  printf '%s' "$content" > "$tmp"
  mv -f "$tmp" "$target"
  chmod 600 "$target" 2>/dev/null || true
}

# ============================================================
# 备份现有文件 (不是软链才备份)
# ============================================================
cc_backup_if_needed() {
  local f="$1"
  if [ -f "$f" ] && [ ! -L "$f" ]; then
    local bak="${f}.bak.$(date +%Y%m%d_%H%M%S)"
    cp "$f" "$bak"
    cc_log "  → 已备份 $f → $bak"
  fi
}

# ============================================================
# 把 ~/.claude.json 标记 hasCompletedOnboarding=true
# 没装 jq 也得能干活: 退化为 sed 改写或最小化新建
# ============================================================
cc_ensure_onboarding_completed() {
  if [ ! -f "$CC_USER_JSON" ]; then
    cc_write_json_atomic "$CC_USER_JSON" '{"hasCompletedOnboarding":true}'
    return 0
  fi

  if command -v jq >/dev/null 2>&1; then
    local tmp
    tmp="$(mktemp "${CC_USER_JSON}.XXXXXX")"
    jq '. + {"hasCompletedOnboarding": true}' "$CC_USER_JSON" > "$tmp" 2>/dev/null \
      && mv -f "$tmp" "$CC_USER_JSON" \
      || { rm -f "$tmp"; return 1; }
    chmod 600 "$CC_USER_JSON" 2>/dev/null || true
    return 0
  fi

  # 无 jq 兜底: 简单字符串替换
  if grep -q '"hasCompletedOnboarding"' "$CC_USER_JSON"; then
    sed -i 's/"hasCompletedOnboarding"\s*:\s*false/"hasCompletedOnboarding": true/' "$CC_USER_JSON"
  else
    # 在最后一个 } 之前插入字段
    sed -i '$ s/}$/,"hasCompletedOnboarding":true}/' "$CC_USER_JSON"
  fi
}

# ============================================================
# 写 Key 到 .token 文件 (settings.json 的 apiKeyHelper 会读它)
# ============================================================
cc_write_token() {
  local key="$1"
  mkdir -p "$CC_HOME"
  printf '%s' "$key" > "$CC_TOKEN_FILE"
  chmod 600 "$CC_TOKEN_FILE" 2>/dev/null || true
}

# ============================================================
# 把模板 profile 渲染到 ~/.claude/profiles/<name>.json
# 第三个起为 sed 替换对 (key=value)
# ============================================================
cc_render_profile() {
  local src="$1" dst="$2"
  shift 2
  cp "$src" "$dst"
  while [ $# -gt 0 ]; do
    local pair="$1"; shift
    local k="${pair%%=*}"
    local v="${pair#*=}"
    # 用 | 作分隔符避免 URL 里的 / 把 sed 搞坏
    local v_esc
    v_esc="$(printf '%s' "$v" | sed -e 's/[\&|]/\\&/g')"
    sed -i "s|$k|$v_esc|g" "$dst"
  done
  chmod 600 "$dst" 2>/dev/null || true
}

# ============================================================
# 写 Key 到 ~/.bashrc (供调试和 fallback 使用)
# 主链路读 .token 文件,不依赖此变量
# ============================================================
cc_persist_env_to_bashrc() {
  local var_name="$1" var_val="$2"
  sed -i "/^export $var_name=/d" "$HOME/.bashrc" 2>/dev/null || true
  echo "export $var_name=\"$var_val\"" >> "$HOME/.bashrc"
  export "$var_name=$var_val"
}

# ============================================================
# 把当前 active profile 名写入 marker
# ============================================================
cc_set_active_profile() {
  local name="$1"
  mkdir -p "$CC_HOME"
  echo "$name" > "$CC_ACTIVE_FILE"
}

# ============================================================
# Key 格式自检 — 不联网,本地正则
# 火山方舟 Key 通常是字母数字和连字符,长度 20+
# 仅用于挡掉"明显贴错"的输入(空格、换行、含中文等)
# 返回 0 = 看起来像个 Key;1 = 明显不像
# ============================================================
cc_format_check_key() {
  local key="$1"
  [ -n "$key" ] || return 1
  # 长度至少 20
  [ "${#key}" -ge 20 ] || return 1
  # 仅允许字母数字 + 连字符 + 下划线 + 点
  echo "$key" | grep -qE '^[A-Za-z0-9._-]+$' || return 1
  return 0
}

# ============================================================
# Key 活性预校验 — 抗网络抖动
# 用法: cc_ping_key <key> <base_url>
# 返回:
#   0 = 联通且鉴权 OK (拿到 2xx/4xx 中的非鉴权码)
#   1 = 明确鉴权失败 (HTTP 401 / 403)
#   2 = 网络抖动,无法判断 (3 次重试都没拿到明确答案,放行写盘)
#
# 设计原则:
#   - 用 /models endpoint,不消耗推理 token,不计费
#   - 单次超时 3 秒,最多 3 次重试,最坏 9 秒
#   - 只看到 401/403 才报错,其它一律放行
# ============================================================
cc_ping_key() {
  local key="$1" base_url="$2"
  local code
  local i
  for i in 1 2 3; do
    code=$(curl -sS -o /dev/null -w "%{http_code}" \
                --max-time 3 \
                -H "Authorization: Bearer $key" \
                "${base_url%/}/models" 2>/dev/null || echo "000")
    case "$code" in
      401|403)
        return 1
        ;;
      2*|400|404|405|422)
        return 0
        ;;
      000|408|429|5*)
        sleep 1
        continue
        ;;
      *)
        # 未知状态码,保守视为联通
        return 0
        ;;
    esac
  done
  # 三次都没拿到明确答案,视为网络问题,放行
  return 2
}

# ============================================================
# 读取 settings.json 中某个 env key 的值 (无 jq 兜底)
# ============================================================
cc_read_env_value() {
  local key="$1"
  [ -f "$CC_SETTINGS" ] || { echo ""; return; }
  if command -v jq >/dev/null 2>&1; then
    jq -r ".env.\"$key\" // empty" "$CC_SETTINGS" 2>/dev/null
  else
    grep -E "\"$key\"\s*:" "$CC_SETTINGS" \
      | head -1 \
      | sed -E 's/.*"'"$key"'"\s*:\s*"([^"]*)".*/\1/'
  fi
}

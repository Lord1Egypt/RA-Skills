#!/usr/bin/env bash
# relay-helper.sh — codex-relay 共享工具函数
#
# 使用方式: source 这个文件,然后调用其中的函数。
#
# 提供的函数:
#   profile_relay_port <profile>     — 返回该 profile 用的 relay 端口(arkv3 返回空)
#   profile_relay_upstream <profile> — 返回该 profile 的上游 URL
#   profile_env_key_name <profile>   — 返回该 profile 用的环境变量名
#   probe_responses_support <url> <key> — 探测上游是否原生支持 Responses API(0=支持, 1=不支持)
#   ensure_codex_relay_installed     — 确保 codex-relay 已安装(自动 pip install)
#   start_relay <profile> <port> <upstream> — 后台启动 relay,等待端口就绪
#   stop_relay_on_port <port>        — 停止指定端口的 relay
#   relay_running <port>             — 端口上是否有服务在跑

# ============================================================
# Profile → 端口/上游 映射
# ============================================================
profile_relay_port() {
  case "$1" in
    agentplan)  echo "4446" ;;
    codingplan) echo "4450" ;;
    kimi)       echo "4447" ;;
    deepseek)   echo "4448" ;;
    custom)     echo "4449" ;;
    arkv3)      echo "" ;;       # arkv3 直连,不用 relay
    *)          echo "" ;;
  esac
}

profile_relay_upstream() {
  case "$1" in
    agentplan)  echo "https://ark.cn-beijing.volces.com/api/plan/v3" ;;
    codingplan) echo "https://ark.cn-beijing.volces.com/api/coding/v3" ;;
    kimi)       echo "https://api.moonshot.cn/v1" ;;
    deepseek)   echo "https://api.deepseek.com/v1" ;;
    custom)     echo "${CUSTOM_UPSTREAM:-}" ;;   # custom 由调用方通过环境变量传入
    *)          echo "" ;;
  esac
}

profile_env_key_name() {
  case "$1" in
    agentplan)  echo "ARK_API_KEY" ;;
    codingplan) echo "ARK_API_KEY" ;;
    kimi)       echo "MOONSHOT_API_KEY" ;;
    deepseek)   echo "DEEPSEEK_API_KEY" ;;
    arkv3)      echo "ARK_V3_API_KEY" ;;
    custom)     echo "CUSTOM_API_KEY" ;;
    *)          echo "" ;;
  esac
}

# ============================================================
# Key 格式自检 — 不联网,本地正则
# 仅用于挡掉"明显贴错"的输入(空格、换行、含中文等)
# 返回 0 = 看起来像个 Key;1 = 明显不像
# ============================================================
codex_format_check_key() {
  local key="$1"
  [ -n "$key" ] || return 1
  [ "${#key}" -ge 20 ] || return 1
  echo "$key" | grep -qE '^[A-Za-z0-9._-]+$' || return 1
  return 0
}

# ============================================================
# Key 活性预校验 — 抗网络抖动
# 用法: codex_ping_key <key> <base_url>
# 返回:
#   0 = 联通且鉴权 OK (拿到 2xx/4xx 中的非鉴权码)
#   1 = 明确鉴权失败 (HTTP 401 / 403)
#   2 = 网络抖动,无法判断 (3 次重试都没拿到明确答案,放行)
# ============================================================
codex_ping_key() {
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
        return 0
        ;;
    esac
  done
  return 2
}

# ============================================================
# 探测上游是否支持 OpenAI Responses API
# ============================================================
# 用法: probe_responses_support <base_url> <api_key>
# 返回: 0 = 支持 Responses(可直连)
#       1 = 不支持(应过 relay)
probe_responses_support() {
  local base_url="$1"
  local api_key="$2"
  local code

  # 去掉末尾斜杠
  base_url="${base_url%/}"

  code="$(curl -s -o /dev/null -w '%{http_code}' \
    --max-time 6 \
    -X POST "${base_url}/responses" \
    -H "Authorization: Bearer ${api_key}" \
    -H "Content-Type: application/json" \
    -d '{"model":"probe","input":"ping"}' 2>/dev/null || echo "000")"

  # 404 = 该端点不存在 → 不支持 Responses
  # 401/403 = 鉴权问题但端点存在 → 支持(只是 Key 不一定对)
  # 400/422 = 参数问题但端点存在 → 支持
  # 200 = 正常返回(model 名不对也能通过 schema 校验) → 支持
  # 000/其它 = 网络不通,无法判断,保守按"不支持"处理(走 relay 更安全)
  case "$code" in
    404)             return 1 ;;
    200|400|401|403|422) return 0 ;;
    *)               return 1 ;;
  esac
}

# ============================================================
# 确保 codex-relay 已安装
# ============================================================
ensure_codex_relay_installed() {
  if command -v codex-relay >/dev/null 2>&1; then
    return 0
  fi

  # PATH 可能没加载,先手动加
  export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
  if command -v codex-relay >/dev/null 2>&1; then
    return 0
  fi

  echo "正在安装 codex-relay..."
  pip install --user --break-system-packages codex-relay >/dev/null 2>&1 || {
    echo "❌ codex-relay 安装失败。请手动执行: pip install --user --break-system-packages codex-relay" >&2
    return 1
  }

  # 确保 ~/.local/bin 在 PATH 中
  if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  fi

  command -v codex-relay >/dev/null 2>&1 || {
    echo "❌ codex-relay 安装完但找不到命令。请检查 PATH。" >&2
    return 1
  }
}

# ============================================================
# 端口检查
# ============================================================
relay_running() {
  local port="$1"
  (echo > /dev/tcp/127.0.0.1/"$port") >/dev/null 2>&1
}

# ============================================================
# 启动 relay
# ============================================================
# 用法: start_relay <profile> <port> <upstream_url>
start_relay() {
  local profile="$1"
  local port="$2"
  local upstream="$3"
  local key_name
  key_name="$(profile_env_key_name "$profile")"

  if [ -z "$port" ] || [ -z "$upstream" ]; then
    echo "❌ start_relay: 缺少 port 或 upstream 参数" >&2
    return 1
  fi

  # 端口已经有服务,直接复用
  if relay_running "$port"; then
    return 0
  fi

  ensure_codex_relay_installed || return 1

  # 加载 Key 到环境(当前 shell 可能还没 source .bashrc)
  if [ -n "$key_name" ] && [ -z "$(eval echo \$$key_name)" ]; then
    local key_line
    key_line="$(grep "^export ${key_name}=" "$HOME/.bashrc" 2>/dev/null | tail -1 || true)"
    [ -n "$key_line" ] && eval "$key_line"
  fi

  # ⚠️ 关键修复(v3.2):codex-relay 不会从客户端请求里提取 Authorization,
  # 必须通过 CODEX_RELAY_API_KEY 环境变量把 Key 注入给 relay 进程,否则上游会 401。
  local key_value=""
  if [ -n "$key_name" ]; then
    key_value="$(eval echo \"\$$key_name\")"
  fi
  if [ -z "$key_value" ]; then
    echo "❌ start_relay: 找不到环境变量 $key_name 的值。请先确保 Key 已写入 ~/.bashrc 并 export 到当前 shell。" >&2
    return 1
  fi

  # 后台启动
  local log_file="$HOME/.codex-relay-${profile}.log"
  CODEX_RELAY_API_KEY="$key_value" nohup codex-relay \
    --port "$port" \
    --upstream "$upstream" \
    > "$log_file" 2>&1 &

  # 最多等 5 秒
  for i in 1 2 3 4 5; do
    sleep 1
    if relay_running "$port"; then
      return 0
    fi
  done

  echo "❌ codex-relay (profile=$profile, port=$port) 启动失败。日志: $log_file" >&2
  return 1
}

# ============================================================
# 停止 relay
# ============================================================
stop_relay_on_port() {
  local port="$1"
  pkill -f "codex-relay --port $port" 2>/dev/null || true
  sleep 1
}

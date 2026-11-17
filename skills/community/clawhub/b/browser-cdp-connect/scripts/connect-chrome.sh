#!/usr/bin/env bash
# connect-chrome.sh — 自动发现用户 Chrome 的 CDP 端口并连接 Hermes browser 工具
#
# 原理：Chrome 通过 chrome://inspect 开远程调试后，会在 user-data-dir 下
# 生成 DevToolsActivePort 文件（第一行端口号，第二行 wsPath UUID）。
# 本脚本读这个文件，拼出 ws:// URL，写入 Hermes config 的 browser.cdp_url，
# 并设置 BROWSER_CDP_URL 环境变量实现 live override（当前 session 立即生效）。
#
# 用法：bash connect-chrome.sh
# 退出码：0=成功，1=Chrome 未开远程调试

set -e

# --- 定位 DevToolsActivePort 文件 ---
PORT_FILE=""
if [ -n "$LOCALAPPDATA" ]; then
    # Windows (git-bash)
    PORT_FILE="$LOCALAPPDATA/Google/Chrome/User Data/DevToolsActivePort"
elif [ -n "$HOME" ]; then
    # macOS / Linux
    case "$(uname -s)" in
        Darwin*) PORT_FILE="$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort" ;;
        Linux*)  PORT_FILE="$HOME/.config/google-chrome/DevToolsActivePort" ;;
    esac
fi

if [ -z "$PORT_FILE" ] || [ ! -f "$PORT_FILE" ]; then
    echo "chrome: not connected"
    echo "  请在 Chrome 地址栏打开 chrome://inspect/#remote-debugging"
    echo "  勾选 'Allow remote debugging for this browser instance'"
    echo "  可能需要重启 Chrome"
    exit 1
fi

# --- 读取端口和 wsPath ---
# 文件格式：第一行端口号，第二行 /devtools/browser/<uuid>
PORT=$(head -1 "$PORT_FILE" | tr -d '[:space:]')
WS_PATH=$(sed -n '2p' "$PORT_FILE" | tr -d '[:space:]')

if [ -z "$PORT" ] || [ "$PORT" -lt 1 ] 2>/dev/null; then
    echo "chrome: invalid port in $PORT_FILE"
    exit 1
fi

if [ -z "$WS_PATH" ]; then
    # 只有端口号没有 wsPath（命令行 --remote-debugging-port 方式）
    WS_URL="ws://127.0.0.1:${PORT}/devtools/browser"
else
    WS_URL="ws://127.0.0.1:${PORT}${WS_PATH}"
fi

echo "chrome: ok (port $PORT, wsPath ${WS_PATH:-<none>})"

# --- 端口探测（确认 Chrome 真在监听）---
if ! (echo > /dev/tcp/127.0.0.1/$PORT) 2>/dev/null; then
    # /dev/tcp 不可用时回退到 netstat
    if command -v netstat >/dev/null 2>&1; then
        if ! netstat -an 2>/dev/null | grep -q ":$PORT .*LISTEN"; then
            echo "chrome: port $PORT not listening (Chrome 可能已关闭)"
            exit 1
        fi
    else
        echo "chrome: cannot verify port $PORT (no /dev/tcp, no netstat)"
    fi
fi

# --- 写入 Hermes config ---
WS_URL_FOR_CONFIG="$WS_URL"
if command -v hermes >/dev/null 2>&1; then
    hermes config set browser.cdp_url "$WS_URL_FOR_CONFIG" 2>&1 | grep -v "^$" || true
    echo "config: browser.cdp_url set"
else
    # hermes 不在 PATH 时手动写（fallback）
    CONFIG_PATH="${HERMES_CONFIG:-$LOCALAPPDATA/hermes/config.yaml}"
    if [ -f "$CONFIG_PATH" ]; then
        # 用 python 改 yaml（避免 sed 转义问题）
        python -c "
import yaml, sys
path = r'$CONFIG_PATH'
with open(path, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)
cfg.setdefault('browser', {})['cdp_url'] = r'$WS_URL_FOR_CONFIG'
with open(path, 'w', encoding='utf-8') as f:
    yaml.dump(cfg, f, allow_unicode=True, default_flow_style=False)
print('config: browser.cdp_url set (manual)')
" 2>&1 || echo "config: failed to write (edit $CONFIG_PATH manually)"
    else
        echo "config: $CONFIG_PATH not found, set HERMES_CONFIG env or edit manually"
    fi
fi

# --- Live override（当前 session 立即生效）---
export BROWSER_CDP_URL="$WS_URL"
echo "live:   BROWSER_CDP_URL exported (current session)"
echo ""
echo "ws_url: $WS_URL"
echo ""
echo "✓ 连接成功。browser_navigate 现在用你的日常 Chrome（带登录态）。"
echo "  验证: stealth_features 应含 'cdp_override'。"
echo "  完成后切回 headless: hermes config set browser.cdp_url ''"
echo ""
echo "⚠️  注意：Chrome 重启后 wsPath UUID 会变，需重跑此脚本。"

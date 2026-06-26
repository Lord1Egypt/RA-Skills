#!/bin/bash
# Feishu Gateway 一键恢复脚本
# 用途：容器重装 / venv 重建后恢复飞书 bot 连接 + 飞书端显示优化
# 用法：bash scripts/feishu-gateway-recover.sh
#
# 使用前请确认环境变量已在 ~/.hermes/.env 中正确配置：
#   FEISHU_APP_ID, FEISHU_APP_SECRET

set -e

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
# hermes venv 路径 — 根据你的安装方式调整
HERMES_VENV="${HERMES_VENV:-$(dirname $(which hermes) 2>/dev/null)/../.venv}"
if [ ! -d "$HERMES_VENV" ]; then
    # 常见安装路径
    HERMES_VENV="/usr/local/lib/hermes-agent/.venv"
fi
LOG="$HERMES_HOME/logs/gateway.log"
LOCK_DIR="$HOME/.local/state/hermes/gateway-locks"
CONFIG="$HERMES_HOME/config.yaml"

echo "=== 1/5 安装 lark-oapi（飞书 SDK）==="
if "$HERMES_VENV/bin/python" -c "import lark_oapi" 2>/dev/null; then
    echo "  ✓ 已安装"
else
    "$HERMES_VENV/bin/python" -m ensurepip --upgrade 2>/dev/null || true
    "$HERMES_VENV/bin/python" -m pip install -q lark-oapi 2>&1
    # 国内用户可加镜像：-i https://mirrors.aliyun.com/pypi/simple/
    echo "  ✓ 安装完成"
fi

echo ""
echo "=== 2/5 飞书显示优化 ==="
# 飞书端隐藏思考过程
hermes config set display.platforms.feishu.show_reasoning false 2>/dev/null || \
    echo "  ⚠  show_reasoning 设置失败（可手动改 config.yaml）"
# 飞书端隐藏工具调用
hermes config set display.platforms.feishu.tool_progress '"off"' 2>/dev/null || \
    echo "  ⚠  tool_progress 设置失败（可手动改 config.yaml）"
# 禁用 still working 通知
hermes config set agent.gateway_notify_interval 0 2>/dev/null || \
    echo "  ⚠  gateway_notify_interval 设置失败（可手动改 config.yaml）"
echo "  ✓ 显示配置完成"

echo ""
echo "=== 3/5 清理旧 gateway 进程和锁文件 ==="
for pid in $(pgrep -f 'hermes.*gateway' 2>/dev/null); do
    kill -9 "$pid" 2>/dev/null && echo "  killed PID $pid"
done
if ls "$LOCK_DIR"/feishu-app-id-*.lock 2>/dev/null; then
    rm -f "$LOCK_DIR"/feishu-app-id-*.lock
    echo "  ✓ 锁文件已清理"
else
    echo "  ✓ 无残留锁文件"
fi
sleep 1

echo ""
echo "=== 4/5 启动 Gateway ==="
set -a
source "$HERMES_HOME/.env" 2>/dev/null || true
set +a

hermes gateway run 2>&1 &
GATEWAY_PID=$!
echo "  Gateway PID: $GATEWAY_PID"

echo ""
echo "=== 5/5 验证连接 ==="
for i in $(seq 1 10); do
    sleep 1
    if grep -q '✓ feishu connected' "$LOG" 2>/dev/null; then
        echo "  ✓ 飞书已连接！"
        echo ""
        echo "=== 自动恢复完成 ==="
        echo "  [✓] lark-oapi 已安装"
        echo "  [✓] 飞书显示优化已配置（隐藏思考/工具/通知）"
        echo "  [✓] Gateway 进程运行中 (PID $GATEWAY_PID)"
        echo "  [✓] 飞书 WebSocket 已连接"
        echo ""
        echo "  手动确认项（需在飞书控制台操作）："
        echo "  [ ] 事件订阅含 card.action.trigger（卡片回执）"
        echo "  [ ] 事件订阅含 im.message.receive_v1（消息接收）"
        echo "  [ ] 版本已发布上线"
        echo "  控制台: https://open.feishu.cn/app/<你的app_id>"
        exit 0
    fi
    echo "  等待中... ($i/10)"
done

echo "  ✗ 连接超时，检查日志: tail -20 $LOG"
exit 1

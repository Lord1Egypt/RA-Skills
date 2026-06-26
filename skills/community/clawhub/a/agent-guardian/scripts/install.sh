#!/bin/bash
# ========================================
# 🛡️ Agent Guardian 安装脚本
# 自动配置看门狗、状态汇报、即时查询、语言过滤
# ========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🛡️ Agent Guardian 安装程序"
echo "=========================="
echo ""

# ===== 1. 交互式配置 =====
read -p "📡 渠道类型 (qqbot/telegram/wechat/feishu/discord): " CHANNEL
CHANNEL=${CHANNEL:-qqbot}

read -p "👤 用户ID/目标: " TARGET
if [ -z "$TARGET" ]; then
    echo "❌ 用户ID不能为空"
    exit 1
fi

read -p "⏰ 状态汇报间隔(分钟, 默认5): " REPORT_INTERVAL
REPORT_INTERVAL=${REPORT_INTERVAL:-5}

read -p "🐕 看门狗检查间隔(分钟, 默认3): " WATCHDOG_INTERVAL
WATCHDOG_INTERVAL=${WATCHDOG_INTERVAL:-3}

echo ""
echo "配置确认:"
echo "  渠道: $CHANNEL"
echo "  目标: $TARGET"
echo "  汇报间隔: ${REPORT_INTERVAL}分钟"
echo "  看门狗间隔: ${WATCHDOG_INTERVAL}分钟"
read -p "确认安装? (y/n): " CONFIRM
[ "$CONFIRM" != "y" ] && { echo "取消安装"; exit 0; }

# ===== 2. 写入配置文件 =====
cat > /tmp/agent-guardian-config.json << EOF
{
  "channel": "$CHANNEL",
  "target": "$TARGET",
  "report_interval": $REPORT_INTERVAL,
  "watchdog_interval": $WATCHDOG_INTERVAL,
  "installed_at": "$(date -Iseconds)",
  "skill_dir": "$SKILL_DIR"
}
EOF
echo "✅ 配置文件写入 /tmp/agent-guardian-config.json"

# ===== 3. 设置脚本执行权限 =====
chmod +x "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/*.py 2>/dev/null
echo "✅ 脚本执行权限设置完成"

# ===== 4. 安装依赖 =====
if ! python3 -c "import langdetect" 2>/dev/null; then
    echo "📦 安装 langdetect..."
    pip3 install langdetect -q 2>/dev/null || echo "⚠️ langdetect 安装失败（非必需，字符集检测仍可用）"
fi

if ! command -v inotifywait &>/dev/null; then
    echo "📦 安装 inotify-tools..."
    apt-get install -y inotify-tools -q 2>/dev/null || echo "⚠️ inotify-tools 安装失败（即时状态查询功能不可用）"
fi
echo "✅ 依赖检查完成"

# ===== 5. 配置系统 crontab =====
CRON_MARKER="# agent-guardian"
# 移除旧条目
crontab -l 2>/dev/null | grep -v "$CRON_MARKER" > /tmp/crontab-guardian.tmp || true
# 添加新条目
echo "*/$REPORT_INTERVAL * * * * $SCRIPT_DIR/smart-status-report.sh >> /tmp/status-report.log 2>&1 $CRON_MARKER" >> /tmp/crontab-guardian.tmp
crontab /tmp/crontab-guardian.tmp
rm -f /tmp/crontab-guardian.tmp
echo "✅ 系统 crontab 配置完成（每${REPORT_INTERVAL}分钟汇报）"

# ===== 6. 配置 systemd 守护进程（即时状态查询） =====
if command -v systemctl &>/dev/null && command -v inotifywait &>/dev/null; then
    cat > /etc/systemd/system/agent-guardian-query.service << EOF
[Unit]
Description=Agent Guardian Status Query Daemon
After=network.target

[Service]
Type=simple
ExecStart=$SCRIPT_DIR/status-query-daemon.sh
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl enable agent-guardian-query.service 2>/dev/null
    systemctl restart agent-guardian-query.service
    echo "✅ 即时状态查询守护进程已启动"
else
    echo "⚠️ systemd 或 inotifywait 不可用，跳过即时查询守护进程"
fi

# ===== 7. 初始化状态文件 =====
bash "$SCRIPT_DIR/reset-work-state.sh"
echo "✅ 工作状态初始化完成"

# ===== 8. 生成渠道 patch 指引 =====
PATCH_DIR="$SKILL_DIR/references/patches"
if [ -d "$PATCH_DIR" ] && [ -f "$PATCH_DIR/${CHANNEL}.md" ]; then
    echo ""
    echo "📋 渠道适配补丁指引: $PATCH_DIR/${CHANNEL}.md"
    echo "   请阅读该文件，手动将 [CUSTOM] 代码块添加到渠道插件源码中。"
    echo "   这一步需要修改插件源码并重启 gateway，无法全自动完成。"
fi

echo ""
echo "========================================="
echo "🎉 Agent Guardian 安装完成！"
echo ""
echo "已启用:"
echo "  🐕 看门狗 - 通过 openclaw cron 配置（需手动添加）"
echo "  📊 定时汇报 - 系统 crontab 每${REPORT_INTERVAL}分钟"
echo "  🔍 即时查询 - systemd 守护进程"
echo "  🔤 语言过滤 - 需渠道 patch 集成"
echo ""
echo "还需手动完成:"
echo "  1. 添加 openclaw cron 看门狗任务"
echo "  2. 应用渠道插件 patch（见 references/patches/）"
echo "  3. 重启 gateway"
echo "========================================="

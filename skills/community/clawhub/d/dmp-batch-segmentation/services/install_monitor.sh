#!/bin/bash
# DMP 任务监控服务安装脚本
# 首次使用时自动部署监控服务

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_DIR="$HOME/.dmp-monitor"

echo "=========================================="
echo "  DMP 任务监控服务安装程序"
echo "=========================================="
echo ""
echo "技能目录: $SKILL_DIR"
echo "安装目录: $INSTALL_DIR"
echo ""

# 检查是否已安装
if [ -d "$INSTALL_DIR" ] && [ -f "$INSTALL_DIR/task_monitor.py" ]; then
    echo "✅ 检测到已安装，检查服务状态..."
    
    # 检查服务是否在运行
    if pgrep -f "task_monitor.py" > /dev/null; then
        echo "✅ 监控服务正在运行"
    else
        echo "⚠️ 监控服务未运行，正在启动..."
    fi
else
    echo "📦 首次安装，正在部署..."
fi

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "📋 复制文件..."
cp "$SKILL_DIR/services/task_monitor.py" "$INSTALL_DIR/"
cp "$SKILL_DIR/services/monitor_config.json" "$INSTALL_DIR/"
cp "$SKILL_DIR/services/notify.py" "$INSTALL_DIR/"
cp "$SKILL_DIR/services/start_monitor.sh" "$INSTALL_DIR/"
cp "$SKILL_DIR/services/stop_monitor.sh" "$INSTALL_DIR/"
cp "$SKILL_DIR/services/check_monitor.sh" "$INSTALL_DIR/"

# 设置执行权限
chmod +x "$INSTALL_DIR"/*.sh

# 更新脚本中的路径
sed -i "s|/home/mlclaw/.dmp-monitor|$INSTALL_DIR|g" "$INSTALL_DIR"/*.sh

# 设置 crontab（每分钟检查服务状态）
echo "⏰ 配置定时任务..."
CRON_CMD="* * * * * $INSTALL_DIR/check_monitor.sh"
(crontab -l 2>/dev/null | grep -v "check_monitor.sh"; echo "$CRON_CMD") | crontab -

# 配置通知
echo ""
echo "=========================================="
echo "  配置任务完成通知"
echo "=========================================="
echo ""
echo "请选择通知方式（可多选，输入序号用逗号分隔）："
echo "  1. 企业微信机器人"
echo "  2. 钉钉机器人"
echo "  3. 飞书机器人"
echo "  4. 跳过（稍后配置）"
echo ""
read -p "请选择: " notify_choice

if [ "$notify_choice" != "4" ] && [ -n "$notify_choice" ]; then
    IFS=',' read -ra CHOICES <<< "$notify_choice"
    for choice in "${CHOICES[@]}"; do
        case $choice in
            1)
                read -p "请输入企业微信 Webhook URL: " wechat_url
                if [ -n "$wechat_url" ]; then
                    python3 "$INSTALL_DIR/notify.py" setup-wechat "$wechat_url"
                fi
                ;;
            2)
                read -p "请输入钉钉 Webhook URL: " dingtalk_url
                if [ -n "$dingtalk_url" ]; then
                    python3 "$INSTALL_DIR/notify.py" setup-dingtalk "$dingtalk_url"
                fi
                ;;
            3)
                read -p "请输入飞书 Webhook URL: " feishu_url
                if [ -n "$feishu_url" ]; then
                    python3 "$INSTALL_DIR/notify.py" setup-feishu "$feishu_url"
                fi
                ;;
        esac
    done
fi

# 启动服务
echo ""
echo "🚀 启动监控服务..."
cd "$INSTALL_DIR"
nohup python3 task_monitor.py > service.log 2>&1 &
echo $! > task_monitor.pid

sleep 2

# 检查是否启动成功
if pgrep -f "task_monitor.py" > /dev/null; then
    echo ""
    echo "=========================================="
    echo "  ✅ 安装成功！"
    echo "=========================================="
    echo ""
    echo "服务状态: 运行中 (PID: $(cat $INSTALL_DIR/task_monitor.pid))"
    echo "安装目录: $INSTALL_DIR"
    echo "日志文件: $INSTALL_DIR/service.log"
    echo ""
    echo "使用方法:"
    echo "  添加任务: python3 $INSTALL_DIR/task_monitor.py add <任务ID> <任务名称>"
    echo "  查看状态: python3 $INSTALL_DIR/task_monitor.py status"
    echo "  查看通知: python3 $INSTALL_DIR/task_monitor.py notifications"
    echo "  配置通知: python3 $INSTALL_DIR/notify.py config"
    echo ""
    exit 0
else
    echo ""
    echo "=========================================="
    echo "  ❌ 安装失败"
    echo "=========================================="
    echo ""
    echo "请检查日志: $INSTALL_DIR/service.log"
    echo ""
    exit 1
fi

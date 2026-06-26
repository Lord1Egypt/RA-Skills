#!/bin/bash
# A2A Gateway - 健康检查定时任务配置脚本
# 周期：每 12 小时执行一次

WORKSPACE="$HOME/.qclaw/workspace-a2a-gateway"
SCRIPT="$WORKSPACE/scripts/health.py"
LOG_DIR="$WORKSPACE/logs"
CRON_SCHEDULE="0 */12 * * *"

echo "=================================================="
echo "🏥 A2A Gateway - 健康检查定时任务配置"
echo "=================================================="
echo ""

# 1. 检查脚本是否存在
echo "1️⃣  检查 health.py 脚本..."
if [ ! -f "$SCRIPT" ]; then
    echo "   ❌ 错误: $SCRIPT 不存在"
    echo "   请先运行: python3 scripts/health.py check"
    exit 1
fi
echo "   ✅ 脚本存在: $SCRIPT"
echo ""

# 2. 创建日志目录
echo "2️⃣  创建日志目录..."
mkdir -p "$LOG_DIR"
echo "   ✅ 日志目录: $LOG_DIR"
echo ""

# 3. 显示将要配置的 cron 任务
echo "3️⃣  准备配置的定时任务:"
echo "   周期: 每 12 小时（每天 00:00 和 12:00）"
echo "   命令: cd $WORKSPACE && python3 scripts/health.py check >> $LOG_DIR/health-check.log 2>&1"
echo ""

# 4. 生成 cron 任务行
CRON_LINE="$CRON_SCHEDULE cd $WORKSPACE && python3 scripts/health.py check >> $LOG_DIR/health-check.log 2>&1"

echo "4️⃣   Cron 任务行:"
echo "   $CRON_LINE"
echo ""

# 5. 检查是否 already 存在
echo "5️⃣  检查是否已存在相同的定时任务..."
EXISTING=$(crontab -l 2>/dev/null | grep -F "scripts/health.py check")
if [ -n "$EXISTING" ]; then
    echo "   ⚠️  发现已存在的定时任务:"
    echo "   $EXISTING"
    echo ""
    read -p "   是否要替换它？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 删除旧的任务
        crontab -l 2>/dev/null | grep -v "scripts/health.py check" | crontab -
        echo "   ✅ 旧任务已删除"
    else
        echo "   ❌ 取消配置"
        exit 0
    fi
fi
echo ""

# 6. 添加到 crontab
echo "6️⃣  添加到 crontab..."
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "   ✅ 定时任务已添加"
echo ""

# 7. 显示当前 crontab
echo "7️⃣  当前的定时任务:"
crontab -l | grep -v "^#"
echo ""

# 8. 测试运行
echo "8️⃣  测试运行（手动执行一次）..."
cd "$WORKSPACE" && python3 scripts/health.py check
if [ $? -eq 0 ]; then
    echo "   ✅ 测试运行成功"
else
    echo "   ❌ 测试运行失败"
fi
echo ""

# 9. 显示日志文件位置
echo "9️⃣  日志配置:"
echo "   日志文件: $LOG_DIR/health-check.log"
echo "   查看日志: tail -f $LOG_DIR/health-check.log"
echo ""

echo "=================================================="
echo "✅ 配置完成！"
echo "=================================================="
echo ""
echo "📅 执行计划:"
echo "   - 每天 00:00（午夜）"
echo "   - 每天 12:00（中午）"
echo ""
echo "🔍 验证命令:"
echo "   crontab -l | grep health.py"
echo "   tail -20 $LOG_DIR/health-check.log"
echo ""

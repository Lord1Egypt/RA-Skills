#!/bin/bash
#
# Claw 运营管理中心 - 一键启用自动记录
#

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/claw-ops-manager"
SHELL_CONFIG="$HOME/.zshrc"

echo "🔧 Claw 运营管理中心 - 自动记录配置"
echo ""

# 检查技能目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：技能目录不存在"
    echo "请先运行: clawhub install claw-ops-manager"
    exit 1
fi

echo "✅ 找到技能目录: $SKILL_DIR"

# 检查 Web UI 服务器
if ! pgrep -f "server_full.py" > /dev/null; then
    echo "⚠️  Web UI 服务器未运行"
    echo "启动服务器..."
    cd "$SKILL_DIR"
    python3 scripts/server_full.py &
    sleep 2
    echo "✅ Web UI 已启动: http://localhost:8080"
else
    echo "✅ Web UI 已运行"
fi

echo ""
echo "选择配置方案："
echo "1) Shell 别名（推荐，简单）"
echo "2) Python 包装器（给 Python 脚本用）"
echo "3) 手动记录模式（需要手动调用）"
echo "4) 查看当前状态"
echo ""
read -p "请选择 [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "📝 配置 Shell 别名..."

        # 检查是否已经配置
        if grep -q "claw-exec" "$SHELL_CONFIG" 2>/dev/null; then
            echo "⚠️  别名已存在，跳过"
        else
            # 添加别名到配置文件
            cat >> "$SHELL_CONFIG" << 'EOF'

# Claw 运营管理中心 - 自动记录别名
alias claw-exec='$HOME/.openclaw/workspace/skills/claw-ops-manager/scripts/audit_wrapper.sh'
alias claw-audit='cd ~/.openclaw/workspace/skills/claw-ops-manager && python3 scripts/auto_audit.py'
alias claw-dashboard='open http://localhost:8080'
EOF
            echo "✅ 别名已添加到 $SHELL_CONFIG"
        fi

        echo ""
        echo "📚 使用方法："
        echo "  claw-exec 'ls -la'              # 执行并记录命令"
        echo "  claw-exec 'rm -rf ~/Desktop/截图'"
        echo "  claw-audit                      # 测试自动记录"
        echo "  claw-dashboard                  # 打开 Web UI"
        echo ""
        echo "⚠️  请运行以下命令使别名生效："
        echo "   source $SHELL_CONFIG"
        ;;

    2)
        echo ""
        echo "📝 Python 包装器路径："
        echo "  $SKILL_DIR/scripts/auto_audit.py"
        echo ""
        echo "📚 使用方法："
        cat << 'EOF'
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/claw-ops-manager")

from scripts.auto_audit import audited_exec

# 自动记录所有命令
audited_exec("ls -la")
audited_exec("rm -rf ~/Desktop/截图")
EOF
        ;;

    3)
        echo ""
        echo "📝 手动记录模式"
        echo ""
        echo "要记录操作，运行："
        cat << 'EOF'
cd ~/.openclaw/workspace/skills/claw-ops-manager

python3 << 'PYEOF'
from scripts.logger import OperationLogger

logger = OperationLogger()
logger.log_operation(
    tool_name="exec",
    action="run_command",
    parameters={"command": "你的命令"},
    success=True,
    duration_ms=100,
    user="牢大"
)
PYEOF
EOF
        ;;

    4)
        echo ""
        echo "📊 当前状态："
        echo ""
        echo "Web UI 服务器:"
        if pgrep -f "server_full.py" > /dev/null; then
            echo "  ✅ 运行中 (PID: $(pgrep -f 'server_full.py'))"
            echo "  🌐 访问: http://localhost:8080"
        else
            echo "  ❌ 未运行"
        fi
        echo ""
        echo "数据库:"
        if [ -f "$HOME/.openclaw/audit.db" ]; then
            echo "  ✅ 存在"
            count=$(sqlite3 "$HOME/.openclaw/audit.db" "SELECT COUNT(*) FROM operations;" 2>/dev/null || echo "0")
            echo "  📊 操作记录: $count 条"
        else
            echo "  ❌ 不存在"
        fi
        echo ""
        echo "Shell 别名:"
        if grep -q "claw-exec" "$SHELL_CONFIG" 2>/dev/null; then
            echo "  ✅ 已配置"
        else
            echo "  ❌ 未配置"
        fi
        ;;

    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ 配置完成！"
echo ""
echo "🌐 打开 Web UI: http://localhost:8080"
echo "📖 查看集成指南: $SKILL_DIR/INTEGRATION.md"

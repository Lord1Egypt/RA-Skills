#!/bin/bash
# ============================================================================
# Keynote MCP Server - 一键安装脚本
# ============================================================================
#
# 用法:
#   ./install.sh          # 完整安装（依赖 + 配置）
#   ./install.sh --deps   # 仅安装依赖
#   ./install.sh --config # 仅配置 Claude Desktop
#   ./install.sh --test   # 仅测试连接
#
# 平台要求: macOS 12.0+ (Monterey)
# Python 要求: 3.10+
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# 平台检测
# ============================================================================

check_platform() {
    log_info "检查运行环境..."

    if [[ "$(uname)" != "Darwin" ]]; then
        log_error "检测到非 macOS 平台: $(uname)"
        echo ""
        echo "此 MCP Server 仅能在 macOS 上运行（需要 Keynote.app）"
        echo "但你仍可以在当前环境查看代码结构和进行开发测试"
        exit 1
    fi

    echo "  平台: macOS $(sw_vers -productVersion)"
    echo "  架构: $(uname -m)"
}

# ============================================================================
# Python 检测
# ============================================================================

check_python() {
    log_info "检查 Python 环境..."

    if ! command -v python3 &> /dev/null; then
        log_error "未检测到 python3"
        echo "请安装 Python 3.10+: https://www.python.org/downloads/"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "  Python: $PYTHON_VERSION"

    # 检查版本
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ ($PYTHON_MAJOR -eq 3) && ($PYTHON_MINOR -lt 10) ]]; then
        log_error "Python 版本过低，需要 3.10+"
        exit 1
    fi
}

# ============================================================================
# Keynote 检测
# ============================================================================

check_keynote() {
    log_info "检查 Keynote..."

    if [ -d "/Applications/Keynote.app" ]; then
        echo "  ✓ Keynote.app 已安装"
    else
        log_warn "未检测到 Keynote.app"
        echo "  请从 App Store 安装 Keynote: https://apps.apple.com/app/keynote/id409183694"
    fi
}

# ============================================================================
# 安装依赖
# ============================================================================

install_dependencies() {
    log_info "安装 Python 依赖..."

    # 升级 pip
    echo "  升级 pip..."
    python3 -m pip install --upgrade pip > /dev/null 2>&1

    # 安装 MCP SDK
    echo "  安装 mcp (Model Context Protocol SDK)..."
    python3 -m pip install "mcp[cli]" 2>&1 | tail -3

    # 验证安装
    echo ""
    log_info "验证安装..."
    if python3 -c "import mcp; print('  ✓ mcp 版本:', mcp.__version__)" 2>/dev/null; then
        echo "  ✓ 依赖安装成功"
    else
        log_error "依赖安装失败，请手动运行:"
        echo "  pip install \"mcp[cli]\""
        exit 1
    fi
}

# ============================================================================
# 配置 Claude Desktop
# ============================================================================

configure_claude_desktop() {
    log_info "配置 Claude Desktop..."

    # 配置文件路径
    CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

    # 检查配置文件是否存在
    if [ -f "$CONFIG_FILE" ]; then
        log_info "检测到现有配置文件: $CONFIG_FILE"

        # 备份
        BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        echo "  ✓ 已备份到: $BACKUP_FILE"

        # 检查是否已有 keynote 配置
        if grep -q "keynote" "$CONFIG_FILE"; then
            log_warn "配置中已包含 'keynote'，跳过自动添加"
            echo "  请手动确认或修改配置文件:"
            echo "  $CONFIG_FILE"
            return
        fi
    else
        log_info "未找到配置文件，将创建新配置"
        mkdir -p "$(dirname "$CONFIG_FILE")"
        # 创建基本配置
        echo '{' > "$CONFIG_FILE"
        echo '  "mcpServers": {}' >> "$CONFIG_FILE"
        echo '}' >> "$CONFIG_FILE"
        echo "  ✓ 已创建配置文件"
    fi

    # 构造新的 server 配置
    SERVER_CONFIG=$(cat <<EOF
    "keynote": {
      "type": "stdio",
      "command": "$(which python3)",
      "args": [
        "$SCRIPT_DIR/server.py"
      ]
    }
EOF
)

    # 使用 Python 脚本以 JSON 安全的方式插入配置
    python3 << PYEOF
import json
import os

config_file = os.path.expanduser("$CONFIG_FILE")

# 读取现有配置
with open(config_file, "r") as f:
    config = json.load(f)

# 如果没有 mcpServers 字段，添加
if "mcpServers" not in config:
    config["mcpServers"] = {}

# 添加 keynote server
config["mcpServers"]["keynote"] = {
    "type": "stdio",
    "command": "$(which python3)",
    "args": ["$SCRIPT_DIR/server.py"]
}

# 写回文件
with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print("  ✓ 已添加 keynote MCP Server 配置")
PYEOF

    echo ""
    echo "配置文件内容:"
    echo "--------------------------------------------------"
    cat "$CONFIG_FILE"
    echo "--------------------------------------------------"
    echo ""
    log_info "配置完成!"
    echo ""
    echo "下一步:"
    echo "  1. 重启 Claude Desktop 应用"
    echo "  2. 在聊天中说 '用 Keynote 创建一个演示文稿'"
    echo "  3. 首次调用时会请求权限，点击允许"
    echo ""
    echo "要取消配置，运行:"
    echo "  rm '$CONFIG_FILE'"
    echo "  然后重启 Claude Desktop"
}

# ============================================================================
# 测试脚本
# ============================================================================

test_connection() {
    log_info "测试本地 Keynote 控制..."

    echo ""
    echo "测试 1: AppleScript 基本命令"
    if osascript -e 'tell application "System Events" to return "OK"' 2>/dev/null; then
        echo "  ✓ AppleScript 可用"
    else
        log_warn "AppleScript 执行失败"
        echo "  可能原因: 未授予终端自动化权限"
        echo "  解决: 系统设置 → 隐私与安全性 → 自动化 → 允许终端"
    fi

    echo ""
    echo "测试 2: Keynote 是否可被 AppleScript 控制"
    KEYNOTE_RESULT=$(osascript <<EOF 2>&1 || echo "FAILED")
tell application "Keynote"
    activate
    return "Keynote OK"
end tell
EOF
)

    if [[ "$KEYNOTE_RESULT" == *"OK"* ]]; then
        echo "  ✓ Keynote 控制正常"
    else
        log_warn "Keynote 控制失败"
        echo "  错误信息: $KEYNOTE_RESULT"
        echo ""
        echo "  解决步骤:"
        echo "  1. 确保 Keynote 已安装并可正常启动"
        echo "  2. 在首次调用时，系统会请求权限，请点击允许"
        echo "  3. 手动检查: 系统设置 → 隐私与安全性 → 自动化"
    fi

    echo ""
    echo "测试 3: Python 模块加载"
    if python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from keynote_tools import keynote_controller, applescript
print('  ✓ keynote_tools 模块加载成功')
info = keynote_controller.get_keynote_status()
print('  状态:', info)
" 2>&1; then
        echo "  ✓ Python 模块正常"
    else
        log_error "Python 模块有问题，请检查"
    fi
}

# ============================================================================
# 显示帮助信息
# ============================================================================

show_help() {
    cat <<EOF
Keynote MCP Server - 安装脚本
================================

用法:
  ./install.sh              完整安装
  ./install.sh --deps       仅安装 Python 依赖
  ./install.sh --config     仅配置 Claude Desktop
  ./install.sh --test       仅测试本地连接
  ./install.sh --help       显示此帮助

安装完成后，重启 Claude Desktop 即可使用。

项目结构:
  keynote-mcp-server/
  ├── server.py                    MCP Server 主程序
  ├── keynote_tools/
  │   ├── applescript.py           AppleScript 执行引擎
  │   └── keynote_controller.py    高层 API
  ├── examples/
  │   └── claude_desktop_config.json   配置示例
  └── install.sh                   本安装脚本
EOF
}

# ============================================================================
# 主逻辑
# ============================================================================

main() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║          Keynote MCP Server - 安装脚本 v1.0             ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""

    # 解析参数
    case "${1:-}" in
        "--help"|"-h")
            show_help
            exit 0
            ;;
        "--deps")
            check_platform
            check_python
            install_dependencies
            echo ""
            log_info "依赖安装完成!"
            echo "要配置 Claude Desktop，运行: ./install.sh --config"
            exit 0
            ;;
        "--config")
            check_platform
            configure_claude_desktop
            exit 0
            ;;
        "--test")
            check_platform
            check_python
            test_connection
            exit 0
            ;;
        "")
            # 完整安装
            ;;
        *)
            log_error "未知参数: $1"
            echo "运行 ./install.sh --help 查看帮助"
            exit 1
            ;;
    esac

    # 完整安装流程
    check_platform
    check_python
    check_keynote
    install_dependencies
    configure_claude_desktop

    echo ""
    log_info "=========================================="
    log_info "  安装完成!"
    log_info "=========================================="
    echo ""
    echo "测试工具:"
    echo "  ./install.sh --test"
    echo ""
    echo "使用示例（在 Claude 中说）:"
    echo "  \"用 Keynote 创建一个演示文稿，标题为产品发布\""
    echo "  \"打开 ~/Documents/demo.key 并列出所有幻灯片\""
    echo "  \"创建 5 张幻灯片，每张一个简短标题\""
    echo ""
}

main "$@"

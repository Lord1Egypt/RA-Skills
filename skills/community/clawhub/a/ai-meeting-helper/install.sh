#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 安装 ai-meeting-helper..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install openai python-dotenv --quiet

# 创建配置文件模板
if [ ! -f "$BASE_DIR/.env" ]; then
    echo "📝 创建 .env 配置文件..."
    cat > "$BASE_DIR/.env" << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here

# 可选：使用代理
# HTTP_PROXY=
# HTTPS_PROXY=
EOF
    echo "⚠️  请编辑 $BASE_DIR/.env 文件，填入你的 OPENAI_API_KEY"
fi

# 创建备份目录
mkdir -p "$BASE_DIR/.ai_meeting_backup"
mkdir -p "$BASE_DIR/.ai_meeting_logs"

# 设置可执行权限
chmod +x "$SCRIPT_DIR/source/meeting_helper.py"

echo "✅ 安装完成！"
echo ""
echo "📖 使用说明："
echo "1. 编辑 .env 文件，设置 OPENAI_API_KEY"
echo "2. 运行：ai-meeting-helper process <audio_file>"
echo "3. 或：ai-meeting-helper batch <folder>"
echo ""
echo "📚 详细文档：cat $BASE_DIR/SKILL.md"
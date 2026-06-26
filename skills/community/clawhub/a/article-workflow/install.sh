#!/bin/bash
# Article Workflow Skill 安装脚本
# 用法：./install.sh

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$(dirname "$SKILL_DIR")")"

echo "🚀 安装 Article Workflow Skill..."
echo "📁 安装目录：$SKILL_DIR"

# 创建必要的目录
echo "📂 创建目录结构..."
mkdir -p "$SKILL_DIR"/{data,logs}

# 创建 .gitignore
cat > "$SKILL_DIR/.gitignore" << 'EOF'
# 运行时数据
data/
logs/

# 配置文件（包含敏感信息）
config.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# macOS
.DS_Store

# 临时文件
*.tmp
*.bak
EOF
echo "✅ 创建 .gitignore"

# 复制配置文件
if [ ! -f "$SKILL_DIR/config.json" ]; then
    cp "$SKILL_DIR/config.example.json" "$SKILL_DIR/config.json"
    echo "✅ 创建配置文件 config.json"
else
    echo "⚠️  config.json 已存在，跳过"
fi

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true
chmod +x "$SKILL_DIR/scripts/"*.py 2>/dev/null || true

# 创建初始化数据文件
if [ ! -f "$SKILL_DIR/data/url_cache.json" ]; then
    cat > "$SKILL_DIR/data/url_cache.json" << 'EOF'
{
  "urls": {},
  "metadata": {
    "last_updated": null,
    "total": 0
  }
}
EOF
    echo "✅ 创建 URL 缓存文件"
fi

if [ ! -f "$SKILL_DIR/data/stats.json" ]; then
    cat > "$SKILL_DIR/data/stats.json" << 'EOF'
{
  "total_processed": 0,
  "today": 0,
  "this_week": 0,
  "this_month": 0,
  "by_quality": {
    "S": 0,
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
  }
}
EOF
    echo "✅ 创建统计文件"
fi

# 创建日志文件
touch "$SKILL_DIR/logs/workflow.log"
touch "$SKILL_DIR/logs/error.log"
echo "✅ 创建日志文件"

# 验证安装
echo ""
echo "🔍 验证安装..."
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✅ SKILL.md 存在"
else
    echo "❌ SKILL.md 缺失"
    exit 1
fi

if [ -f "$SKILL_DIR/scripts/check_url_dup.py" ]; then
    echo "✅ check_url_dup.py 存在"
else
    echo "⚠️  check_url_dup.py 不存在（可选）"
fi

if [ -f "$SKILL_DIR/scripts/monitor.sh" ]; then
    echo "✅ monitor.sh 存在"
else
    echo "⚠️  monitor.sh 不存在（可选）"
fi

# 完成
echo ""
echo "✅ Article Workflow Skill 安装完成！"
echo ""
echo "📖 下一步："
echo "   1. 编辑 config.json 配置你的参数"
echo "   2. 在群聊中测试：@Nox 分析这篇文章：https://..."
echo "   3. 查看文档：cat $SKILL_DIR/README.md"
echo ""
echo "🔧 常用命令："
echo "   ./scripts/monitor.sh status    # 查看状态"
echo "   ./scripts/monitor.sh report    # 生成周报"
echo "   ./scripts/monitor.sh cleanup   # 清理数据"

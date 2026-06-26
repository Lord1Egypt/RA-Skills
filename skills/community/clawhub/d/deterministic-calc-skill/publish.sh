#!/bin/bash
# deterministic-calc Skill 发布脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="deterministic-calc"

echo "========================================"
echo "  $SKILL_NAME 发布脚本"
echo "========================================"
echo ""

# 1. 检查必要文件
echo "📋 检查必要文件..."
for file in "SKILL.md" "__init__.py" "package.json" "README.md"; do
    if [ ! -f "$SKILL_DIR/$file" ]; then
        echo "❌ 缺少必要文件：$file"
        exit 1
    fi
done
echo "✅ 文件检查通过"
echo ""

# 2. 运行测试
echo "🧪 运行测试..."
cd "$SKILL_DIR"
python3 -m deterministic_calc calc "1 + 1" > /dev/null
echo "✅ 测试通过"
echo ""

# 3. 初始化 git（如果需要）
echo "🔧 检查 git 状态..."
if [ ! -d "$SKILL_DIR/.git" ]; then
    echo "初始化 git 仓库..."
    cd "$SKILL_DIR"
    git init
    git add .
    git commit -m "Initial commit: $SKILL_NAME skill"
fi
echo ""

# 4. 显示 git 远程
echo "📡 Git 远程仓库:"
cd "$SKILL_DIR"
git remote -v 2>/dev/null || echo "  (未设置)"
echo ""

# 5. 发布说明
echo "========================================"
echo "  发布步骤"
echo "========================================"
echo ""
echo "1️⃣  在 GitHub 创建仓库:"
echo "   https://github.com/new"
echo "   仓库名：$SKILL_NAME-skill"
echo "   设为 Public"
echo ""
echo "2️⃣  关联远程仓库:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/$SKILL_NAME-skill.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣  发布到 ClawHub:"
echo "   npx clawhub login    # 登录（首次）"
echo "   npx clawhub publish  # 发布"
echo ""
echo "4️⃣  验证发布:"
echo "   npx clawhub search $SKILL_NAME"
echo ""
echo "========================================"
echo "  用户安装命令"
echo "========================================"
echo ""
echo "   npx clawhub install $SKILL_NAME"
echo ""
echo "========================================"

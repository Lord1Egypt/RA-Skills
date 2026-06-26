#!/bin/bash

# 专业厨师对话食谱生成技能安装脚本
# 作者：中国深圳肖柏然 xiaoboren0@gmail.com

set -e

echo "========================================"
echo "  专业厨师对话食谱生成技能安装"
echo "========================================"
echo ""

# 检查当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="chef-dialog-recipe"

echo "📁 技能目录: $SCRIPT_DIR"
echo "🎯 技能名称: $SKILL_NAME"
echo ""

# 检查必要文件
REQUIRED_FILES=(
    "SKILL.md"
    "chef-dialog.sh"
    "install.sh"
)

echo "🔍 检查必要文件..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        exit 1
    fi
done
echo ""

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x "$SCRIPT_DIR/chef-dialog.sh"
chmod +x "$SCRIPT_DIR/chef-dialog-ai.sh"
chmod +x "$SCRIPT_DIR/chef-perspective.sh"
chmod +x "$SCRIPT_DIR/chef-perspective-ai.sh"
chmod +x "$SCRIPT_DIR/analyze-recipe.sh"
chmod +x "$SCRIPT_DIR/analyze-recipe-ai.sh"
chmod +x "$SCRIPT_DIR/finalize-recipe.sh"
chmod +x "$SCRIPT_DIR/install.sh"
echo "  ✅ 权限设置完成"
echo ""

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p "$SCRIPT_DIR/output"
echo "  ✅ 输出目录: $SCRIPT_DIR/output"
echo ""

# 检查OpenClaw技能目录
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/workspace/skills"
if [ -d "$OPENCLAW_SKILLS_DIR" ]; then
    echo "📂 OpenClaw技能目录: $OPENCLAW_SKILLS_DIR"
    
    # 检查是否已存在
    if [ -d "$OPENCLAW_SKILLS_DIR/$SKILL_NAME" ]; then
        echo "  ⚠️  技能已存在，跳过复制"
    else
        echo "  📋 复制技能到OpenClaw技能目录..."
        cp -r "$SCRIPT_DIR" "$OPENCLAW_SKILLS_DIR/"
        echo "  ✅ 复制完成"
    fi
else
    echo "  ⚠️  OpenClaw技能目录不存在，跳过复制"
fi
echo ""

# 测试运行
echo "🧪 测试技能运行..."
echo "  运行: ./chef-dialog.sh \"测试菜品\""
echo ""

# 创建测试脚本
TEST_SCRIPT="$SCRIPT_DIR/test_skill.sh"
cat > "$TEST_SCRIPT" << 'EOF'
#!/bin/bash
echo "🧪 测试专业厨师对话食谱生成技能"
echo "========================================"
echo ""
echo "测试1: 显示帮助信息"
./chef-dialog.sh
echo ""
echo "测试2: 生成东坡肉食谱"
./chef-dialog.sh "东坡肉"
echo ""
echo "✅ 测试完成！"
EOF

chmod +x "$TEST_SCRIPT"
echo "  ✅ 测试脚本创建: $TEST_SCRIPT"
echo ""

# 显示使用说明
echo "📖 使用说明"
echo "========================================"
echo ""
echo "1. 基本使用:"
echo "   ./chef-dialog.sh \"菜品名称\""
echo "   示例: ./chef-dialog.sh \"东坡肉\""
echo ""
echo "2. 输出文件:"
echo "   所有文件将保存在 ./output/ 目录下"
echo "   - 厨师视角食谱: .chef.md"
echo "   - AI分析报告: .analysis.md"
echo "   - 完整优化食谱: .md"
echo "   - 汇总报告: .summary.md"
echo ""
echo "3. 查看结果:"
echo "   cat output/菜品名称_recipe_时间戳.md"
echo ""
echo "4. 集成到OpenClaw:"
echo "   技能已复制到 OpenClaw 技能目录"
echo "   可在OpenClaw中直接调用"
echo ""

# 显示技能信息
echo "🎯 技能信息"
echo "========================================"
echo "名称: 专业厨师对话食谱生成"
echo "版本: 1.0"
echo "作者: 中国深圳肖柏然"
echo "邮箱: xiaoboren0@gmail.com"
echo "功能:"
echo "  • 专业厨师视角食谱生成"
echo "  • AI审查分析优化"
echo "  • 详细食材变化描述"
echo "  • 精确烹饪时间控制"
echo "  • 完整问题解决方案"
echo ""

echo "✅ 安装完成！"
echo ""
echo "🦞 像龙虾蜕壳生长，我们持续优化烹饪技艺 🦞"
echo ""
echo "开始使用: ./chef-dialog.sh \"您的菜品名称\""
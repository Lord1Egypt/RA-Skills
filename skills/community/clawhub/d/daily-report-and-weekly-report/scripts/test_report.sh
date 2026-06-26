#!/bin/bash
# 工作周报生成器测试脚本

echo "=== 工作周报生成器测试 ==="

# 测试1: 检查git是否可用
if command -v git &> /dev/null; then
    echo "✓ Git可用"
else
    echo "✗ Git不可用，但skill仍可使用其他数据源"
fi

# 测试2: 创建测试目录和文件
TEST_DIR="test_report_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR" || exit 1

# 初始化测试git仓库
git init
echo "# 测试项目" > README.md
git add README.md
git commit -m "初始提交: 添加README"

# 创建一些TODO注释
echo "// TODO: 实现用户登录功能" > app.js
echo "# TODO列表" > TODO.md
echo "1. 优化数据库查询" >> TODO.md
echo "2. 添加错误处理" >> TODO.md

echo "测试环境已设置在: $TEST_DIR"
echo ""
echo "=== 测试命令示例 ==="
echo "1. 生成最近1天的报告:"
echo "   git log --since=\"1 day ago\" --oneline"
echo ""
echo "2. 查找TODO注释:"
echo "   grep -r \"TODO\" ."
echo ""
echo "3. 完整的报告生成流程请参考SKILL.md"
echo ""
echo "=== 测试完成 ==="
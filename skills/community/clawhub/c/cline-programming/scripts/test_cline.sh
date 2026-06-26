#!/bin/bash
# Cline 编程技能测试脚本

echo "=== Cline 编程技能测试 ==="
echo "正在检查Cline是否已安装..."

# 检查Cline是否已安装
if ! command -v cline &> /dev/null; then
    echo "❌ Cline未安装，请先使用npm install -g @cline/cli命令安装"
    exit 1
fi

echo "✅ Cline已安装，版本: $(cline --version)"

echo "=== 测试Cline命令 ==="
echo ""

# 测试Cline帮助命令
echo "=== 测试Cline帮助 ==="
if cline help; then
    echo "✅ Cline帮助命令执行成功"
else
    echo "❌ Cline帮助命令执行失败"
    exit 1
fi
echo ""

# 测试Cline版本命令
echo "=== 测试Cline版本 ==="
if cline --version; then
    echo "✅ Cline版本命令执行成功"
else
    echo "❌ Cline版本命令执行失败"
    exit 1
fi
echo ""

# 测试Cline规划模式
echo "=== 测试Cline规划模式 ==="
if cline task "创建一个简单的Hello World程序" --plan --yolo --verbose --json; then
    echo "✅ Cline规划模式执行成功"
else
    echo "❌ Cline规划模式执行失败"
    exit 1
fi
echo ""

# 测试Cline执行模式
echo "=== 测试Cline执行模式 ==="
if cline task "创建一个简单的Hello World程序" --act --yolo --verbose --json; then
    echo "✅ Cline执行模式执行成功"
else
    echo "❌ Cline执行模式执行失败"
    exit 1
fi
echo ""

echo "=== 测试完成 ==="
echo "Cline编程技能测试成功！"
echo ""
echo "您可以使用以下命令开始使用Cline："
echo "1. 生成代码规划：cline task \"任务描述\" --plan --yolo --verbose --json"
echo "2. 执行代码：cline task \"任务描述\" --act --yolo --verbose --json"
echo ""
echo "例如："
echo "cline task \"创建一个简单的Web服务器\" --plan --yolo --verbose --json"
echo "cline task \"创建一个简单的Web服务器\" --act --yolo --verbose --json"
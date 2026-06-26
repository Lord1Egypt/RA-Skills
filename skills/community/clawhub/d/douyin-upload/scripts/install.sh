#!/bin/bash

# 抖音发布技能 - 安装脚本

echo "正在安装抖音发布技能..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "✗ 需要安装Python3"
    exit 1
fi

# 检查pip
if ! command -v pip &> /dev/null; then
    echo "✗ 需要安装pip"
    exit 1
fi

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p ~/.openclaw/workspace/logs
mkdir -p ~/.openclaw/workspace/articles
mkdir -p ~/.openclaw/workspace/images
mkdir -p ~/.openclaw/workspace/temp

# 安装Python依赖
echo "安装Python依赖..."
pip install -r scripts/requirements.txt

# 检查sau命令
echo "检查sau命令..."
if ! command -v sau &> /dev/null; then
    echo "⚠️  未找到sau命令"
    echo "请先安装抖音自动发布工具"
    echo "请参考: https://github.com/your-sau-repo"
    echo "安装后请将sau添加到PATH"
else
    echo "✓ 发现sau命令"
fi

# 创建环境变量配置文件
echo "创建环境变量配置..."
cat > ~/.openclaw/extensions/douyin/skills/douyin-upload/.env << 'EOF'
# 抖音发布技能环境变量配置
OPENAI_API_KEY=your_openai_api_key_here
EOF

echo ""
echo "✓ 抖音发布技能安装完成！"
echo ""
echo "配置说明:"
echo "  1. 复制上面的配置到 ~/.openclaw/extensions/douyin/skills/douyin-upload/.env"
echo "  2. 修改为你的实际配置"
echo "  3. 使用时运行: python3 scripts/main.py '你的主题'"
echo ""
echo "示例:"
echo "  python3 scripts/main.py '人工智能的发展'"
echo ""
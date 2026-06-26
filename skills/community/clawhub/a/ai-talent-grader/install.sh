#!/bin/bash
# AI人才定级专家 - 安装脚本

set -e  # 出错时退出

echo "=== AI人才定级专家 - 安装程序 ==="

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
if [[ $python_version < "3.8" ]]; then
    echo "错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi
echo "✓ Python版本: $python_version"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "警告: 不在虚拟环境中，建议使用虚拟环境"
    read -p "是否创建虚拟环境? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "创建虚拟环境..."
        python3 -m venv venv
        if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
            source venv/bin/activate
        else
            source venv/Scripts/activate
        fi
        echo "✓ 虚拟环境已激活"
    fi
else
    echo "✓ 已在虚拟环境中: $VIRTUAL_ENV"
fi

# 安装依赖
echo "安装依赖..."
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    echo "✓ 依赖安装完成"
else
    echo "错误: requirements.txt 文件不存在"
    exit 1
fi

# 检查可选依赖
echo "检查可选依赖..."
if ! python3 -c "import PyPDF2" 2>/dev/null; then
    echo "警告: PyPDF2 未安装，PDF解析功能将不可用"
    echo "  请使用 pip 安装 pypdf2"
fi

if ! python3 -c "import docx" 2>/dev/null; then
    echo "警告: python-docx 未安装，DOCX解析功能将不可用"
    echo "  请使用 pip 安装 python-docx"
fi

# 创建必要的目录
echo "创建目录结构..."
mkdir -p config
mkdir -p references
mkdir -p modules
mkdir -p examples
mkdir -p logs
echo "✓ 目录结构创建完成"

# 检查配置文件
if [[ ! -f "config/evaluation_config.yaml" ]]; then
    echo "警告: 配置文件不存在，将使用默认配置"
    echo "  请从 references/ 复制模板到 config/"
else
    echo "✓ 配置文件存在"
fi

# 测试安装
echo "测试安装..."
if python3 -c "import yaml; import loguru; print('✓ 核心依赖测试通过')" 2>/dev/null; then
    echo "✓ 安装测试通过"
else
    echo "错误: 核心依赖测试失败"
    exit 1
fi

# 运行示例
echo "运行示例测试..."
if [[ -f "run.py" ]]; then
    python3 run.py create
    echo "✓ 示例文件创建完成"
else
    echo "警告: run.py 不存在，跳过示例测试"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用说明:"
echo "1. 仅简历审计: python main.py audit --resume 简历.pdf"
echo "2. 完整定级: python main.py evaluate --resume 简历.pdf --interview 面试记录.txt"
echo "3. 批量处理: python main.py batch --input-dir candidates/ --output-dir reports/"
echo "4. 运行示例: python run.py evaluate"
echo ""
echo "配置文件位置: config/evaluation_config.yaml"
echo "参考文档: references/ 目录"
echo "日志文件: logs/ 目录"
echo ""
echo "如需帮助，请查看 README.md 或运行: python main.py --help"
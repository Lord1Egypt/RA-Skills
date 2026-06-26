#!/bin/bash

# Genos DNA 序列分析 - 安装脚本
# 用于快速安装和配置 Genos DNA 分析环境

set -e

echo "========================================"
echo "  Genos DNA 序列分析 - 安装脚本"
echo "========================================"
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python $PYTHON_VERSION 已安装"
else
    echo "✗ 未找到 Python 3，请安装 Python 3.9+"
    exit 1
fi

# 检查 pip
echo ""
echo "检查 pip..."
if ! command -v pip3 &> /dev/null; then
    echo "✗ 未找到 pip，请安装 pip"
    exit 1
fi

# 创建虚拟环境（可选）
echo ""
read -p "是否创建虚拟环境? (y/n) [y]: " CREATE_VENV
CREATE_VENV=${CREATE_VENV:-y}

if [ "$CREATE_VENV" = "y" ]; then
    echo "创建虚拟环境..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✓ 虚拟环境已创建"
    else
        echo "✓ 虚拟环境已存在"
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
fi

# 安装依赖
echo ""
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ 依赖已安装"

# 创建模型目录
echo ""
echo "创建模型目录..."
if [ ! -d "models" ]; then
    mkdir -p models
    echo "✓ 模型目录已创建"
else
    echo "✓ 模型目录已存在"
fi

# 创建状态目录
echo ""
echo "创建状态目录..."
if [ ! -d "state" ]; then
    mkdir -p state
    echo "✓ 状态目录已创建"
else
    echo "✓ 状态目录已存在"
fi

# 下载模型（可选）
echo ""
read -p "是否下载 Genos 模型? (y/n) [n]: " DOWNLOAD_MODEL
DOWNLOAD_MODEL=${DOWNLOAD_MODEL:-n}

if [ "$DOWNLOAD_MODEL" = "y" ]; then
    echo ""
    echo "选择下载源:"
    echo "1. Hugging Face (推荐)"
    echo "2. ModelScope (魔搭社区)"
    echo "3. GitHub Releases"
    read -p "请选择下载源 (1/2/3) [1]: " DOWNLOAD_SOURCE
    DOWNLOAD_SOURCE=${DOWNLOAD_SOURCE:-1}
    
    case $DOWNLOAD_SOURCE in
        1)
            echo ""
            read -p "Hugging Face Token (可选，用于下载私有模型): " HF_TOKEN
            
            if [ -n "$HF_TOKEN" ]; then
                huggingface-cli login --token "$HF_TOKEN"
            fi
            
            echo "从 Hugging Face 下载 Genos 模型..."
            echo "注意: 模型较大（约 2GB），下载可能需要一些时间"
            
            if command -v huggingface-cli &> /dev/null; then
                huggingface-cli download zhejianglab/Genos-1___2B --local-dir ./models/Genos-1___2B
                echo "✓ 模型已从 Hugging Face 下载"
            else
                echo "✗ 未找到 huggingface-cli，请先安装: pip install huggingface-hub"
                echo "或手动下载模型到 ./models/Genos-1___2B 目录"
            fi
            ;;
        2)
            echo "从 ModelScope 下载 Genos 模型..."
            echo "注意: 模型较大（约 2GB），下载可能需要一些时间"
            
            if command -v pip3 &> /dev/null; then
                pip3 install modelscope
                python3 -c "from modelscope import snapshot_download; snapshot_download('zhejianglab/Genos-1___2B', cache_dir='./models')"
                echo "✓ 模型已从 ModelScope 下载"
            else
                echo "✗ 未找到 pip，请先安装 pip"
                echo "或手动下载模型到 ./models/Genos-1___2B 目录"
            fi
            ;;
        3)
            echo "从 GitHub Releases 下载 Genos 模型..."
            echo "注意: 模型较大（约 2GB），下载可能需要一些时间"
            
            if command -v curl &> /dev/null && command -v unzip &> /dev/null; then
                curl -L -o genos-1.2b.zip "https://github.com/zhejianglab/Genos/releases/download/v1.0/Genos-1___2B.zip"
                unzip -o genos-1.2b.zip -d ./models/Genos-1___2B
                rm -f genos-1.2b.zip
                echo "✓ 模型已从 GitHub Releases 下载"
            else
                echo "✗ 未找到 curl 或 unzip，请先安装"
                echo "或手动下载模型到 ./models/Genos-1___2B 目录"
            fi
            ;;
        *)
            echo "✗ 无效的选择，请手动下载模型到 ./models/Genos-1___2B 目录"
            ;;
    esac
fi

# 创建配置文件
echo ""
echo "创建配置文件..."
if [ ! -f "config.json" ]; then
    cat > config.json << EOF
{
    "model_path": "./models/Genos-1___2B",
    "device_map": "cpu",
    "torch_dtype": "float16",
    "state_file": "./scripts/.model_loaded"
}
EOF
    echo "✓ 配置文件已创建 (config.json)"
else
    echo "✓ 配置文件已存在"
fi

# 测试安装
echo ""
echo "测试安装..."
python3 -c "
import sys
sys.path.insert(0, 'scripts')
try:
    from genos_dna import analyze_dna_sequence
    result = analyze_dna_sequence('ACGTACGT')
    print('✓ 安装测试通过')
    print(f'  序列长度: {result[\"cleaned_length\"]}')
    print(f'  GC 含量: {result[\"gc_content\"]:.2f}%')
except Exception as e:
    print('✗ 安装测试失败')
    print(f'  错误: {e}')
    sys.exit(1)
"

echo ""
echo "========================================"
echo "  安装完成！"
echo "========================================"
echo ""
echo "使用方法:"
echo "  1. 激活虚拟环境: source venv/bin/activate"
echo "  2. 运行示例: python3 example.py"
echo "  3. 命令行使用: python3 scripts/genos_dna.py analyze 'ACGTACGT'"
echo ""
echo "配置文件: config.json"
echo "模型目录: models/Genos-1___2B"
echo ""

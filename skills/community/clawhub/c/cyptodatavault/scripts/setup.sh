#!/bin/bash
# DataVault Skill 环境设置

set -e

echo "========================================"
echo "DataVault Skill Setup"
echo "========================================"

# 检查 Python 版本
echo "Checking Python version..."
python3 --version

# 创建虚拟环境 (可选)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "Activating virtual environment..."
source venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

# 创建配置
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cat > .env << 'EOF'
# DataVault Configuration
DATAVAULT_API_KEY=your_api_key_here

# Blockchain APIs
ETHERSCAN_API_KEY=your_etherscan_key
BSCSCAN_API_KEY=your_bscscan_key
POLYGONSCAN_API_KEY=your_polygonscan_key

# Optional: Redis for caching
REDIS_URL=redis://localhost:6379/0
EOF
    echo "Created .env file - please fill in your API keys"
fi

# 运行测试
echo "Running tests..."
bash scripts/test.sh

echo ""
echo "========================================"
echo "✅ Setup complete!"
echo "========================================"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the skill:"
echo "  python -m src"
echo ""
echo "To add more API keys, edit .env file"
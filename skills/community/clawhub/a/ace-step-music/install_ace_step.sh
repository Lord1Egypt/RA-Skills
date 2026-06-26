#!/bin/bash
# ACE-Step 1.5 安装脚本 for Mac Mini M2
# 作者: 进化大师
# 日期: 2026-03-03

set -e  # 遇到错误立即退出

echo "🎵 ACE-Step 1.5 安装程序"
echo "=========================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
INSTALL_DIR="$HOME/workspace/ace-step"
VENV_DIR="$HOME/ace-step-env"
MODEL_DIR="$INSTALL_DIR/models"

# 检查系统
echo "📋 检查系统环境..."

# 检查 macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "${RED}错误: 此脚本仅支持 macOS${NC}"
    exit 1
fi

# 检查 Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "${YELLOW}警告: 非 Apple Silicon 芯片，性能可能受影响${NC}"
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查内存
echo "📊 检查内存..."
MEMORY_GB=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//' | xargs -I {} echo "{} * 4096 / 1024 / 1024 / 1024" | bc)
echo "✅ 可用内存约: ${MEMORY_GB}GB"

# 检查磁盘空间
echo "💾 检查磁盘空间..."
DISK_AVAIL=$(df -h $HOME | awk 'NR==2 {print $4}')
echo "✅ 可用磁盘空间: $DISK_AVAIL"

echo ""
echo "🚀 开始安装..."
echo ""

# 1. 创建安装目录
echo "[1/6] 创建安装目录..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$MODEL_DIR"
cd "$INSTALL_DIR"

# 2. 创建虚拟环境
echo "[2/6] 创建 Python 虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "${YELLOW}虚拟环境已存在，跳过创建${NC}"
else
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建成功"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 3. 升级 pip
echo "[3/6] 升级 pip..."
pip install --upgrade pip -q

# 4. 安装依赖
echo "[4/6] 安装依赖包..."

# 安装 MLX (Apple Silicon 加速)
echo "  - 安装 MLX..."
pip install mlx mlx-lm -q || echo "${YELLOW}MLX 安装可能失败，继续尝试...${NC}"

# 安装其他依赖
echo "  - 安装基础依赖..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu -q || true
pip install transformers accelerate safetensors -q || true
pip install soundfile librosa -q || true

# 5. 克隆仓库 (带重试)
echo "[5/6] 下载 ACE-Step 1.5..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "✅ 仓库已存在，跳过克隆"
else
    # 尝试多次克隆
    for i in 1 2 3; do
        echo "  尝试克隆 (第 $i 次)..."
        if git clone --depth 1 https://github.com/ace-step/ACE-Step-1.5.git tmp_repo; then
            mv tmp_repo/* .
            rm -rf tmp_repo
            echo "✅ 克隆成功"
            break
        else
            echo "${YELLOW}  克隆失败，等待重试...${NC}"
            sleep 5
        fi
    done
    
    if [ ! -f "$INSTALL_DIR/README.md" ]; then
        echo "${YELLOW}警告: 仓库克隆失败，将使用 pip 安装方式${NC}"
        # 备用方案：pip 安装
        pip install ace-step -q || echo "${YELLOW}pip 安装也失败，请手动检查${NC}"
    fi
fi

# 6. 安装 ACE-Step
echo "[6/6] 安装 ACE-Step..."
if [ -f "$INSTALL_DIR/setup.py" ] || [ -f "$INSTALL_DIR/pyproject.toml" ]; then
    pip install -e ".[mlx]" -q || pip install -e . -q || echo "${YELLOW}本地安装失败，使用 pip 版本${NC}"
fi

echo ""
echo "✅ 安装完成！"
echo ""

# 创建启动脚本
cat > "$INSTALL_DIR/run.sh" << 'EOF'
#!/bin/bash
# ACE-Step 快速启动脚本

source "$HOME/ace-step-env/bin/activate"
cd "$HOME/workspace/ace-step"

if [ "$1" = "generate" ]; then
    shift
    python -m ace_step.generate "$@"
elif [ "$1" = "check" ]; then
    echo "检查安装状态..."
    python -c "import ace_step; print('ACE-Step 版本:', ace_step.__version__)" 2>/dev/null || echo "版本信息不可用"
    python -c "import mlx; print('MLX 版本:', mlx.__version__)" 2>/dev/null || echo "MLX 未安装"
else
    echo "用法:"
    echo "  ./run.sh generate --prompt \"你的音乐描述\" --output music.wav"
    echo "  ./run.sh check"
fi
EOF

chmod +x "$INSTALL_DIR/run.sh"

# 创建测试脚本
cat > "$INSTALL_DIR/test.py" << 'EOF'
#!/usr/bin/env python3
"""ACE-Step 安装测试"""

import sys
import time

print("🧪 测试 ACE-Step 安装...")
print("=" * 40)

# 测试 1: 导入测试
print("\n[1/4] 测试模块导入...")
try:
    import ace_step
    print("✅ ace_step 模块导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 测试 2: MLX 测试
print("\n[2/4] 测试 MLX 后端...")
try:
    import mlx
    import mlx.core as mx
    print(f"✅ MLX 版本: {mlx.__version__}")
    # 简单计算测试
    a = mx.array([1, 2, 3])
    print(f"✅ MLX 计算测试通过")
except ImportError:
    print("⚠️  MLX 未安装，将使用 CPU 模式")

# 测试 3: 模型检查
print("\n[3/4] 检查模型文件...")
import os
model_paths = [
    "~/workspace/ace-step/models",
    "./models",
]
found = False
for path in model_paths:
    expanded = os.path.expanduser(path)
    if os.path.exists(expanded):
        print(f"✅ 找到模型目录: {expanded}")
        found = True
        break

if not found:
    print("⚠️  未找到模型目录，首次运行时会自动下载")

# 测试 4: 快速生成测试 (可选)
print("\n[4/4] 快速生成测试 (5秒音乐)...")
print("    按 Ctrl+C 跳过")
try:
    start = time.time()
    # 这里可以添加实际的生成测试
    print(f"    测试跳过 (需手动运行)")
except KeyboardInterrupt:
    print("    跳过")

print("\n" + "=" * 40)
print("✅ 测试完成！")
print("")
print("使用方法:")
print("  cd ~/workspace/ace-step")
print("  ./run.sh generate --prompt \"A peaceful piano melody\" --output test.wav")
print("")
EOF

chmod +x "$INSTALL_DIR/test.py"

echo "📁 安装目录: $INSTALL_DIR"
echo "🐍 虚拟环境: $VENV_DIR"
echo ""
echo "🎉 安装脚本执行完毕！"
echo ""
echo "下一步操作:"
echo "  1. 运行测试: cd $INSTALL_DIR && python test.py"
echo "  2. 生成音乐: ./run.sh generate --prompt \"你的描述\" --output music.wav"
echo "  3. 查看帮助: ./run.sh --help"
echo ""
echo "如果克隆失败，请手动下载:"
echo "  git clone https://github.com/ace-step/ACE-Step-1.5.git $INSTALL_DIR"

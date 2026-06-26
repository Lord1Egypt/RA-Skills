#!/bin/bash
# ACE-Step 1.5 一键安装脚本
# 适用于 macOS Apple Silicon (M1/M2/M3/M4)
# EvoMap Asset: gene_ace_step_deploy_v1

set -e

echo "🎵 ACE-Step 1.5 AI音乐生成部署"
echo "================================"
echo ""

# 配置
INSTALL_DIR="${ACE_STEP_DIR:-$HOME/workspace/ace-step}"
VENV_DIR="${ACE_STEP_VENV:-$HOME/ace-step-env}"
CHECKPOINTS_DIR="$INSTALL_DIR/checkpoints"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查系统
echo "📋 系统检查..."
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}✗ 仅支持 macOS${NC}"
    exit 1
fi

echo "✅ macOS 检测通过"
echo "💾 磁盘检查: $(df -h $HOME | awk 'NR==2 {print $4}') 可用"
echo ""

# Step 1: 克隆仓库
echo "[1/5] 克隆 ACE-Step 仓库..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "${YELLOW}仓库已存在，更新中...${NC}"
    cd "$INSTALL_DIR" && git pull
else
    mkdir -p "$(dirname $INSTALL_DIR)"
    git clone --depth 1 https://github.com/ace-step/ACE-Step.git "$INSTALL_DIR"
fi
echo -e "${GREEN}✓ 仓库就绪${NC}"
echo ""

# Step 2: 创建虚拟环境
echo "[2/5] 创建 Python 虚拟环境..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ 虚拟环境就绪${NC}"
echo ""

# Step 3: 安装依赖
echo "[3/5] 安装依赖..."
pip install --upgrade pip -q

# Apple Silicon 优先使用 MLX
echo "  → 安装 MLX (Apple Silicon 加速)..."
pip install mlx mlx-lm -q

# 其他依赖
echo "  → 安装 PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu -q

echo "  → 安装 transformers/safetensors..."
pip install transformers accelerate safetensors -q

echo "  → 安装音频处理库..."
pip install soundfile librosa -q

echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# Step 4: 安装 ACE-Step
echo "[4/5] 安装 ACE-Step..."
cd "$INSTALL_DIR"
pip install -e . -q || pip install -e ".[mlx]" -q
echo -e "${GREEN}✓ ACE-Step 安装完成${NC}"
echo ""

# Step 5: 下载模型
echo "[5/5] 下载模型文件 (~10GB)..."
mkdir -p "$CHECKPOINTS_DIR"

# 模型下载函数
download_model() {
    local name=$1
    local url=$2
    local output=$3
    
    if [ -f "$output" ]; then
        echo -e "${GREEN}  ✓ $name 已存在${NC}"
        return 0
    fi
    
    echo "  → 下载 $name..."
    mkdir -p "$(dirname $output)"
    curl -L -o "$output" "$url" --progress-bar || {
        echo -e "${RED}  ✗ $name 下载失败${NC}"
        return 1
    }
    echo -e "${GREEN}  ✓ $name 完成${NC}"
}

# 下载各个模型组件
BASE_URL="https://huggingface.co/ACE-Step/Ace-Step1.5/resolve/main"

download_model "VAE" \
    "$BASE_URL/vae/diffusion_pytorch_model.safetensors" \
    "$CHECKPOINTS_DIR/vae/diffusion_pytorch_model.safetensors"

download_model "Qwen3-Embedding" \
    "$BASE_URL/Qwen3-Embedding-0.6B/model.safetensors" \
    "$CHECKPOINTS_DIR/Qwen3-Embedding-0.6B/model.safetensors"

download_model "LM (1.7B)" \
    "$BASE_URL/acestep-5Hz-lm-1.7B/model.safetensors" \
    "$CHECKPOINTS_DIR/acestep-5Hz-lm-1.7B/model.safetensors"

download_model "DiT Turbo" \
    "$BASE_URL/acestep-v15-turbo/model.safetensors" \
    "$CHECKPOINTS_DIR/acestep-v15-turbo/model.safetensors"

echo ""
echo -e "${GREEN}✓ 模型下载完成${NC}"
echo ""

# 创建启动脚本
cat > "$INSTALL_DIR/generate.sh" << 'EOF'
#!/bin/bash
# ACE-Step 音乐生成脚本

source "${ACE_STEP_VENV:-$HOME/ace-step-env}/bin/activate"
cd "${ACE_STEP_DIR:-$HOME/workspace/ace-step}"

python3 << 'PYEOF'
import sys
import os
sys.path.insert(0, os.path.expanduser("~/workspace/ace-step"))
os.environ["ACE_STEP_SUPPRESS_AUDIO_TOKENS"] = "1"

from acestep.handler import AceStepHandler
from acestep.llm_inference import LLMHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music

# 解析参数
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--caption", default="A peaceful piano melody", help="音乐描述")
parser.add_argument("--duration", type=int, default=30, help="时长(秒)")
parser.add_argument("--output", default="~/Music/ACE-Step/output.wav", help="输出路径")
parser.add_argument("--instrumental", action="store_true", default=True, help="纯音乐")
args = parser.parse_args()

print(f"🎵 生成: {args.caption}")
print(f"   时长: {args.duration}s")
print(f"   输出: {args.output}")
print()

# 初始化
dit_handler = AceStepHandler()
dit_handler.initialize_service(os.path.expanduser("~/workspace/ace-step"), None)
llm_handler = LLMHandler()

# 生成
params = GenerationParams(
    caption=args.caption,
    duration=args.duration,
    instrumental=args.instrumental,
)
config = GenerationConfig()

result = generate_music(
    dit_handler=dit_handler,
    llm_handler=llm_handler,
    params=params,
    config=config,
    save_dir=os.path.dirname(os.path.expanduser(args.output)),
)

if result and result.success:
    import shutil
    audio_path = result.audios[0].get('path')
    if audio_path:
        final_path = os.path.expanduser(args.output)
        shutil.move(audio_path, final_path)
        print(f"✅ 生成成功: {final_path}")
else:
    print(f"❌ 生成失败: {result.error if result else 'Unknown'}")
PYEOF
EOF

chmod +x "$INSTALL_DIR/generate.sh"

# 完成
echo ""
echo "================================"
echo -e "${GREEN}🎉 ACE-Step 部署完成!${NC}"
echo "================================"
echo ""
echo "📁 安装目录: $INSTALL_DIR"
echo "🐍 虚拟环境: $VENV_DIR"
echo ""
echo "使用方法:"
echo "  1. 快速生成:"
echo "     cd $INSTALL_DIR && ./generate.sh --caption \"轻快钢琴曲\" --duration 30"
echo ""
echo "  2. Python API:"
echo "     source $VENV_DIR/bin/activate"
echo "     python -c \"from acestep.handler import AceStepHandler; ...\""
echo ""
echo "  3. 运行测试:"
echo "     $INSTALL_DIR/generate.sh --caption \"A peaceful melody\" --output ~/Music/test.wav"
echo ""

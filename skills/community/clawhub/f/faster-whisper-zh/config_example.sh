#!/bin/bash
# faster-whisper 配置示例
# 复制此文件为 config.sh 并根据需要修改

# ========================================
# 环境变量配置
# ========================================

# HuggingFace 缓存目录（避免重复下载模型）
export HF_HOME=/config/huggingface

# 使用国内镜像加速下载（中国用户推荐）
export HF_ENDPOINT=https://hf-mirror.com

# PyTorch CUDA 设置（如有多个 GPU）
# export CUDA_VISIBLE_DEVICES=0  # 只使用第一个 GPU
# export CUDA_VISIBLE_DEVICES=0,1  # 使用前两个 GPU

# ========================================
# 默认转录参数
# ========================================

# 模型选择（根据硬件选择）
# 选项: tiny, base, small, medium, large-v3, large-v3-turbo, distil-large-v3
DEFAULT_MODEL="large-v3-turbo"

# 默认语言
# 选项: zh (中文), en (英文), ja (日文), ko (韩文), auto (自动检测)
DEFAULT_LANGUAGE="zh"

# 计算设备
# 选项: auto (自动检测), cpu, cuda
DEFAULT_DEVICE="cpu"

# 计算类型
# 选项: auto, int8 (CPU优化), float16 (GPU优化), float32 (高精度)
DEFAULT_COMPUTE_TYPE="auto"

# 束搜索大小（影响准确性和速度）
# 范围: 1-10，值越高越准确但越慢
DEFAULT_BEAM_SIZE=5

# ========================================
# 硬件特定配置
# ========================================

# 检测硬件并设置优化配置
detect_hardware() {
    echo "检测硬件配置..."
    
    # 检查 CUDA
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1)
        if [ -n "$GPU_INFO" ]; then
            echo "✓ 检测到 NVIDIA GPU: $GPU_INFO"
            DEFAULT_DEVICE="cuda"
            DEFAULT_COMPUTE_TYPE="float16"
            DEFAULT_MODEL="large-v3-turbo"
            return
        fi
    fi
    
    # 检查 Apple Silicon
    if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
        echo "✓ 检测到 Apple Silicon"
        DEFAULT_DEVICE="cpu"
        DEFAULT_COMPUTE_TYPE="int8"
        DEFAULT_MODEL="large-v3-turbo"
        return
    fi
    
    # 检查系统内存
    if [ "$(uname -s)" = "Linux" ]; then
        MEM_GB=$(free -g | awk '/^Mem:/ {print $2}')
        if [ "$MEM_GB" -ge 16 ]; then
            echo "✓ 检测到大内存系统: ${MEM_GB}GB"
            DEFAULT_MODEL="large-v3-turbo"
        else
            echo "⚠️  检测到有限内存: ${MEM_GB}GB"
            DEFAULT_MODEL="small"
        fi
    fi
    
    echo "ℹ️  使用 CPU 模式配置"
    DEFAULT_DEVICE="cpu"
    DEFAULT_COMPUTE_TYPE="int8"
}

# ========================================
# 使用场景配置
# ========================================

# 会议录音配置（中文，高准确度）
conference_config() {
    DEFAULT_MODEL="large-v3-turbo"
    DEFAULT_LANGUAGE="zh"
    DEFAULT_BEAM_SIZE=5
    echo "已应用会议录音配置"
}

# 实时转录配置（快速，低延迟）
realtime_config() {
    DEFAULT_MODEL="small"
    DEFAULT_BEAM_SIZE=3
    echo "已应用实时转录配置"
}

# 专业转录配置（最高准确度）
professional_config() {
    DEFAULT_MODEL="large-v3-turbo"
    DEFAULT_BEAM_SIZE=10
    echo "已应用专业转录配置"
}

# 多语言配置
multilingual_config() {
    DEFAULT_MODEL="large-v3-turbo"
    DEFAULT_LANGUAGE="auto"
    echo "已应用多语言配置"
}

# ========================================
# 实用函数
# ========================================

# 显示当前配置
show_config() {
    echo "当前配置:"
    echo "  模型: $DEFAULT_MODEL"
    echo "  语言: $DEFAULT_LANGUAGE"
    echo "  设备: $DEFAULT_DEVICE"
    echo "  计算类型: $DEFAULT_COMPUTE_TYPE"
    echo "  束搜索大小: $DEFAULT_BEAM_SIZE"
}

# 生成转录命令
generate_command() {
    local audio_file="$1"
    local output_file="$2"
    
    local cmd=".venv/bin/python3 scripts/transcribe.py \"$audio_file\""
    cmd="$cmd --model \"$DEFAULT_MODEL\""
    cmd="$cmd --language \"$DEFAULT_LANGUAGE\""
    cmd="$cmd --device \"$DEFAULT_DEVICE\""
    cmd="$cmd --compute-type \"$DEFAULT_COMPUTE_TYPE\""
    cmd="$cmd --beam-size \"$DEFAULT_BEAM_SIZE\""

    if [ -n "$output_file" ]; then
        cmd="$cmd --output \"$output_file\""
    fi

    echo "$cmd"
}

# ========================================
# 主程序
# ========================================

# 自动检测硬件（取消注释以启用）
# detect_hardware

# 显示欢迎信息
echo "========================================"
echo "faster-whisper 配置工具"
echo "========================================"
echo ""
echo "使用方法:"
echo "1. 复制此文件为 config.sh"
echo "2. 修改配置参数"
echo "3. 在转录前运行: source config.sh"
echo ""
echo "预设配置:"
echo "  source config.sh && conference_config"
echo "  source config.sh && realtime_config"
echo "  source config.sh && professional_config"
echo ""
show_config
echo "========================================"
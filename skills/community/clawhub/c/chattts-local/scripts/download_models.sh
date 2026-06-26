#!/bin/bash
# ChatTTS 模型下载脚本（使用 HuggingFace 镜像）

set -e

MODEL_DIR="$HOME/.openclaw/ChatTTS/models"
HF_MIRROR="https://hf-mirror.com"
REPO="2Noise/ChatTTS"

echo "📦 开始下载 ChatTTS 模型..."
echo "🌐 使用 HuggingFace 镜像源：$HF_MIRROR"

# 创建目录
mkdir -p "$MODEL_DIR/asset"
mkdir -p "$MODEL_DIR/tokenizer"
mkdir -p "$MODEL_DIR/ckpt"

# 下载 asset 目录文件
echo "📥 下载 asset 文件..."
wget -c "$HF_MIRROR/$REPO/resolve/main/asset/config.yaml" -O "$MODEL_DIR/asset/config.yaml"
wget -c "$HF_MIRROR/$REPO/resolve/main/asset/DVAE.pt" -O "$MODEL_DIR/asset/DVAE.pt"
wget -c "$HF_MIRROR/$REPO/resolve/main/asset/spk_stat.pt" -O "$MODEL_DIR/asset/spk_stat.pt"

# 下载 tokenizer 文件
echo "📥 下载 tokenizer 文件..."
wget -c "$HF_MIRROR/$REPO/resolve/main/tokenizer/tokenizer.json" -O "$MODEL_DIR/tokenizer/tokenizer.json"
wget -c "$HF_MIRROR/$REPO/resolve/main/tokenizer/special_tokens_map.json" -O "$MODEL_DIR/tokenizer/special_tokens_map.json"

# 下载 ckpt 文件
echo "📥 下载模型检查点（约 400MB，可能需要几分钟）..."
wget -c "$HF_MIRROR/$REPO/resolve/main/ckpt/model.pt" -O "$MODEL_DIR/ckpt/model.pt"

echo ""
echo "✅ 模型下载完成！"
echo "📂 模型位置：$MODEL_DIR"
echo ""
ls -lh "$MODEL_DIR"/*

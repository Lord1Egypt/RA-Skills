#!/bin/bash
#==============================================================================
# YOLO Model Downloader
# 自动下载 YOLO 模型到 HuggingFace modules 缓存目录
#==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MODELS_DIR="${HOME}/.cache/huggingface/modules/camera-yolo-operator"

echo "=========================================="
echo " YOLO Model Downloader"
echo "=========================================="
echo ""
echo "Skill 目录: ${SKILL_DIR}"
echo "模型目录:   ${MODELS_DIR}"
echo "说明: 模型禁止放入 skill 文件夹本身；统一放到 HuggingFace modules 缓存。"
echo ""

# Create directory
mkdir -p "${MODELS_DIR}"

# Ultralytics YOLO26s models
MODELS=(
    "yolo26s.pt"
    "yolo26s-seg.pt"
    "yolo26s-pose.pt"
    "yolo26s-obb.pt"
    "yolo26s-cls.pt"
)

echo "开始下载 YOLO 模型..."
echo ""

# Download each model using Python/ultralytics
for model in "${MODELS[@]}"; do
    target="${MODELS_DIR}/${model}"

    if [ -f "${target}" ]; then
        echo "  [SKIP] ${model} already exists"
        continue
    fi

    echo "  [DOWNLOAD] ${model}..."

    python3 -c "
from ultralytics import YOLO
import sys
try:
    model = YOLO('${model}')
    print('    [OK] Downloaded: ${model}')
except Exception as e:
    print(f'    [ERROR] Failed: {e}', file=sys.stderr)
    sys.exit(1)
" || {
        echo "  [ERROR] Failed to download ${model}"
        continue
    }

    # Move downloaded model to target directory.
    # Ultralytics may save to the current directory or ~/.cache/ultralytics/.
    if [ -f "${model}" ]; then
        mv "${model}" "${target}"
        echo "    [MOVED] to ${target}"
        continue
    fi
    cache_dir="$HOME/.cache/ultralytics/"
    if [ -f "${cache_dir}${model}" ]; then
        cp "${cache_dir}${model}" "${target}"
        echo "    [MOVED] to ${target}"
    elif [ -f "${cache_dir}/yolo${model:4}" ]; then
        # Handle yolo26s.pt -> yolo26s.pt naming
        cp "${cache_dir}/yolo${model:4}" "${target}" 2>/dev/null || true
    fi
done

echo ""
echo "=========================================="
echo " Model download complete!"
echo "=========================================="
echo ""
echo "Model location: ${MODELS_DIR}"
ls -lh "${MODELS_DIR}"/*.pt 2>/dev/null || echo "  (no .pt files)"
echo ""
echo "Depth model (DA3Metric-Large) will be downloaded automatically on first run"
echo "Tip: Run 'unset all_proxy ALL_PROXY' if HuggingFace download is slow"

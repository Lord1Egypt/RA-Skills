#!/bin/bash
# ACE-Step 模型下载监控脚本

echo "📥 ACE-Step 模型下载监控"
echo "=========================="
echo ""

CACHE_DIR="$HOME/.cache/huggingface"
MODEL_DIR="$HOME/workspace/ace-step/models"

echo "📍 缓存目录: $CACHE_DIR"
echo "📍 模型目录: $MODEL_DIR"
echo ""

# 检查目录大小
echo "📊 当前占用空间:"
if [ -d "$CACHE_DIR" ]; then
    echo "   HuggingFace缓存: $(du -sh $CACHE_DIR 2>/dev/null | cut -f1)"
else
    echo "   HuggingFace缓存: 未创建"
fi

if [ -d "$MODEL_DIR" ]; then
    echo "   本地模型目录: $(du -sh $MODEL_DIR 2>/dev/null | cut -f1)"
else
    echo "   本地模型目录: 未创建"
fi

echo ""
echo "🔍 监控下载进度 (每 10 秒刷新，按 Ctrl+C 停止)..."
echo ""

while true; do
    clear
    echo "📥 ACE-Step 模型下载监控 - $(date '+%H:%M:%S')"
    echo "=============================================="
    echo ""
    
    if [ -d "$CACHE_DIR" ]; then
        SIZE=$(du -sh $CACHE_DIR 2>/dev/null | cut -f1)
        FILES=$(find $CACHE_DIR -type f 2>/dev/null | wc -l)
        echo "📦 HuggingFace缓存: $SIZE ($FILES 个文件)"
        
        # 显示最近修改的文件
        echo ""
        echo "📝 最近下载的文件:"
        find $CACHE_DIR -type f -mtime -1 2>/dev/null | head -5 | while read f; do
            echo "   - $(basename $f) ($(du -h $f 2>/dev/null | cut -f1))"
        done
    else
        echo "⏳ 等待下载开始..."
    fi
    
    echo ""
    echo "💡 提示: 完整模型约 4GB，下载时间取决于网络速度"
    echo "   按 Ctrl+C 停止监控"
    
    sleep 10
done

#!/bin/bash
# 飞书图片发送 - 智能图片处理和发送

if [ $# -eq 0 ]; then
    echo "请提供图片路径"
    exit 1
fi

IMAGE_PATH="$1"
if [ ! -f "$IMAGE_PATH" ]; then
    echo "图片文件不存在: $IMAGE_PATH"
    exit 1
fi

# 获取文件大小 (字节)
FILE_SIZE=$(stat -f%z "$IMAGE_PATH")
# 设置大小阈值，飞书图片最大限制为 10MB = 10485760 字节
THRESHOLD=10485760

FILENAME=$(basename "$IMAGE_PATH")
WORKSPACE_PATH="/Users/bornforthis/.openclaw/workspace/$FILENAME"

# 复制原图到工作空间
cp "$IMAGE_PATH" "$WORKSPACE_PATH"

if [ $FILE_SIZE -gt $THRESHOLD ]; then
    echo "图片过大 (${FILE_SIZE} 字节)，正在进行压缩并同时发送原图..."
    
    # 压缩版本
    COMPRESSED_FILENAME="compressed_${FILENAME}"
    COMPRESSED_WORKSPACE_PATH="/Users/bornforthis/.openclaw/workspace/${COMPRESSED_FILENAME}"
    
    # macOS 下使用 sips 进行压缩 (限制最大边长或质量)
    sips -Z 1920 -s format jpeg -s formatOptions 80 "$IMAGE_PATH" --out "$COMPRESSED_WORKSPACE_PATH" > /dev/null
    
    # 发送压缩版
    echo "发送压缩版..."
    message(action="send", media="$COMPRESSED_WORKSPACE_PATH")
    
    # 发送原图版
    echo "发送原图版..."
    message(action="send", media="$WORKSPACE_PATH")
    
else
    echo "图片大小正常 (${FILE_SIZE} 字节)，直接发送原图..."
    # 直接发送
    message(action="send", media="$WORKSPACE_PATH")
fi

echo "完成: $FILENAME"

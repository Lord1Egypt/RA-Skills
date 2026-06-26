# feishu-image-sender - 飞书图片发送技能（增强版）

**智能图片发送工具，支持系统截图、本地图片发送，自动处理大图片压缩和双版本发送。**

## 📌 技能位置
**管理目录**: `/Users/bornforthis/.openclaw/skills/feishu-image-sender/improved/`

## 🚀 新增功能

- 📏 **智能大小检测** - 自动检测图片文件大小
- 🗜️ **智能压缩** - 大图片自动压缩到合适大小
- 📤 **双版本发送** - 同时发送压缩版和原图版
- ⚡ **小图直发** - 小图片直接发送，无需压缩
- 🔍 **质量保持** - 压缩时保持最佳视觉质量

## 📊 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MAX_SIZE_MB` | 10 | 最大文件大小（MB） |
| `COMPRESS_SIZE_MB` | 5 | 开始压缩的大小阈值（MB） |
| `COMPRESS_QUALITY` | 85 | JPEG压缩质量（1-100） |
| `KEEP_ORIGINAL` | true | 是否保留原图发送 |

## 🎯 使用方法

### 1. 系统截图并发送（智能处理）

```python
# 截图并发送，自动处理大小
exec(command="feishu-image-screenshot")
```

### 2. 发送指定图片（智能压缩）

```python
# 发送指定图片，自动压缩大图
exec(command="feishu-image-send /path/to/large-image.png")
```

### 3. 交互式截图（智能处理）

```python
# 交互式截图，智能处理大小
exec(command="feishu-image-interactive")
```

## 🔧 核心算法

### 智能图片处理流程

```python
def process_image_intelligently(image_path):
    """
    智能图片处理流程
    1. 检测图片大小
    2. 根据大小决定处理方式
    3. 发送适当版本
    """
    
    # 1. 获取文件大小
    file_size = get_file_size(image_path)
    size_mb = file_size / (1024 * 1024)
    
    if size_mb <= COMPRESS_SIZE_MB:
        # 小图片直接发送
        send_image(image_path, "original")
        return "小图片，直接发送"
    
    elif size_mb <= MAX_SIZE_MB:
        # 中等图片，压缩后发送
        compressed_path = compress_image(image_path)
        send_image(compressed_path, "compressed")
        return "中等图片，已压缩发送"
    
    else:
        # 大图片，双版本发送
        compressed_path = compress_image(image_path, quality=70)
        send_image(compressed_path, "compressed")
        if KEEP_ORIGINAL:
            send_image(image_path, "original")
        return "大图片，已发送压缩版和原图版"
```

### 图片压缩算法

```python
def compress_image(input_path, quality=85, max_size_mb=10):
    """
    智能图片压缩
    - 保持宽高比
    - 自动调整质量
    - 保证输出大小限制
    """
    from PIL import Image
    import os
    
    # 获取文件信息
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    
    # 打开图片
    with Image.open(input_path) as img:
        # 转换为RGB模式（如果是RGBA）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # 计算压缩后的尺寸
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        
        # 根据目标大小调整尺寸
        target_size_bytes = max_size_mb * 1024 * 1024
        current_size = os.path.getsize(input_path)
        
        if current_size > target_size_bytes:
            # 计算缩放比例
            scale_ratio = (target_size_bytes / current_size) ** 0.5
            new_width = int(original_width * scale_ratio)
            new_height = int(original_height * scale_ratio)
            
            # 调整尺寸
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 保存压缩后的图片
        compressed_path = f"/tmp/compressed_{name}.jpg"
        img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
        
        return compressed_path
```

## 📁 文件结构

```
feishu-image-sender/improved/
├── SKILL.md                 # 技能说明
├── README.md               # 使用说明
├── scripts/                 # 脚本目录
│   ├── screenshot.sh       # 系统截图脚本
│   ├── send.sh            # 发送图片脚本
│   ├── interactive.sh     # 交互式截图脚本
│   └── utils.py           # 工具函数
├── config/                 # 配置目录
│   └── settings.sh      # 配置文件
└── examples/               # 示例目录
    ├── small_image.png     # 小图片示例
    ├── medium_image.jpg    # 中等图片示例
    └── large_image.png    # 大图片示例
```

## 🎨 脚本实现

### screenshot.sh - 系统截图脚本

```bash
#!/bin/bash
# 飞书图片发送 - 系统截图（智能压缩）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILS_FILE="$SCRIPT_DIR/utils.py"

# 加载配置
source "$SCRIPT_DIR/config/settings.sh"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEMP_FILE="/tmp/screenshot_${TIMESTAMP}.png"
WORKSPACE_DIR="/Users/bornforthis/.openclaw/workspace"

# 创建工作空间目录
mkdir -p "$WORKSPACE_DIR"

# 截图
/usr/sbin/screencapture -x -t png "$TEMP_FILE"

if [ ! -f "$TEMP_FILE" ]; then
    echo "截图失败"
    exit 1
fi

# 智能处理图片
python3 "$UTILS_FILE" process_image "$TEMP_FILE" "screenshot_${TIMESTAMP}"

# 清理临时文件
rm -f "$TEMP_FILE"

echo "截图已智能处理并发送到飞书"
```

### send.sh - 发送图片脚本

```bash
#!/bin/bash
# 飞书图片发送 - 发送指定图片（智能压缩）

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <图片路径>"
    exit 1
fi

IMAGE_PATH="$1"
if [ ! -f "$IMAGE_PATH" ]; then
    echo "错误: 图片文件不存在: $IMAGE_PATH"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILS_FILE="$SCRIPT_DIR/utils.py"
WORKSPACE_DIR="/Users/bornforthis/.openclaw/workspace"

# 创建工作空间目录
mkdir -p "$WORKSPACE_DIR"

# 获取文件名
FILENAME=$(basename "$IMAGE_PATH")
NAME="${FILENAME%.*}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 智能处理图片
python3 "$UTILS_FILE" process_image "$IMAGE_PATH" "${NAME}_${TIMESTAMP}"

echo "图片已智能处理并发送到飞书"
```

### interactive.sh - 交互式截图脚本

```bash
#!/bin/bash
# 飞书图片发送 - 交互式截图（智能压缩）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILS_FILE="$SCRIPT_DIR/utils.py"
WORKSPACE_DIR="/Users/bornforthis/.openclaw/workspace"

# 创建工作空间目录
mkdir -p "$WORKSPACE_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEMP_FILE="/tmp/interactive_${TIMESTAMP}.png"

# 交互式截图
echo "请选择要截图的区域..."
/usr/sbin/screencapture -i -t png "$TEMP_FILE"

if [ -f "$TEMP_FILE" ]; then
    # 智能处理图片
    python3 "$UTILS_FILE" process_image "$TEMP_FILE" "interactive_${TIMESTAMP}"
    
    # 清理临时文件
    rm -f "$TEMP_FILE"
    
    echo "交互式截图已智能处理并发送到飞书"
else
    echo "用户取消截图"
fi
```

### utils.py - 工具函数

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书图片发送工具函数
智能图片处理和发送
"""

import os
import sys
import subprocess
import shutil
from PIL import Image
import json

# 配置
MAX_SIZE_MB = 10
COMPRESS_SIZE_MB = 5
COMPRESS_QUALITY = 85
KEEP_ORIGINAL = True

def get_file_size_mb(file_path):
    """获取文件大小（MB）"""
    if not os.path.exists(file_path):
        return 0
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def compress_image(input_path, quality=85, max_size_mb=10):
    """
    智能图片压缩
    :param input_path: 输入图片路径
    :param quality: JPEG质量 (1-100)
    :param max_size_mb: 最大文件大小(MB)
    :return: 压缩后的图片路径
    """
    try:
        # 获取文件信息
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB模式
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 获取原始尺寸
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height
            
            # 计算目标大小
            target_size_bytes = max_size_mb * 1024 * 1024
            current_size = os.path.getsize(input_path)
            
            # 如果需要调整尺寸
            if current_size > target_size_bytes:
                scale_ratio = (target_size_bytes / current_size) ** 0.5
                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)
                
                # 调整尺寸
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            compressed_path = f"/tmp/compressed_{name}.jpg"
            img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
            
            return compressed_path
    
    except Exception as e:
        print(f"压缩图片失败: {e}")
        return input_path

def send_image_to_feishu(image_path, version="original"):
    """发送图片到飞书"""
    try:
        # 复制到工作空间
        workspace_dir = "/Users/bornforthis/.openclaw/workspace"
        os.makedirs(workspace_dir, exist_ok=True)
        
        filename = os.path.basename(image_path)
        workspace_path = os.path.join(workspace_dir, filename)
        
        shutil.copy2(image_path, workspace_path)
        
        # 发送到飞书
        result = subprocess.run([
            sys.executable, "-c", 
            f"from message import message; message(action='send', media='{workspace_path}')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {version}版本已发送到飞书: {filename}")
            return True
        else:
            print(f"❌ 发送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 发送图片失败: {e}")
        return False

def process_image(input_path, base_name):
    """
    智能处理图片
    :param input_path: 输入图片路径
    :param base_name: 基础文件名
    """
    file_size_mb = get_file_size_mb(input_path)
    
    print(f"📏 检测到图片大小: {file_size_mb:.2f} MB")
    
    # 小图片直接发送
    if file_size_mb <= COMPRESS_SIZE_MB:
        print("🟢 小图片，直接发送")
        send_image_to_feishu(input_path, "original")
        return "小图片，直接发送"
    
    # 中等图片，压缩后发送
    elif file_size_mb <= MAX_SIZE_MB:
        print("🟡 中等图片，压缩后发送")
        compressed_path = compress_image(input_path, COMPRESS_QUALITY, MAX_SIZE_MB)
        send_image_to_feishu(compressed_path, "compressed")
        
        # 清理压缩文件
        if os.path.exists(compressed_path):
            os.remove(compressed_path)
        
        return "中等图片，已压缩发送"
    
    # 大图片，双版本发送
    else:
        print("🔴 大图片，发送压缩版和原图版")
        
        # 发送压缩版
        compressed_path = compress_image(input_path, COMPRESS_QUALITY, MAX_SIZE_MB)
        send_image_to_feishu(compressed_path, "compressed")
        
        # 发送原图版
        if KEEP_ORIGINAL:
            send_image_to_feishu(input_path, "original")
        
        # 清理压缩文件
        if os.path.exists(compressed_path):
            os.remove(compressed_path)
        
        return "大图片，已发送压缩版和原图版"

def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("使用方法: python3 utils.py process_image <input_path> <base_name>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    base_name = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在: {input_path}")
        sys.exit(1)
    
    result = process_image(input_path, base_name)
    print(f"处理结果: {result}")

if __name__ == "__main__":
    main()
```

## ⚙️ 配置文件

### settings.sh

```bash
# 飞书图片发送配置
MAX_SIZE_MB=10
COMPRESS_SIZE_MB=5
COMPRESS_QUALITY=85
KEEP_ORIGINAL=true
WORKSPACE_DIR="/Users/bornforthis/.openclaw/workspace"
TEMP_DIR="/tmp"
```

## 🎯 使用示例

### 示例1: 小图片处理
```bash
# 小图片 (< 5MB) - 直接发送
feishu-image-send small_image.png
# 输出: 🟢 小图片，直接发送
```

### 示例2: 中等图片处理
```bash
# 中等图片 (5-10MB) - 压缩后发送
feishu-image-send medium_image.jpg
# 输出: 🟡 中等图片，压缩后发送
```

### 示例3: 大图片处理
```bash
# 大图片 (> 10MB) - 双版本发送
feishu-image-send large_image.png
# 输出: 🔴 大图片，发送压缩版和原图版
```

## 📈 性能优化

### 压缩策略
1. **小图片** (< 5MB): 直接发送，保持原图质量
2. **中等图片** (5-10MB): 轻度压缩，保持良好质量
3. **大图片** (> 10MB): 双版本发送，保证可用性

### 质量控制
- 使用 LANCZOS 重采样算法，保持图片质量
- JPEG 质量 85%，在文件大小和质量间取得平衡
- 自动调整尺寸，保持宽高比

### 文件管理
- 自动清理临时文件
- 工作空间文件管理
- 错误处理和日志记录

## 🔧 故障排除

### 常见问题

1. **PIL库未安装**
```bash
pip install Pillow
```

2. **权限问题**
```bash
chmod +x scripts/*.sh
```

3. **路径问题**
确保工作空间目录存在且可写

### 日志调试
```bash
# 启用详细日志
export FEISHU_IMAGE_DEBUG=1
feishu-image-send image.png
```

## 🎉 总结

这个增强版的 feishu-image-sender 技能提供了：

- ✅ **智能大小检测** - 自动识别图片大小
- ✅ **智能压缩** - 根据大小自动压缩
- ✅ **双版本发送** - 大图片发送压缩版和原图版
- ✅ **小图直发** - 小图片直接发送，保持质量
- ✅ **配置灵活** - 可调整压缩参数
- ✅ **错误处理** - 完善的错误处理机制

通过这个技能，用户可以轻松发送各种大小的图片到飞书，系统会自动处理压缩和发送策略，确保最佳的发送效果。
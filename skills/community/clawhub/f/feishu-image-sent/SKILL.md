# feishu-image-sender - 飞书图片发送技能

**飞书图片发送工具，支持系统截图和本地图片发送到飞书。**

## 📌 技能位置
**统一管理目录**: `/opt/homebrew/lib/node_modules/openclaw/skills/feishu-image-sender/`

## 功能特性

- 🖥️ **系统截图** - 截取整个电脑屏幕
- 📐 **区域截图** - 支持指定截图区域
- 🖼️ **本地图片发送** - 发送本地图片文件到飞书
- 📱 **即时发送** - 截图后可直接发送到飞书
- 🎯 **自动化流程** - 标准化的图片发送流程

## 使用场景

- 需要分享当前屏幕内容
- 截取错误界面或问题截图
- 制作教程或演示截图
- 发送本地图片文件到飞书
- 远程协助时分享屏幕

## 核心功能

### 1. 系统截图并发送

```python
# 完整的截图并发送流程
def screenshot_and_send():
    # 1. 系统截图
    exec(command="/usr/sbin/screencapture -t png /tmp/screenshot.png")
    
    # 2. 移动到工作空间
    exec(command="cp /tmp/screenshot.png /Users/bornforthis/.openclaw/workspace/")
    
    # 3. 发送到飞书
    message(action="send", media="/Users/bornforthis/.openclaw/workspace/screenshot.png")
```

### 2. 发送本地图片

```python
# 发送本地图片文件
def send_local_image(image_path):
    # 检查文件是否存在
    if not os.path.exists(image_path):
        return "图片文件不存在"
    
    # 移动到工作空间（如果需要）
    workspace_path = "/Users/bornforthis/.openclaw/workspace/" + os.path.basename(image_path)
    exec(command=f"cp '{image_path}' '{workspace_path}'")
    
    # 发送到飞书
    message(action="send", media=workspace_path)
    return "图片发送成功"
```

### 3. 交互式截图

```python
# 交互式区域截图
def interactive_screenshot():
    exec(command="/usr/sbin/screencapture -i -c -t png /tmp/interactive_screenshot.png")
    exec(command="cp /tmp/interactive_screenshot.png /Users/bornforthis/.openclaw/workspace/")
    message(action="send", media="/Users/bornforthis/.openclaw/workspace/interactive_screenshot.png")
```

## 使用方法

### 方法1: 快速截图并发送

```python
# 使用feishu-image-screenshot命令快速截图并发送
exec(command="feishu-image-screenshot")
```

### 方法2: 发送指定图片

```python
# 发送指定路径的图片
exec(command="feishu-image-send /path/to/image.png")
```

### 方法3: 交互式截图

```python
# 交互式选择区域截图
exec(command="feishu-image-interactive")
```

## 参数说明

### 截图参数
- **格式**: PNG (推荐，无损压缩)
- **质量**: PNG 保持最佳质量，适合技术截图
- **延迟**: 可添加延迟避免截取到快照界面
- **区域**: 支持全屏、交互式选择区域

### 发送参数
- **文件路径**: 必须是工作空间目录下的文件
- **文件格式**: 支持 PNG、JPEG、GIF 等常见图片格式
- **文件大小**: 建议不超过 10MB

## 最佳实践

1. **使用 PNG 格式** - 保持最佳质量，适合技术截图
2. **添加适当延迟** - 避免截取到过渡状态
3. **文件命名规范** - 使用时间戳避免重复
4. **智能压缩** - 如果图片过大，会自动先压缩上传一次，再原图上传一次。小图片则不压缩直接发送。
5. **路径规范** - 文件必须保存到工作空间目录

## 常见问题

### Q: 截图为空白
**A**: 确保使用系统级截图命令，而不是浏览器截图

### Q: 截图模糊
**A**: 使用 PNG 格式，避免 JPEG 压缩

### Q: 截图不完整
**A**: 检查屏幕分辨率设置，使用全屏截图模式

### Q: 文件路径被拒绝
**A**: 飞书发送时需要将文件移动到允许的目录，如工作空间目录

### Q: screencapture 命令找不到
**A**: 在 macOS 上使用完整路径：
```bash
/usr/sbin/screencapture -t png /tmp/screenshot.png
```

## 示例脚本

### feishu-image-screenshot (截图并发送)
```bash
#!/bin/bash
# 飞书图片发送 - 系统截图并发送

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="/tmp/screenshot_${TIMESTAMP}.png"

# 截图
/usr/sbin/screencapture -x -t png "$FILENAME"

# 移动到工作空间
cp "$FILENAME" "/Users/bornforthis/.openclaw/workspace/screenshot_${TIMESTAMP}.png"

# 发送到飞书
message(action="send", media="/Users/bornforthis/.openclaw/workspace/screenshot_${TIMESTAMP}.png")

# 清理临时文件
rm "$FILENAME"

echo "截图已发送到飞书"
```

### feishu-image-send (发送指定图片)
```bash
#!/bin/bash
# 飞书图片发送 - 发送指定图片

if [ $# -eq 0 ]; then
    echo "请提供图片路径"
    exit 1
fi

IMAGE_PATH="$1"
if [ ! -f "$IMAGE_PATH" ]; then
    echo "图片文件不存在: $IMAGE_PATH"
    exit 1
fi

# 获取文件名
FILENAME=$(basename "$IMAGE_PATH")
WORKSPACE_PATH="/Users/bornforthis/.openclaw/workspace/$FILENAME"

# 复制到工作空间
cp "$IMAGE_PATH" "$WORKSPACE_PATH"

# 发送到飞书
message(action="send", media="$WORKSPACE_PATH")

echo "图片已发送到飞书: $FILENAME"
```

### feishu-image-interactive (交互式截图)
```bash
#!/bin/bash
# 飞书图片发送 - 交互式截图

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="/tmp/interactive_${TIMESTAMP}.png"

# 交互式截图
/usr/sbin/screencapture -i -t png "$FILENAME"

if [ -f "$FILENAME" ]; then
    # 移动到工作空间
    cp "$FILENAME" "/Users/bornforthis/.openclaw/workspace/interactive_${TIMESTAMP}.png"
    
    # 发送到飞书
    message(action="send", media="/Users/bornforthis/.openclaw/workspace/interactive_${TIMESTAMP}.png")
    
    # 清理临时文件
    rm "$FILENAME"
    
    echo "交互式截图已发送到飞书"
else
    echo "用户取消截图"
fi
```

## 集成到OpenClaw

### 在Python脚本中使用
```python
import subprocess

def send_image_to_feishu(image_path):
    """发送图片到飞书"""
    # 复制到工作空间
    workspace_path = "/Users/bornforthis/.openclaw/workspace/" + os.path.basename(image_path)
    subprocess.run(["cp", image_path, workspace_path])
    
    # 发送到飞书
    message(action="send", media=workspace_path)

def take_screenshot_and_send():
    """截图并发送到飞书"""
    import time
    timestamp = int(time.time())
    temp_path = f"/tmp/screenshot_{timestamp}.png"
    workspace_path = f"/Users/bornforthis/.openclaw/workspace/screenshot_{timestamp}.png"
    
    # 截图
    subprocess.run(["/usr/sbin/screencapture", "-x", "-t", "png", temp_path])
    
    # 移动并发送
    subprocess.run(["cp", temp_path, workspace_path])
    message(action="send", media=workspace_path)
    
    # 清理
    subprocess.run(["rm", temp_path])
```

## 支持的图片格式

- **PNG** - 无损压缩，推荐用于技术截图
- **JPEG** - 有损压缩，适合照片类图片
- **GIF** - 动图支持
- **WebP** - 现代图片格式
- **BMP** - 无压缩格式

## 性能优化

1. **文件大小控制** - 大图片建议压缩到10MB以内
2. **格式选择** - 技术截图用PNG，照片类用JPEG
3. **批量处理** - 支持批量发送多张图片
4. **缓存机制** - 避免重复发送相同图片

---

**注意**: 此技能优先使用系统级截图方法，确保截图的真实性和完整性，并遵循标准化的图片发送流程。
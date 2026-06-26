# Banana Pro Image Generation

使用 Gemini 图像模型生成图片的 OpenClaw Skill。

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key

```bash
export NEXTAI_API_KEY="your-api-key"
```

### 3. 生成图片

```bash
python scripts/generate_image.py \
  --prompt "A serene Japanese garden with cherry blossoms" \
  --filename "garden.png"
```

## 功能

- 🎨 文生图
- 📝 白板图（手写风格）
- 🏷️ Logo设计
- 📱 社交媒体配图
- ✏️ 图片编辑

## 分辨率

- `1K` - 默认，日常使用
- `2K` - 高清
- `4K` - 打印级别

## 示例

### 生成白板图

```bash
python scripts/generate_image.py \
  --prompt "生成一张白板图片，手写字体风格，内容是 OpenClaw 架构图..." \
  --filename "architecture.png"
```

### 设计 Logo

```bash
python scripts/generate_image.py \
  --prompt "设计一个AI助手Logo，圆形，蓝色渐变，简约现代" \
  --filename "logo.png" \
  --resolution 2K
```

### 编辑图片

```bash
python scripts/generate_image.py \
  --prompt "把天空改成夕阳效果" \
  --filename "edited.png" \
  --input-image "original.jpg"
```

## 许可证

MIT License

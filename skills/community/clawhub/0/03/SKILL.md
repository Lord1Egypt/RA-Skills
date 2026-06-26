---
name: "vision-ai"
version: "1.0.0"
description: "安全的图片识别工具，支持本地和API两种模式"
author: "AI Skills Team"
tags: ["图像识别", "视觉", "AI", "OpenAI", "Claude"]
requires: []
---

# AI视觉识别技能

安全的图片识别工具，支持本地模式和API模式（GPT-4o/Claude），保护隐私。

## 技能描述

提供图片内容识别、描述和分析功能。支持API模式（使用OpenAI或Claude）获得高准确度，或本地模式（无需API）保护隐私。

## 使用场景

- 用户："描述这张图片的内容" → 分析图片并返回描述
- 用户："这张图片里有什么物体？" → 识别图片中的物体
- 用户："分析这张截图" → 提取图片中的文字和界面信息
- 用户："批量分析这些图片" → 处理多张图片

## 工具和依赖

### 工具列表

- `scripts/vision_ai.py`：核心视觉识别模块

### API密钥

**可选（API模式）**：
- `OPENAI_API_KEY`：OpenAI API密钥（GPT-4o）
- `ANTHROPIC_API_KEY`：Anthropic API密钥（Claude）

### 外部依赖

**API模式（推荐）**：
- Python 3.7+
- openai 或 anthropic

**本地模式**：
- Python 3.7+
- torch（PyTorch）
- transformers
- Pillow

## 配置说明

### 环境变量

```bash
# API模式（推荐）
export OPENAI_API_KEY="sk-xxx"
# 或
export ANTHROPIC_API_KEY="sk-ant-xxx"
```

### 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)
- 最大文件大小：10MB

## 使用示例

### 基本用法

```python
from vision_ai import VisionAI

# API模式（推荐）
vision = VisionAI(mode="api")
result = vision.analyze("photo.jpg", "描述图片中的物体")

# 本地模式（无需API）
vision = VisionAI(mode="local")
result = vision.analyze("photo.jpg")

# 批量分析
results = vision.batch_analyze("./images")
```

### 场景1：描述图片内容

用户："这张图片里有什么？"

AI：
```python
vision = VisionAI(mode="api")
result = vision.analyze("photo.jpg", "描述图片内容")
# 返回：图片包含一只在草地上奔跑的金色犬...
```

### 场景2：识别图片中的文字

用户："提取这张截图中的文字"

AI：
```python
result = vision.analyze("screenshot.png", "提取图片中的所有文字")
# 返回：识别出的文字内容
```

### 场景3：批量分析

用户："分析images文件夹里的所有图片"

AI：
```python
results = vision.batch_analyze("./images")
# 返回：每张图片的分析结果
```

## 故障排除

### 问题1：API模式调用失败

**现象**：返回API错误

**解决**：
1. 检查API密钥是否正确
2. 确认API配额充足
3. 检查网络连接
4. 验证图片格式和大小

### 问题2：本地模式首次运行慢

**现象**：第一次分析图片很慢

**解决**：
- 首次运行需要下载模型（约500MB）
- 确保网络畅通
- 下载完成后会缓存，后续速度正常

### 问题3：图片格式不支持

**现象**：提示文件格式错误

**解决**：
- 确认文件是JPG/PNG/WebP/GIF格式
- 检查文件大小不超过10MB
- 尝试转换图片格式

## 性能对比

| 模式 | 准确度 | 速度 | 成本 | 隐私 |
|------|--------|------|------|------|
| API模式 | ⭐⭐⭐⭐⭐ | 快 | 按量计费 | 需上传 |
| 本地模式 | ⭐⭐⭐ | 慢 | 免费 | 完全本地 |

## 注意事项

1. **敏感图片**：建议使用本地模式，保护隐私
2. **API配额**：API模式按使用量计费，注意控制成本
3. **批量处理**：注意API速率限制
4. **模型下载**：本地模式首次运行需要下载模型

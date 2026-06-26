---
name: bananapro-image-gen
description: 使用 Gemini 图像模型生成图片，支持白板图、Logo设计、社交媒体配图。
author: jarvis
license: MIT
tags:
  - image
  - gemini
  - ai
  - design
  - logo
---

# Banana Pro Image Generation Skill

使用 Gemini 图像模型生成各种风格的图片。

## 功能特点

- 文生图：根据文字描述生成图片
- 白板图：生成手写风格的概念图、流程图
- Logo设计：创建简约现代的Logo
- 社交媒体配图：生成适合各平台的配图
- 图片编辑：修改已有图片

## 中转 API 配置教程

### 什么是中转 API？

中转 API 是第三方提供的 API 代理服务，相比官方 API 有以下优势：

- 成本更低（通常 5-7 折）
- 国内网络直连，更稳定
- 无需配置代理

### 推荐中转服务

**apipro.maynor1024.live**（默认）

网站：https://apipro.maynor1024.live/

### 配置方式

**方式一：使用中转 API（推荐）**

```
export NEXTAI_API_KEY="your-api-key"
```

获取 API Key：
1. 访问 https://apipro.maynor1024.live/
2. 注册账号
3. 获取 API Key

**方式二：使用官方 Gemini API**

```
export GEMINI_API_KEY="your-gemini-api-key"
```

获取方式：访问 https://aistudio.google.com/apikey

注意：官方 API 需要科学上网。

**方式三：使用其他中转服务**

支持任何 OpenAI 兼容的中转服务：

```
export NEXTAI_API_KEY="your-api-key"
export NEXTAI_API_URL="https://your-proxy.com/v1"
```

## 使用方法

### 基础用法

```
python scripts/generate_image.py \
  --prompt "A serene Japanese garden" \
  --filename "garden.png"
```

### 高清图片

```
python scripts/generate_image.py \
  --prompt "你的提示词" \
  --filename "output.png" \
  --resolution 2K
```

### 图片编辑

```
python scripts/generate_image.py \
  --prompt "把天空改成夕阳效果" \
  --filename "edited.png" \
  --input-image "original.jpg"
```

## 分辨率选项

- **1K**（默认）：~1024px，日常使用
- **2K**：~2048px，高清展示
- **4K**：~4096px，打印输出

## 提示词技巧

### 白板图模板

```
生成一张白板图片，手写字体风格，内容包含：
- 标题：[主题]
- 核心要点：
  1. [要点1]
  2. [要点2]
- 使用箭头、框图等手绘元素
```

### Logo设计模板

```
设计一个[主题]Logo，要求：
- 形状：[圆形/方形/抽象]
- 颜色：[主色调]
- 元素：[核心元素]
- 风格：[现代/简约]
```

## 常见问题

### Q: 中转 API 安全吗？

A: 选择可信的中转服务很重要。apipro.maynor1024.live 是社区常用的中转服务。

### Q: 支持中文提示词吗？

A: 完全支持！Gemini 对中文理解很好。

## 许可证

MIT License

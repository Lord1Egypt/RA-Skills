---
name: dmxapi-image-recognition
description: 使用 DMXAPI 平台进行图像识别和理解。支持 Gemini 等多模态视觉模型。可进行图片描述、OCR文字识别、图表数据分析、物体检测、场景理解等任务。当用户需要识别图片内容、提取图片文字、分析图表、理解图像时使用此技能。
compatibility: Requires Node.js 20+ and dmxapi-cli installed
metadata:
  author: onee-io
  version: "1.0.0"
---

# DMXAPI 图像识别/理解

通过 DMXAPI 统一 CLI 调用多种 AI 视觉模型进行图像识别和理解。

## 前置准备

1. 安装 CLI 工具（需要 Node.js 20+）：
   ```bash
   npm install -g dmxapi-cli
   ```

2. 配置 API Key（从 [DMXAPI 控制台](https://www.dmxapi.cn/) 获取）：
   ```bash
   dmxapi config set apiKey sk-your-api-key
   ```

## 命令格式

```bash
dmxapi chat -m <model> "提示词" --image <path>
```

## 选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `-m, --model <model>` | 视觉模型名称（默认 `gpt-5-mini`） | `-m gemini-3-flash-preview` |
| `--image <path>` | 图片路径（本地文件或 URL） | `--image ./photo.png` |
| `-s, --system <message>` | 系统消息（定义识别任务） | `-s "你是一个OCR专家"` |
| `-t, --temperature <number>` | 采样温度 0-2 | `-t 0.3` |
| `--max-tokens <number>` | 最大输出 token 数 | `--max-tokens 2000` |

## 支持的图片格式

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- WebP (`.webp`)
- GIF (`.gif`)

## 图片输入方式

1. **本地文件路径**：自动转换为 base64 data URL
   ```bash
   dmxapi chat "描述这张图片" --image ./photo.jpg
   ```

2. **远程 URL**：直接使用网络图片
   ```bash
   dmxapi chat "分析这张图片" --image https://example.com/image.png
   ```

## 推荐模型

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `gpt-5-mini` | 默认模型，速度快，成本低 | 通用图像识别 |
| `gemini-3-flash-preview` | Google 最新视觉模型 | 复杂图像分析、场景理解 |

## 使用步骤

1. 确定用户的图像识别需求类型（描述、OCR、分析等）
2. 选择合适的视觉模型
3. 根据任务类型编写精确的提示词
4. 构建 `dmxapi chat` 命令并执行
5. 将识别结果返回给用户

## 示例

### 图片描述

```bash
# 基本描述
dmxapi chat "请详细描述这张图片的内容" --image ./landscape.jpg

# 简洁描述
dmxapi chat "用一句话描述这张图片" --image ./photo.png
```

### OCR 文字识别

```bash
# 通用 OCR
dmxapi chat "识别图片中的所有文字，按原始排版输出" --image ./document.png

# 手写文字识别
dmxapi chat "识别图片中的手写文字" --image ./handwriting.jpg

# 表格识别
dmxapi chat "识别图片中的表格，以 Markdown 表格格式输出" --image ./table.png
```

### 图表数据分析

```bash
# 图表解读
dmxapi chat "分析这张图表，提取关键数据点并总结趋势" --image ./chart.png

# 数据提取
dmxapi chat "提取图中柱状图的所有数值，以 JSON 格式输出" --image ./bar-chart.jpg
```

### 物体检测与识别

```bash
# 物体检测
dmxapi chat "识别图片中的所有物体，列出它们的名称和位置" --image ./room.jpg

# 动植物识别
dmxapi chat "识别图片中的植物种类" --image ./flower.png
```

### 场景理解

```bash
# 场景分析
dmxapi chat "分析这张图片的场景，描述环境、氛围和可能的用途" --image ./scene.jpg

# 安全检查
dmxapi chat "检查这张图片是否存在安全隐患" --image ./workplace.png
```

### 文档理解

```bash
# 文档摘要
dmxapi chat "总结这张文档图片的主要内容" --image ./contract.png

# 信息提取
dmxapi chat "从身份证图片中提取姓名和身份证号" --image ./id-card.jpg
```

### 代码/截图识别

```bash
# 代码识别
dmxapi chat "识别图片中的代码并输出为可复制的文本格式" --image ./code-screenshot.png

# UI 分析
dmxapi chat "分析这个 UI 界面的设计元素和布局" --image ./ui-screenshot.jpg
```

## 使用 System 消息增强效果

通过 `-s` 参数设置 system 消息，可以让模型专注于特定任务：

```bash
# OCR 专家模式
dmxapi chat -s "你是一个专业的OCR识别助手，只输出识别到的文字内容，不要添加任何解释" "识别文字" --image ./doc.png

# 数据分析专家模式
dmxapi chat -s "你是一个数据分析专家，擅长从图表中提取数据" "分析图表" --image ./chart.png

# 多语言识别
dmxapi chat -s "识别图片中的文字，如果是英文请翻译成中文" "识别并翻译" --image ./english-doc.png
```

## 注意事项

- 本地图片文件会自动转换为 base64 data URL 上传
- 远程 URL 图片直接传递给 API 处理
- 对于复杂识别任务，建议使用 `gemini-3-flash-preview`
- 如果识别结果不满意，可以调整提示词或降低 temperature 参数获得更确定的输出
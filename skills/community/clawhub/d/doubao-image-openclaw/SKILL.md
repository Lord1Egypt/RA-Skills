---
name: doubao-image
description: 使用火山引擎豆包模型生成图片。通过火山引擎豆包图片生成 API 创建图片。支持自定义提示词、尺寸、模型等参数。使用方式：生图：一只可爱的小猫。
---

# doubao-image - 豆包图片生成

使用火山引擎豆包模型生成图片。

## 简介

通过火山引擎豆包图片生成 API 创建图片。支持多模型自动切换、URL 输出等功能。

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `VOLCENGINE_IMAGE_API_KEY` | Yes | 豆包 API Key |
| `DOUBAO_IMAGE_OUTPUT_DIR` | No | 图片输出目录（默认：workspace/downloads/images） |

**Get API Key**:
1. Login https://console.volces.com/
2. Go to API Key management
3. Copy your API Key

## 使用方式

```
生图：一只可爱的小猫
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 图片描述 | (必填) |
| --model | 使用的模型 | doubao-seedream-4-0-250828 |
| --size | 图片尺寸 | 1024x1024 |
| --num | 生成数量 | 1 |
| --url-only | 仅返回 URL，不下载 | false |

### 支持的模型（自动切换）

按优先级排序，优先使用第一个，失败则自动尝试下一个：

1. `doubao-seedream-4-0-250828` (默认)
2. `doubao-seedream-4-5-251128`
3. `doubao-seedream-5-0-260128`
4. `doubao-seedream-3-0-t2i-250415`

### 支持的尺寸

- 1024x1024 (默认)
- 1280x720
- 720x1280
- 1024x768
- 768x1024

## 输出格式

### 控制台输出

```
==================================================
Prompt: a cute kitten
Size: 1024x1024
Num: 1
==================================================
Trying model: doubao-seedream-4-0-250828
[OK] Model doubao-seedream-4-0-250828 success

==================================================
Success!
Model: doubao-seedream-4-0-250828
URL: https://...
==================================================

Downloading to: C:\Users\zcf\.openclaw\workspace\downloads\images\doubao_1234567890.jpeg
[OK] Saved: C:\Users\zcf\.openclaw\workspace\downloads\images\doubao_1234567890.jpeg
  Size: 256.5 KB

[FILE_PATH] C:\Users\zcf\.openclaw\workspace\downloads\images\doubao_1234567890.jpeg
```

### 特殊标记

- `[URL_ONLY] <url>` - 仅生成 URL 时的输出
- `[FILE_PATH] <path>` - 文件保存路径

## 输出目录

图片自动保存到 `downloads/images/` 目录。

可通过环境变量自定义：
```bash
# Windows
set DOUBAO_IMAGE_OUTPUT_DIR=D:\my_images

# Linux/Mac
export DOUBAO_IMAGE_OUTPUT_DIR=/path/to/images
```

## 重要说明

- **API Key**: 从 `VOLCENGINE_IMAGE_API_KEY` 环境变量读取
- **Multi-model fallback**: 如果默认模型失败，会自动尝试备选模型
- **URL Output**: 生成后立即输出图片 URL

## 错误处理

- 如果所有模型都失败，会显示具体错误信息
- 如果下载失败，仍会输出 URL 供手动下载

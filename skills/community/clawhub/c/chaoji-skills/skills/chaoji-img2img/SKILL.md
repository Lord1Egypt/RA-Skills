---
name: chaoji-img2img
description: AI 图生图助手（素材生成）。根据参考图和文字描述生成新图片。Triggered when user says "图生图", "参考这张图生成", "素材生成", "潮绘", "image to image", etc.
version: "1.0.0"
metadata: {"openclaw":{"requires":{"bins":["python"],"env":["CHAOJI_AK","CHAOJI_SK"],"paths":{"read":["~/.chaoji/credentials.json","~/.openclaw/workspace/chaoji/"],"write":["~/.openclaw/workspace/chaoji/"]}},"primaryEnv":"CHAOJI_AK"}}
requirements:
  credentials:
    - name: CHAOJI_AK
      source: env | ~/.chaoji/credentials.json
    - name: CHAOJI_SK
      source: env | ~/.chaoji/credentials.json
  permissions:
    - type: file_read
      paths:
        - ~/.chaoji/credentials.json
        - ~/.openclaw/workspace/chaoji/
    - type: file_write
      paths:
        - ~/.openclaw/workspace/chaoji/
    - type: exec
      commands:
        - python
---

# chaoji-img2img

## Overview

AI 图生图（素材生成），根据参考图和文字描述生成全新图片。支持最多 14 张参考图，适用于电商素材生成、风格迁移、创意设计等场景。

## Dependencies

- credentials: `CHAOJI_AK` + `CHAOJI_SK` 环境变量或 `~/.chaoji/credentials.json`
- commands: `image2image`

## Core Workflow

```
Preflight -> Execute -> Deliver
```

### Preflight

1. 检查凭证：验证 `CHAOJI_AK` 和 `CHAOJI_SK` 是否配置
2. 确认用户提供了参考图和文字描述

### Execute

**参数提取**：
- `img` *: 参考图列表（1~14 张，本地路径/URL/OSS Path）
- `prompt` *: 生成图片的文字描述（不超过 4000 字符）
- `ratio`: 生图比例（默认 auto）。可选值：auto, 1:1, 3:4, 4:3, 9:16, 16:9, 2:3, 3:2, 21:9
- `resolution`: 生成分辨率（默认 1k）。可选值：1k, 2k

**调用 API**

```bash
python chaoji-tools/scripts/run_command.py \
  --command image2image \
  --input-json '{"img": ["oss/path/ref.jpg"], "prompt": "一件白色T恤的电商主图"}'
```

或直接调用 Python 脚本：
```bash
python skills/chaoji-img2img/scripts/img2img.py \
  --img ref.jpg \
  --prompt "一件白色T恤的电商主图"
```

### Deliver

输出结果：
1. 返回生成的图片 URL 列表
2. 自动下载到本地
3. 提供下一步建议（如：调整 prompt 重新生成、更换参考图等）

## Input Format

### 基本输入（单张参考图）

```json
{
  "img": ["参考图"],
  "prompt": "生成描述"
}
```

### 多参考图 + 自定义比例

```json
{
  "img": ["参考图1", "参考图2", "参考图3"],
  "prompt": "生成描述",
  "ratio": "3:4",
  "resolution": "2k"
}
```

## Usage Examples

### 示例 1：基本图生图

```bash
python skills/chaoji-img2img/scripts/img2img.py \
  --img "https://example.com/reference.jpg" \
  --prompt "将这件衣服放在简约白色背景上，电商风格"
```

### 示例 2：多参考图 + 高分辨率

```bash
python skills/chaoji-img2img/scripts/img2img.py \
  --img ref1.jpg --img ref2.jpg --img ref3.jpg \
  --prompt "结合以上参考生成时尚海报" \
  --ratio 3:4 --resolution 2k
```

## Error Handling

1. **CREDENTIALS_MISSING** - 修复：设置 CHAOJI_AK / CHAOJI_SK
2. **INPUT_ERROR** - 缺少参考图或 prompt；参考图超过 14 张
3. **API_ERROR** - 检查网络连接，稍后重试
4. **TIMEOUT** - 稍后重试
5. **QUOTA_EXCEEDED** - [充值入口](https://open.chaoji.com/order)

## Best Practices

### 参考图

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB
- 图片越清晰、构图越明确，生成效果越好

### Prompt 编写建议

- 描述越具体，效果越好
- 可以指定风格、场景、光线、色调等
- 最多 4000 字符

### ratio 选择

- 电商主图 -> `1:1`
- 竖版海报/手机壁纸 -> `9:16` 或 `3:4`
- 横版海报/Banner -> `16:9` 或 `21:9`
- 自动匹配参考图 -> `auto`（默认）

## Security

- 凭证通过环境变量或加密文件存储
- 输入参数经过严格验证
- 输出文件存储在受信任目录

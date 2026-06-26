---
name: chaoji-tryon-shoes
description: AI 鞋靴试穿助手。将鞋商品图穿到模特脚上，生成逼真试穿效果。Triggered when user says "试鞋", "鞋靴试穿", "鞋试穿", "把鞋穿上", "shoes tryon", etc.
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

# chaoji-tryon-shoes

## Overview

AI 鞋靴试穿助手，将鞋商品图穿到真人模特脚上，生成逼真的试穿效果图。使用专业模式（tryon_type=5），版型和材质还原效果优。

## Dependencies

- credentials: `CHAOJI_AK` + `CHAOJI_SK` 环境变量或 `~/.chaoji/credentials.json`
- commands: `tryon_shoes`

## Core Workflow

```
Preflight -> Execute -> Deliver
```

### Preflight

1. 检查凭证
2. 确认提供了鞋图和模特图

### Execute

**参数提取**（全部必填）：
- `list_images_shoe`: 鞋商品图列表（1~3 张，本地路径/URL/OSS Path）
- `list_images_human`: 模特图片（目前只取第一张）

提供多张不同角度的鞋图可以获得更好的试穿效果。

**调用 API**

```bash
# 单张鞋图
python chaoji-tools/scripts/run_command.py \
  --command tryon_shoes \
  --input-json '{"list_images_shoe": ["oss/path/shoe.jpg"], "list_images_human": ["oss/path/model.jpg"]}'

# 多张鞋图
python chaoji-tools/scripts/run_command.py \
  --command tryon_shoes \
  --input-json '{"list_images_shoe": ["shoe1.jpg", "shoe2.jpg", "shoe3.jpg"], "list_images_human": ["model.jpg"]}'
```

或直接调用 Python 脚本：
```bash
python skills/chaoji-tryon-shoes/scripts/tryon_shoes.py \
  "https://example.com/model.jpg" \
  --shoe "https://example.com/shoe.jpg"
```

### Deliver

1. 返回生成的图片 URL 列表
2. 自动下载到本地

## Input Format

### 单张鞋图

```json
{
  "list_images_shoe": ["鞋商品图"],
  "list_images_human": ["模特图"]
}
```

### 多张鞋图（效果更好）

```json
{
  "list_images_shoe": ["鞋图1", "鞋图2", "鞋图3"],
  "list_images_human": ["模特图"]
}
```

## Usage Examples

### 示例 1：单张鞋图

```bash
python skills/chaoji-tryon-shoes/scripts/tryon_shoes.py \
  "https://example.com/model.jpg" \
  --shoe "https://example.com/shoe.jpg"
```

### 示例 2：多张鞋图

```bash
python skills/chaoji-tryon-shoes/scripts/tryon_shoes.py \
  "https://example.com/model.jpg" \
  --shoe "https://example.com/front.jpg" \
  --shoe "https://example.com/side1.jpg" \
  --shoe "https://example.com/side2.jpg"
```

## Error Handling

1. **CREDENTIALS_MISSING** - 凭证缺失
2. **INPUT_ERROR** - 缺少鞋图或模特图；或鞋图超过 3 张
3. **API_ERROR** - API 调用失败
4. **TIMEOUT** - 任务超时
5. **QUOTA_EXCEEDED** - 配额不足

## Best Practices

### 输入图片要求

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB
- 鞋商品图清晰、背景简洁效果最佳
- 模特图姿势自然，脚部清晰可见

## Security

- 凭证通过环境变量或加密文件存储
- 输入参数经过严格验证
- 所有图片参数统一处理为 OSS Path 后传入 API

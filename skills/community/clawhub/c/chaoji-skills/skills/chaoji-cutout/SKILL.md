---
name: chaoji-cutout
description: AI 智能抠图助手。支持人像抠图、服装分割、图案抠图、通用抠图和智能抠图。Triggered when user says "抠图", "去背景", "分割", "cutout", "segmentation", etc.
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

# chaoji-cutout

## Overview

AI 智能抠图，支持多种抠图模式。同步接口，即时返回结果（透明底图 + mask 灰度图）。

## Dependencies

- credentials: `CHAOJI_AK` + `CHAOJI_SK` 环境变量或 `~/.chaoji/credentials.json`
- commands: `cutout`

## Core Workflow

```
Preflight -> Execute -> Deliver
```

### Execute

**参数提取**：
- `image` *: 待抠图图片（本地路径/URL/OSS Path）
- `method`: 抠图模式（默认 auto）
  - `auto` — 智能抠图（自动识别，推荐）
  - `seg` — 人像抠图
  - `clothseg` — 服装分割
  - `patternseg` — 图案抠图
  - `generalseg` — 通用抠图
- `cate_token`: 仅 `clothseg` 模式生效，指定服装类别
  - `upper` — 上装
  - `lower` — 下装
  - `overall` — 全身装（默认）

**调用 API**

```bash
# 智能抠图（默认）
python chaoji-tools/scripts/run_command.py \
  --command cutout \
  --input-json '{"image": "oss/path/photo.jpg"}'

# 服装分割（上装）
python chaoji-tools/scripts/run_command.py \
  --command cutout \
  --input-json '{"image": "oss/path/photo.jpg", "method": "clothseg", "cate_token": "upper"}'
```

或直接调用 Python 脚本：
```bash
python skills/chaoji-cutout/scripts/cutout.py photo.jpg
python skills/chaoji-cutout/scripts/cutout.py photo.jpg --method clothseg --cate-token upper
```

### Deliver

本接口为**同步接口**，即时返回两个结果：
1. **view_image** — 抠图前景透明底图（RGBA 四通道）
2. **image_mask** — mask 灰度图（单通道 alpha 值）

## Input Format

### 智能抠图（推荐）

```json
{
  "image": "图片路径/URL/OSS Path"
}
```

### 指定模式

```json
{
  "image": "图片",
  "method": "clothseg",
  "cate_token": "upper"
}
```

## Usage Examples

### 示例 1：智能抠图

```bash
python skills/chaoji-cutout/scripts/cutout.py "https://example.com/photo.jpg"
```

### 示例 2：人像抠图

```bash
python skills/chaoji-cutout/scripts/cutout.py photo.jpg --method seg
```

### 示例 3：服装分割（上装）

```bash
python skills/chaoji-cutout/scripts/cutout.py model.jpg --method clothseg --cate-token upper
```

## Error Handling

1. **CREDENTIALS_MISSING** - 修复：设置 CHAOJI_AK / CHAOJI_SK
2. **INPUT_ERROR** - 图片 URL 无效或 method 不在可选范围
3. **API_ERROR** - 检查网络连接，稍后重试
4. **QUOTA_EXCEEDED** - [充值入口](https://open.chaoji.com/order)

## Best Practices

### 图片要求

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB

### method 选择建议

- 不确定用哪个 -> `auto`（默认，推荐）
- 人物照片去背景 -> `seg`
- 从穿着照中分割出服装 -> `clothseg`
- 抠出衣服上的图案/Logo -> `patternseg`
- 抠出任意物体 -> `generalseg`

## Security

- 凭证通过环境变量或加密文件存储
- 输入参数经过严格验证
- 输出文件存储在受信任目录

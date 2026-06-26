---
name: chaoji-tryon
description: AI 真人试衣助手（模特试衣）。使用 human_tryon API，支持真人模特换装，效果更逼真。Triggered when user says "真人试衣", "模特换装", "把衣服穿到真人身上", "human tryon", "换装", etc.
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

# chaoji-tryon

## Overview

AI 真人试衣助手（模特试衣），使用 `human_tryon` API 将服装图片穿到真人模特身上，生成高质量的试衣效果图。相比快速试衣（`chaoji-tryon-fast`），本接口使用更高级的模型，效果更逼真。

## Dependencies

- credentials: 潮际 AI 开放平台 API 凭证
  - 凭证配置：`CHAOJI_AK` + `CHAOJI_SK` 环境变量或 `~/.chaoji/credentials.json`
- commands:
  - `human_tryon` — 真人试衣（模特换装）

## Core Workflow

```
Preflight -> [Context] -> Execute -> Refine -> Deliver -> [Record]
```

### Preflight

1. 检查凭证：验证 `CHAOJI_AK` 和 `CHAOJI_SK` 是否配置
2. 检测模式：cwd 有 `openclaw.yaml` -> project mode; else -> one-off
3. 解析输出目录：project mode -> `./output/` | one-off -> `~/.openclaw/workspace/chaoji/output/`
4. 创建目录：`mkdir -p {output_dir}`

### Context（可选，project mode 专属）

读取用户偏好和记忆（如果存在）：
- `~/.openclaw/workspace/chaoji/PREFERENCE.md` — 用户偏好
- `~/.openclaw/workspace/chaoji/memory/tryon.md` — 历史试衣记录

### Execute

**需求分析**

1. **识别输入类型**：
   - 用户提供服装图 + 模特图 -> 直接试衣
   - 用户只提供服装图 -> 询问模特图
   - 用户只提供模特图 -> 询问服装图

2. **参数提取**（必填标 *）：
   - `image_cloth` *: 服装图片（URL 或本地路径，支持真人穿着图）
   - `list_images_human` *: 模特图片列表（目前只取第一张）
   - `cloth_length` *: 服装区域 — `upper`(上装) / `lower`(下装) / `overall`(全身/连衣裙)
   - `dpi`: 输出 DPI（默认 300）
   - `output_format`: 输出格式 jpg/png（默认 jpg）

**输入处理**

支持三种输入格式：
- **本地文件**：自动上传到 OSS -> 获取 URL
- **URL**：直接使用
- **OSS Path**：自动拼接为完整 URL

**调用 API**

使用统一执行器：
```bash
python chaoji-tools/scripts/run_command.py \
  --command human_tryon \
  --input-json '{"image_cloth": "https://...", "list_images_human": ["https://..."], "cloth_length": "overall"}'
```

或直接调用 Python 脚本：
```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "https://example.com/cloth.jpg" \
  "https://example.com/model.jpg" \
  --cloth-length overall
```

### Refine

质量检查（可选）：
1. 检查生成结果是否成功
2. 如失败，提供修复建议（如调整 cloth_length、更换图片等）

### Deliver

输出结果：
1. 返回生成的图片 URL 列表
2. 自动下载到本地（project mode）
3. 提供下一步建议

## Input Format

### 基本输入

```json
{
  "image_cloth": "服装图片 URL",
  "list_images_human": ["模特图片 URL"],
  "cloth_length": "overall"
}
```

### 完整选项

```json
{
  "image_cloth": "服装图片 URL",
  "list_images_human": ["模特图片 URL"],
  "cloth_length": "upper",
  "dpi": 300,
  "output_format": "jpg"
}
```

## Usage Examples

### 示例 1：全身换装

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "https://example.com/dress.jpg" \
  "https://example.com/model.jpg" \
  --cloth-length overall
```

### 示例 2：上装换装

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "https://example.com/top.jpg" \
  "https://example.com/model.jpg" \
  --cloth-length upper
```

### 示例 3：下装换装

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "/path/to/pants.jpg" \
  "/path/to/model.jpg" \
  --cloth-length lower --format png --dpi 600
```

## Error Handling

### 常见错误类型

1. **CREDENTIALS_MISSING** - 凭证缺失
   - 修复：设置环境变量 CHAOJI_AK 和 CHAOJI_SK

2. **INPUT_ERROR** - 输入错误
   - 修复：检查图片 URL 是否有效，cloth_length 是否为 upper/lower/overall

3. **API_ERROR** - API 调用失败
   - 修复：检查网络连接，稍后重试

4. **TIMEOUT** - 任务超时
   - 修复：稍后重试

5. **QUOTA_EXCEEDED** - 配额不足
   - 修复：[充值入口](https://open.chaoji.com/order)

## Best Practices

### 输入图片要求

**服装图片**（image_cloth）：
- 格式：JPG, PNG, JPEG, BMP, WEBP
- 大小：不超过 20MB
- 可以是服装平铺图，也可以是真人穿着图
- 清晰的服装正面图效果最佳

**模特图片**（list_images_human）：
- 格式：JPG, PNG, JPEG, BMP, WEBP
- 大小：不超过 20MB
- 清晰的全身人像照片
- 姿势自然，身体完整可见

### 参数选择建议

**cloth_length**:
- 上装（T恤、衬衫、外套）-> `upper`
- 下装（裤子、裙子）-> `lower`
- 连衣裙、套装、全身 -> `overall`

## Security

- 凭证通过环境变量或加密文件存储
- 不执行用户提供的任意代码
- 输入参数经过严格验证
- 输出文件存储在受信任目录

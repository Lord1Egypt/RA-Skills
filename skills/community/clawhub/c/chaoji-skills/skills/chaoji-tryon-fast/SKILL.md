---
name: chaoji-tryon-fast
description: 快速虚拟试衣助手（快速版）。使用 model_tryon_quick API，速度快，适合快速预览试衣效果。Triggered when user says "快速试衣", "试试这件衣服（快速）", "quick tryon", etc.
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

# chaoji-tryon-fast

## Overview

AI 虚拟试衣助手（快速版）。分析用户输入，调用 ChaoJi API (`model_tryon_quick`) 生成逼真的上身效果图片。

## Dependencies

- runner: 内置 Python runner (chaoji-tools/scripts/run_command.py)
- credentials: 潮际 AI 开放平台 API 凭证
  - 凭证配置：`CHAOJI_AK` + `CHAOJI_SK` 环境变量或 `~/.chaoji/credentials.json`
- command: `model_tryon_quick` — 快速试衣

## Core Workflow

```
Preflight → [Context] → Execute → Refine → Deliver → [Record]
```

### Preflight

1. 检查凭证：验证 `CHAOJI_AK` 和 `CHAOJI_SK` 是否配置
2. 检测模式：cwd 有 `openclaw.yaml` → project mode; else → one-off
3. 解析输出目录：project mode → `./output/` | one-off → `~/.openclaw/workspace/chaoji/output/`
4. 创建目录：`mkdir -p {output_dir}`

### Context（可选，project mode 专属）

读取用户偏好和记忆（如果存在）：
- `~/.openclaw/workspace/chaoji/PREFERENCE.md` — 用户偏好（常用参数、风格偏好）
- `~/.openclaw/workspace/chaoji/memory/tryon.md` — 历史试衣记录
- `./DESIGN.md` — 项目设计规范（如果有）

### Execute

**需求分析**

1. **识别输入类型**：
   - 用户提供服装图 + 模特图 → 直接试衣
   - 用户只提供服装图 → 询问模特图或使用默认模特
   - 用户提供文字描述 → 需要先生成服装或模特

2. **调用命令**：使用 `model_tryon_quick` 执行试衣

3. **参数提取**：
   - `cloth_input`: 服装图片（必填）
   - `human_input`: 模特图片（必填，可选默认）
   - `cloth_length`: 上身区域（upper/lower/overall，默认 overall）
   - `batch_size`: 生成数量（1-8，默认 1）
   - `dpi`: 输出 DPI（默认 300）
   - `format`: 输出格式（jpg/png，默认 jpg）

**输入处理**

支持三种输入格式：
- **本地文件**：自动上传到 OSS → 获取 OSS Path
- **URL**：提取 OSS Path 或直接使用
- **OSS Path**：直接使用

**调用 API**

使用统一执行器：
```bash
python chaoji-tools/scripts/run_command.py \
  --command model_tryon_quick \
  --input-json '{"image_cloth": "...", "list_images_human": [...]}'
```

### Refine

质量检查（可选）：
1. 检查生成结果是否成功
2. 验证输出图片质量
3. 如失败，提供修复建议

### Deliver

输出结果：
1. 返回生成的图片 URL 列表
2. 自动下载到本地（project mode）
3. 提供下一步建议（如：调整参数重新生成、尝试其他风格）

### Record（project mode 专属）

记录用户偏好：
- 使用的参数配置
- 生成的风格偏好
- 用户反馈（如满意/不满意）

## Input Format

### 基本输入

```json
{
  "cloth_input": "服装图片路径/URL/OSS Path",
  "human_input": "模特图片路径/URL/OSS Path"
}
```

### 高级选项

```json
{
  "cloth_input": "服装图片",
  "human_input": "模特图片",
  "cloth_length": "overall",
  "batch_size": 4,
  "dpi": 300,
  "format": "jpg"
}
```

## Usage Examples

### 示例 1：快速试衣（本地文件）

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "/path/to/cloth.jpg" \
  "/path/to/model.jpg"
```

### 示例 2：使用 URL

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "https://example.com/cloth.jpg" \
  "https://example.com/model.jpg"
```

### 示例 3：使用 OSS Path

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "marketing/image/1/xxx/cloth.jpg" \
  "marketing/image/1/xxx/model.jpg"
```

### 示例 4：批量生成

```bash
python skills/chaoji-tryon/scripts/tryon.py \
  "cloth.jpg" "model.jpg" \
  --batch-size 4 --cloth-length upper
```

## Error Handling

### 常见错误类型

1. **CREDENTIALS_MISSING** - 凭证缺失
   - 用户提示：检测到未配置潮际 API 凭证
   - 修复建议：设置环境变量 CHAOJI_AK 和 CHAOJI_SK

2. **INPUT_ERROR** - 输入错误
   - 用户提示：输入参数有误（如缺少服装图或模特图）
   - 修复建议：检查输入文件路径是否正确

3. **API_ERROR** - API 调用失败
   - 用户提示：调用潮际 API 时发生错误
   - 修复建议：检查网络连接，稍后重试

4. **TIMEOUT** - 任务超时
   - 用户提示：任务执行超时
   - 修复建议：减少并发任务数或稍后重试

5. **QUOTA_EXCEEDED** - 配额不足
   - 用户提示：账户余额或配额不足
   - 修复建议：[充值入口](https://open.chaoji.com/order)

## Best Practices

### 输入图片要求

**服装图片**：
- 清晰的服装正面图
- 背景简洁（纯色最佳）
- 光线均匀，无明显阴影
- 建议分辨率：800x800 以上

**模特图片**：
- 清晰的人像照片
- 姿势自然，身体完整可见
- 避免遮挡躯干
- 建议分辨率：800x1200 以上

### 参数选择建议

**cloth_length**:
- 上装 → `upper`
- 下装（裤子/裙子）→ `lower`
- 连衣裙/全身 → `overall`

**batch_size**:
- 快速预览 → 1
- 选择最佳 → 4
- A/B 测试 → 8

**dpi**:
- 网络使用 → 72-150
- 打印使用 → 300
- 高质量打印 → 600

## Security

- 凭证通过环境变量或加密文件存储
- 不执行用户提供的任意代码
- 输入参数经过严格验证
- 输出文件存储在受信任目录

---
name: cs-free-image-generator-nv
description: 使用 NVIDIA MoCL 模型（via NVIDIA API Playground）进行免费文图生成（Text-to-Image）。当用户要求"生成图片"、"画一张图"、"text to image"、"文生图"时触发。
---

# NVIDIA MoCL 文图生成

基于 NVIDIA API Playground 的 MoCL 模型，将自然语言描述转化为图像。

## 使用方式

```bash
python3 scripts/cs-free-image-generator-nv.py \
  --prompt "描述文字" \
  --width 1024 \
  --height 1024
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | ✅ | — | 图像描述文本（英文效果更佳） |
| `--width` | ✅ | — | 图像宽度（1-4096） |
| `--height` | ✅ | — | 图像高度（1-4096） |

## 输出

- 响应 JSON 保存至：`/tmp/cs-free-image-generator/nv/<Unix时间戳>.json`
- 包含 base64 编码的图像数据，可解码保存为 PNG/JPEG 文件

## 示例

```bash
# 生成一只可爱的柯基犬 (1024×1024)
python3 scripts/cs-free-image-generator-nv.py \
  --prompt "一只可爱的柯基犬" \
  --width 1024 \
  --height 1024
```

## 注意事项

- **环境变量**：使用 `dotenv` 自动从 `~/.openclaw/.env` 加载 `NVIDIA_API_KEY`（`override=True`），强制从 `.env` 读取最新值，避免旧进程缓存干扰。
- 宽高限制：1-4096，超出范围会报错
- 响应体自动保存，方便追溯调用结果

---
name: ai-image-gen
description: AI图片生成技能，使用Gemini生成高质量图片，支持文生图和图生图
version: 1.0.0
author: 小帽
grade: A
category: media
tags: [图片, AI, gemini, 生成]
---

# AI图片生成技能

使用 AI 生成高质量图片。

## 核心命令

```bash
uv run /usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "你的描述" --filename "output.jpg" --resolution 2K
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 图片描述（中英文都行） |
| `--filename` | 输出文件名 |
| `--resolution` | 分辨率：1K / 2K |
| `-i reference.jpg` | 可选：参考图片（风格迁移、图片编辑） |

## 使用示例

### 文生图

```bash
# 生成产品封面
uv run /usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "极简白色背景产品展示图，现代科技感" \
  --filename cover.jpg \
  --resolution 2K
```

### 图生图（风格迁移）

```bash
# 基于参考图修改
uv run /usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "把背景改成蓝天白云" \
  -i original.jpg \
  --filename edited.jpg
```

### 常用场景

```bash
# 公众号封面
--prompt "公众号封面：AI技术，科技感，简洁大气"

# 产品图
--prompt "产品展示图，白色背景，专业摄影风格"

# 插图
--prompt "文章配图：数据分析，图表，商务风格"
```

## 注意事项

- 需要 `GEMINI_API_KEY` 环境变量
- 支持 1K 和 2K 分辨率
- 中英文 prompt 都支持

---

*技能创建时间: 2026-03-17*

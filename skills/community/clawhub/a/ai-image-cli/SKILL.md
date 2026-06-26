---
name: ai-image-cli
version: 1.0.0
description: >
  AI 图像生成工具。支持文生图(text2img)和图生图(img2img)功能，基于 AIGW API。
  激活场景：生成图片、画图、制作图像、修改图片、图片编辑、
  或提到 "生成图片"、"画一个"、"创建图像"、"修改这张图"、"改成"、"转为图片" 时激活。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨"
      }
  }

---

# AI Image — AI 图像生成技能

`ai-image-cli` 是 AI 图像生成工具，支持文生图和图生图两大核心能力。

| 能力 | 提供商 | 模型 | 说明 |
|------|--------|------|------|
| 文生图 | AIGW | doubao-seedream-4-5 | 根据文本描述生成图片 |
| 图生图 | AIGW | doubao-seededit-3-0-i2i | 基于源图片和文本生成新图片 |

## 命令选择

根据用户意图，直接选择对应子命令：

- **用户想根据描述生成新图片** → `ai-image text2img "<描述>"`
- **用户提供了图片 URL，想要修改或编辑** → `ai-image img2img "<修改描述>" <URL>`
- **查看工具能力** → `ai-image capabilities`

## 命令速查

| 命令 | 用途 | 关键选项 |
|------|------|----------|
| `ai-image text2img "<描述>"` | 文生图 | `-s` 尺寸, `--seed` 种子, `-g` 引导系数, `--watermark` |
| `ai-image img2img "<描述>" <URL>` | 图生图 | `--seed` 种子, `-g` 引导系数, `--watermark` |
| `ai-image capabilities` | 查看工具能力(JSON) | 无参数，无需认证 |

所有命令输出 JSON 格式，`success` 字段标识成功或失败。

## Quick Start

直接执行命令即可，无需预检。如果命令不存在或返回错误，再执行环境诊断：

```bash
# 诊断环境
bash {baseDir}/scripts/preflight.sh

# 如果 cli_installed: false，执行安装
bash {baseDir}/scripts/install.sh
```

## 常用工作流

### 文生图 (text2img)

```bash
# 基本用法
ai-image text2img "一个中国女孩,高清"

# 指定尺寸
ai-image text2img "夕阳下的海滩" --size 1920x1920

# 使用随机种子(可复现)
ai-image text2img "雪山风景" --seed 12345

# 完整参数
ai-image text2img "城市夜景" --size 1920x1920 --seed 999 --guidance-scale 3.0 --watermark
```

**常用参数：**
- `--size, -s`: 图片尺寸，如 `1920x1920`(默认: `1920x1920`，最低尺寸：`1920x1920`)
- `--seed`: 随机种子，用于复现相同结果
- `--guidance-scale, -g`: 引导系数，控制生成质量(默认: `2.5`)
- `--watermark / --no-watermark`: 是否添加水印(默认: 不添加)

### 图生图 (img2img)

**注意**: 图生图不支持指定尺寸参数，输出图片尺寸由源图片决定。

```bash
# 基本用法
ai-image img2img "改成爱心形状的泡泡" https://example.com/image.jpg

# 使用随机种子
ai-image img2img "改变颜色为红色" https://example.com/car.jpg --seed 777

# 调整引导系数
ai-image img2img "转为水彩画风格" https://example.com/pic.png --guidance-scale 6.0

# 完整参数
ai-image img2img "添加蓝天白云" https://example.com/photo.png \
  --seed 888 --guidance-scale 6.0 --watermark
```

**常用参数：**
- `--seed`: 随机种子，用于复现相同结果
- `--guidance-scale, -g`: 引导系数，控制编辑强度(默认: `5.5`)
- `--watermark / --no-watermark`: 是否添加水印(默认: 不添加)

## 输出格式

### 成功响应

```json
{
  "success": true,
  "command": "text2img",
  "provider": "ark",
  "data": {
    "model": "doubao-seedream-4-5",
    "created": 1754384045,
    "data": [
      {
        "url": "https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/..."
      }
    ],
    "usage": {
      "generated_images": 1,
      "output_tokens": 4096,
      "total_tokens": 4096
    }
  }
}
```

### 错误响应

```json
{
  "success": false,
  "command": "text2img",
  "error": "未找到 AIGW API Key",
  "hint": "请设置 LANGBASE_TOKEN 或 ARK_API_KEY 环境变量"
}
```

## 故障恢复

命令执行失败时，按以下步骤排查：

1. **命令不存在** (`command not found`): 执行 `bash {baseDir}/scripts/install.sh`
2. **认证失败** (`AUTH_FAILED` 或 `未找到 AIGW API Key`): 执行 `bash {baseDir}/scripts/preflight.sh` 查看诊断。若 `auth_configured: false`，说明 `LANGBASE_TOKEN` 环境变量未注入当前进程，需确认 `~/.openclaw/user.env` 中包含 `LANGBASE_TOKEN`。
3. **网络/API 错误**: 重试一次。若持续失败，执行 preflight 检查连通性。

## 未全局安装时的备选方式

```bash
python3 -m ai_image text2img "查询词"
python3 -m ai_image img2img "修改描述" "https://example.com/image.jpg"
```

## 参考文档

- 完整 CLI 参考（参数、返回结构、错误码）：读取 `references/cli-reference.md`
- 更多高级示例（批量生成、参数调优）：读取 `references/examples.md`

---
name: dmxapi-image-generation
description: 使用 DMXAPI 平台生成和编辑图片。支持 Gemini、Seedream（豆包即梦）、OpenAI 等多种模型。可进行文生图、图片编辑、多图融合、联网搜索增强生图。当用户需要生成图片、编辑图片、AI 绘图、多图融合时使用此技能。
compatibility: Requires Node.js 20+ and dmxapi-cli installed
metadata:
  author: onee-io
  version: "1.0.1"
---

# DMXAPI 图片生成/编辑

通过 DMXAPI 统一 CLI 调用多种 AI 模型生成和编辑图片。

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
dmxapi image [options] <prompt>
```

## 选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `-m, --model <model>` | 模型名称（默认 `gemini-3.1-flash-image-preview`，推荐） | `-m gemini-3.1-flash-image-preview` |
| `--size <ratio>` | 图片比例：`auto`, `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | `--size 16:9` |
| `--quality <level>` | 分辨率：`1K`（默认）、`2K`、`4K` | `--quality 2K` |
| `-n, --count <n>` | 生成数量 | `-n 3` |
| `--image <path>` | 输入图片路径（可重复多次实现多图融合） | `--image ./photo.png` |
| `--web-search` | 启用联网搜索增强 | `--web-search` |
| `-o, --save <dir>` | 保存目录（默认当前目录） | `-o ./output` |
| `-p, --param <k=v>` | 额外 API 参数（可重复） | `-p watermark=true` |

## 模型

默认使用 `gemini-3.1-flash-image-preview`（推荐），效果最佳，支持生图、编辑和联网搜索。一般无需指定 `-m` 参数。

如需使用其他模型（如 `doubao-seedream-5.0-lite`、`dall-e-3` 等），通过 `-m` 指定即可。

## 使用步骤

1. 根据用户需求确定提示词、模型、尺寸、质量等参数
2. 构建 `dmxapi image` 命令并执行
3. 图片自动保存到指定目录，将保存路径告知用户

## 示例

```bash
# 文生图
dmxapi image "一只在月球上骑自行车的猫" -o ./output

# 指定比例和质量
dmxapi image "日落风景" --size 16:9 --quality 2K -o ./output

# 图片编辑
dmxapi image "把背景改成星空" --image ./photo.png -o ./output

# 多图融合
dmxapi image "将这两张图片融合成一幅画" --image ./a.png --image ./b.png -o ./output

# 联网搜索增强
dmxapi image "最新款 iPhone 产品图" --web-search -o ./output

# 生成多张
dmxapi image "三只不同颜色的猫" -n 3 -o ./output
```

## 注意事项

- 建议始终用 `-o` 指定输出目录
- 图片编辑需提供本地图片文件路径（支持 png/jpg/webp/gif）

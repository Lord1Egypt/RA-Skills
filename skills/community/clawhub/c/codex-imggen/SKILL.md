---
name: codex-imggen
version: 1.1.1
description: "通过 Codex CLI 生成图片，支持尺寸控制和批量模式。依赖：codex (npm)。代理默认启用。用 generate.sh 生成单张，batch_generate.sh 批量生成游戏 UI 素材，gen_size.sh 指定尺寸。所有输出保存至 ~/.codex/generated_images/。"
metadata: {"openclaw":{"emoji":"🎨","requires":{"anyBins":["codex"]}}}
---

# Codex 图片生成

> ⚠️ **美术必读 — 尺寸限制**：Codex CLI 最大输出约 1.57MP（1254×1254 级别），所有尺寸都会被卡在这个上限内。**4K/FHD/2K 都会降级**，不会真的输出那些尺寸。详见下方安全尺寸表。
>
> ⏱️ **超时注意**：Codex CLI 生图耗时较长（约 30~90 秒），调用时 timeout 应设不低于 **180 秒**，避免 agent 误判为失败而中断重试。

## 注意事项

> **完成后看一眼生成的图对不对**：Codex CLI 报错信息不一定准——报“failed N times with a server error”不一定真没生成。Agent 有视觉能力就调一下 image 工具看一眼生成的图是否对需求；没生成或内容不对，重试即可。

## 尺寸限制速查

| 用途 | 推荐尺寸 | 实际输出 | 风险 |
|------|---------|---------|------|
| **方图素材（安全）** | `1K` / `1:1` / `square` | 1254×1254 | ✅ 无缩放 |
| **横版大图（安全）** | `1536x1024` | 1536×1024 | ✅ 无缩放（唯一精确大尺寸） |
| **竖版素材（安全）** | `9:16` | 941×1672 | ✅ 无缩放 |
| **横版4:3（安全）** | `4:3` | 1448×1086 | ✅ 无缩放 |
| **16:9 横版** | `2K` / `FHD` / `16:9` | 1672×941 | ⚠️ 实际只有 HD 级 |
| **4K / 1080p / 720p** | ❌ 勿用 | 全部降级至 1672×941 | ❌ 严重缩水 |
| **小图如 512×512** | ❌ 勿用 | 膨胀至 1254×1254 | ❌ 严重放大 |

**结论**：游戏 UI 素材推荐用 `1K`（方图）或 `1536x1024`（横版），不要用 FHD/4K/720p 等标识。

## 快速参考

| 任务 | 命令 |
|------|------|
| 单张图片 | `bash ~/.openclaw/skills/codex-imggen/scripts/generate.sh "<prompt>" [output_dir] [-i <ref_image>]` |
| 指定尺寸 | `bash ~/.openclaw/skills/codex-imggen/scripts/gen_size.sh <size_key> "<subject>" [output_dir] [-i <ref_image>]` |
| 批量游戏 UI | `bash ~/.openclaw/skills/codex-imggen/scripts/batch_generate.sh "<style>" <count> [output_dir] [-i <ref_image>]` |

## 尺寸 Key（gen_size.sh）

| Key | 实际输出 | 比例 | MP | 精确度 |
|-----|---------|------|-----|--------|
| `1K` / `1:1` / `square` | 1254×1254 | 1:1 | ~1.57MP | ✅ ~1K（差 <3%） |
| `2K` / `16:9` / `FHD` | 1672×941 | 16:9 | ~1.57MP | ⚠️ ~2K（面积差 -22%） |
| `2048x1080` | 1727×911 | ~17:9 | ~1.57MP | ✅ 2K 最佳匹配 |
| `4K` / `3840x2160` | 1672×941 | 16:9 | ~1.57MP | ❌ 无法达到 4K |
| `9:16` | 941×1672 | 9:16 | ~1.57MP | ✅ 竖版 |
| `4:3` | 1448×1086 | 4:3 | ~1.57MP | ✅ |
| `1536x1024` | 1536×1024 | 3:2 | ~1.57MP | ✅ 完全精确 |
| `720p` / `HD` | 1672×941 | 16:9 | ~1.57MP | ⚠️ 等同 2K |

> **可选参数 `-i <ref_image>`**：传入参考图路径，Codex 会将参考图作为生成上下文，适用于风格迁移、色调匹配等场景。不传此参数则走默认行为。

## 生成图片

### 单张图片
```bash
# 无参考图
bash ~/.openclaw/skills/codex-imggen/scripts/generate.sh \
  "A fantasy sword with golden blade on white background (#ffffff), flat vector art style" \
  /tmp/my-images

# 带参考图（风格迁移）
bash ~/.openclaw/skills/codex-imggen/scripts/generate.sh \
  "A fantasy sword with golden blade on white background, flat vector art style" \
  /tmp/my-images \
  -i /path/to/reference.png
```

### 指定尺寸
```bash
bash ~/.openclaw/skills/codex-imggen/scripts/gen_size.sh \
  "1K" \
  "A medieval castle on a hill at sunset" \
  /tmp/my-images
```

### 批量游戏 UI 素材（2026-05-21 实测）
```bash
bash ~/.openclaw/skills/codex-imggen/scripts/batch_generate.sh \
  "flat vector art style, white background (#ffffff), each icon approximately 256x256 pixels, consistent 2px gold (#d4af37) border, same lighting angle, centered subjects" \
  6 \
  /tmp/my-icons
```

批量生成会输出包含所有元素的一张合并大图（通常为 2x3 或 3x2 网格）。详见下方已验证的 Prompt 示例。

## 批量 Prompt 示例（2026-05-21 实测）

所有批量输出均为一张合并大图；使用 ImageMagick 或 batch_split.sh 裁剪拆分。

### RPG Icons（3x2 网格，1024×1536）
```
Generate a set of 6 RPG game UI icons in a 3x2 grid (2 columns, 3 rows), all in the same flat vector art style with a white background (#ffffff). Each icon approximately 256x256 pixels in combined image. Icons: (1) sword with golden blade, (2) shield with silver surface and red cross, (3) red health potion bottle, (4) purple crystal gem, (5) golden 5-pointed star, (6) red heart. All icons share consistent 2px gold (#d4af37) border, consistent padding, same lighting angle, centered subjects.
```

### Cyberpunk（3x2 网格，1024×1536）
```
Generate a set of 6 cyberpunk game UI elements in a 3x2 grid (2 columns, 3 rows), all in the same neon glow cyberpunk style. Each element approximately 256x256 pixels in combined image. Elements: (1) circuit board chip icon, (2) glowing cyan hexagon, (3) neon sword, (4) holographic shield, (5) power battery with lightning bolt, (6) digital eye/sensor. White background, neon colors (cyan #00ffff, magenta #ff00ff, yellow #ffff00), glow effects.
```

### Pixel Art 道具（2x3 网格，1536×1024）
```
Generate a set of 6 pixel art game items in a 2x3 grid (3 columns, 2 rows), authentic retro pixel style. Each item approximately 256x256 pixels in combined image. Items: (1) red potion, (2) green herb/plant, (3) blue mana crystal, (4) golden coin, (5) brown wooden chest, (6) white feather. White background, pixel perfect, 16-bit era style.
```

### Flat Minimal Icons（3x2 网格，1024×1536）
```
Generate a set of 6 flat minimalist game UI icons in a 3x2 grid (2 columns, 3 rows). Each icon approximately 256x256 pixels in combined image. Icons: (1) play button (triangle), (2) pause button (two bars), (3) settings cogwheel, (4) home button (house shape), (5) sound on (speaker with waves), (6) sound off (speaker with X). Style: ultra flat, solid colors, no outlines, modern mobile game aesthetic. Colors: flat blue (#4a90d9), flat white, flat gray on white background.
```

## 拆分批量输出

> ⚠️ **Layout 注意**：
> - 1024×1536 图片 → 2列 × 3行 → **3x2** layout（每格约 512×512）
> - 1536×1024 图片 → 3列 × 2行 → **2x3** layout（每格约 512×341）

```bash
# ✅ 推荐：用 batch_split.py（背景透明 + 网格拆分 + alpha 抠图一气呵成）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/batch.png 3x2 /tmp/icons/

# layout 格式：rows x cols，第一个数是行数（纵向），第二个数是列数（横向）
```

## 尺寸精确度指南

**可靠（可直接使用）：**
- `1K` / `1:1` / `square` → 1254×1254
- `2048x1080` → 1727×911（2K 最佳匹配）
- `1536x1024` → 1536×1024（完全精确！）
- `2K` / `16:9` / `FHD` → 1672×941
- `9:16` → 941×1672
- `4:3` → 1448×1086

**不可靠（避免使用）：**
- `4K` / `3840x2160` → 上限 1672×941（面积损失 95%）
- 直接请求像素尺寸如 `1920x1080` → 降级至 1672×941
- 小尺寸如 `512x512` → 膨胀至 1254×1254（大幅放大）

**需要精确尺寸**：用语义描述生成，再用 `ffmpeg` 或 PIL 裁剪/缩放至目标尺寸。

## 输出位置

所有图片保存至 `~/.codex/generated_images/<session-id>/`。脚本会自动复制最新一张到指定输出目录；未指定目录时可在该目录查找。

## 代理

代理（`http://127.0.0.1:1080`）默认启用。如代理地址不同，修改各脚本顶部的 `PROXY` 变量。

## 架构说明

```
Codex CLI → Plus 订阅 → ~1.57MP 固定输出 bucket
                                    (8 个 bucket：1:1, 16:9, 3:2, 4:3, 9:16, ~17:9)

需要 >1.57MP 分辨率：使用官方 gpt-image-2 API（planned as separate skill）
```

---
name: article-images-gen
description: 文案插图专家，为文章生成手绘风格插图。风格：手绘、简约、整洁、留白、构图平衡、色调统一。Use when user asks to generate illustrations for articles, "为文章配图", "生成插图", or needs hand-drawn style images for content.
version: 2.0.0
metadata:
  homepage: https://github.com/victor-skills/tree/main/skills/article-images-gen
---

# Article Images Generator (文案插图专家)

专为文章生成手绘风格插图，使用 `opencli gemini image`（主）和 `opencli grok image`（降级）生成图片。

## 调用脚本

```bash
# 为文章生成配图（全自动：分析 → 生成大纲 → 生成提示词 → 生成图片 → 插入文章）
bun scripts/illustrator.ts path/to/article.md [--density <level>] [--output-dir <path>]

# 单张图片（直接 prompt）
bun scripts/main.ts --prompt "your prompt" [--image output.png]

# 批量 prompt 文件
bun scripts/main.ts --promptfiles prompt1.md,prompt2.md
```

密度选项：`minimal` (1-2张) | `balanced` (3-4张) | `per-section`（推荐）| `rich` (5+张)

## 工作流程

1. **分析文案**：识别章节结构、核心论点、适合插图的位置
2. **分析判断**：AI 根据文章章节数量和内容自动选择密度（默认 per-section）
3. **生成大纲**：保存 `{outputDir}/outline.md`
4. **生成提示词**：保存 `{outputDir}/prompts/NN-hand-drawn-{slug}.md`
5. **生成图片**：调用 `opencli gemini image`，失败后降级 `opencli grok image`，保存到 `{outputDir}/`
6. **更新文章**：在对应章节后插入图片引用 `![描述](imgs/01-hand-drawn-xxx.png)`

## 图片生成策略

- **首选**：`opencli gemini image`（16:9 横版）
- **降级**：Gemini 失败时自动切换 `opencli grok image`
- **超时**：单次生成最长 300 秒

## 环境要求
- **依赖**：`opencli` 已安装且 `gemini` / `grok` 可用
- **浏览器**：opencli 需要 Chrome 浏览器支持（自动化操作 gemini.google.com / grok.com）

## 输出目录

固定输出到 `/tmp/imageGen/{YYYYMMDD}/{articleName}/`，例如：
`/tmp/imageGen/20260410/my-article/01-hand-drawn-xxx.png`

`articleName` 取文章文件名（不含扩展名），日期取当天日期。

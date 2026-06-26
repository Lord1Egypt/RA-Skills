---
name: blog-image-embedder
description: Analyze polished zh-CN blog markdown, generate hero + per-section image prompts, embed image placeholders into the markdown, and save updated version.
author: Jeff Yang
version: 1.0.4
tags: [openclaw, clawhub, blog, images, prompts, embed, markdown]
metadata:
  openclaw:
    requires: []
    platforms: ["linux", "darwin"]

inputSchema:
  type: object
  properties:
    imageModel:
      type: string
      default: "openai/gpt-5-mini"
      enum: ["openai/gpt-5-mini", "openai/dall-e-3", "stability/ai-sdxl"]

    polishedPath:
      type: string
      description: Path to polished markdown from blog-polish-zhcn
      pattern: ".*\\.md$"
    outputDir:
      type: string
      default: "~/.openclaw/workspace/contentPolished/"
    style:
      type: string
      default: "clean flat vector illustration, minimal isometric, software-engineering diagram vibe"
    background:
      type: string
      default: "white background with subtle grid"
    aspectRatioHero:
      type: string
      default: "16:9 horizontal"
    aspectRatioSection:          # ← ADD MISSING
      type: string
      default: "16:9"
    imageWidth:                  # ← SAME LEVEL as aspectRatioHero
      type: integer
      default: 800               # ← FIXED: 1200 for hero
      description: Width in pixels for hero image
    imageHeight:
      type: integer
      default: 450
    sectionWidth:
      type: integer
      default: 800
    imageQuality:
      type: string
      enum: ["low", "medium", "high", "ultra"]
      default: "medium"
    imageFormat:
      type: string
      enum: ["png", "jpg", "webp"]
      default: "png"
  required: ["polishedPath", "outputDir"]

outputSchema:
  type: object
  properties:
    illustratedPath: { type: string }
    imagePrompts: { type: array }
    imagePaths: { type: array }
  required: ["illustratedPath", "imagePrompts", "imagePaths"]
workflow:
  - name: resolve_latest_polished
    description: Find latest *.md in outputDir
    inputs: ["outputDir"]
    outputs: ["polishedPath"]
    run: |
      polishedPath="$(ls -t "$outputDir"/*.md | head -n 1)"
      save_state polishedPath "$polishedPath"

  - name: read_polished
    description: Read polished markdown from disk
    inputs: ["polishedPath"]
    outputs: ["markdownContent"]
    run: |
      polishedPath=$(load_state polishedPath)
      markdownContent="$(cat "$polishedPath")"
      save_state markdownContent "$markdownContent"

  - name: parse_sections
    description: Extract title and sections from markdown
    inputs: ["markdownContent"]
    outputs: ["title", "sections"]
    llm: true

  - name: generate_prompts
    description: Generate hero & section images using configured model
    inputs: ["sections", "style", "background", "imageModel", "imageWidth", "imageHeight", "imageQuality"]
    outputs: ["imagePrompts", "imagePaths"]
    image: true

    params:
      model: ${imageModel}
      width: ${imageWidth}
      height: ${imageHeight}
      quality: ${imageQuality}
      format: "png"

  - name: embed_placeholders
    description: Insert [image:x] placeholders and save illustrated markdown
    inputs: ["markdownContent", "imagePaths", "outputDir"]
    outputs: ["illustratedPath"]
    run: |
      markdownContent=$(load_state markdownContent)
      imagePaths=$(load_state imagePaths)
      # ...apply embedding, write to file...
      ts=$(date +"%y%m%d%H%M")
      illustratedPath="$outputDir/${ts}-illustrated.md"
      save_state illustratedPath "$illustratedPath"

  - name: finalize
    run: |
      illustratedPath=$(load_state illustratedPath)
      imagePrompts=$(load_state imagePrompts)
      imagePaths=$(load_state imagePaths)
      jq -n --arg illustratedPath "$illustratedPath" \
        --argjson imagePrompts "$(echo "$imagePrompts" | jq -c .)" \
        --argjson imagePaths "$(echo "$imagePaths" | jq -c .)" \
        '{illustratedPath:$illustratedPath,imagePrompts:$imagePrompts,imagePaths:$imagePaths}'
---

# Blog Image Embedder

Analyzes polished zh-CN markdown, generates consistent image prompts (hero + 1 per section), embeds `[image:x]` placeholders, saves illustrated version.

## When to Use  

Use **after** `blog-polish-zhcn` completes. Input is `polishedPath` from first skill. Triggers: "add images to my polished blog", "generate image prompts for sections".

## Defaults

- `style`: `clean flat vector illustration, minimal isometric, software-engineering diagram vibe`
- `background`: 
    default: `white background with subtle grid`
- `aspectRatioHero`: `16:9 horizontal`
- `aspectRatioSection`: `16:9`

## Workflow Summary

1. **Read** polished markdown from `input.polishedPath`
2. **Parse structure**: Extract title + ## section headings (expect 3-4 sections)
3. **Generate prompts**:
   - Hero: `[Hero of {title}]: {topic summary}, {style}, {background}, 16:9`
   - Section N: `[Section {N} of {title}]: {section summary}, {style}, {background}, 16:9`
4. **Embed placeholders**: Insert `\n\n[image:0]\n\n` after title, `\n\n[image:1]\n\n` after first section, etc.
5. **Save**: `${outputDir}/${ts}-illustrated.md`
6. **Return**: `{ illustratedPath, imagePrompts: [...], imagePaths: [...] }`

## Output Format

```json
{
  "illustratedPath": "/home/jeff/.openclaw/workspace/contentPolished/2603142145-illustrated.md",
  "imagePrompts": ["Hero prompt...", "Section 1 prompt...", "Section 2 prompt..."],
  "imagePaths": ["2603142145-main.png", "2603142145-section1.png", "2603142145-section2.png"]
}


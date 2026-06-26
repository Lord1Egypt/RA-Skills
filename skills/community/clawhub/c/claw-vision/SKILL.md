---


title: SKILL
date: 2026-03-29
name: claw-vision
description: Analyze images via Gemini 3.1 Pro Preview (NUWA Flux). Understand screenshots, receipts, UI, documents, and photos. Trigger: user sends any image file or says "看一下这张图/截图里是什么".
---

## 能力定位
本地图片路径 → 结构化文本理解。通过 vision-tool.py 调用 Gemini 3.1 Pro Preview（NUWA Flux）。

## 触发场景
- 用户发送截图、照片、图片文件
- 关键词：截图、图片里有什么、识别、screenshot、describe image

## 调用方式

```bash
python3 ~/Documents/OpenClaw/workspace/scripts/vision-tool.py <图片绝对路径> "<提示语>"
```

## 参数
| 参数 | 必填 | 默认值 |
|------|------|--------|
| 图片路径 | ✅ | — |
| 提示语 | ✅ | "图片里有什么？" |

## 支持格式
PNG / JPG / JPEG / GIF / WEBP（仅本地文件，不支持URL）

## 输出规范

```
[summary]     图片内容概述
[fields]      关键字段提取（含文字/表格时）
[ui_elements] 界面元素列表（UI截图时）
[confidence]   置信度: 高/中/低
```

## 依赖
- vision-tool.py: ~/Documents/OpenClaw/workspace/scripts/vision-tool.py
- API: NUWA Flux gemini-3.1-pro-preview

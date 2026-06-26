# fashion-video-creator

穿搭视频创作 — 从零生成带货视频的完整素材

## 概述

一站式生成穿搭带货视频所需的全部素材：
- **虚拟模特图**：通过 Seedream 4.5/5.0 文生图生成 720x1280 的全身模特照
- **Seedance 2.0 视频提示词**：包含对话脚本、手势动作、场景描述、镜头风格
- **操作手册(SOP)**：即梦平台的逐步操作指引，从上传素材到生成视频

支持单条和批量模式。批量模式下每条视频可独立配置服装类型、场景、风格等参数。

## 核心能力

| 能力 | 说明 |
|------|------|
| 9 种模特预设 | 亚洲/欧美/黑人/拉丁裔，纤细/丰满/健美等体型 |
| 精细体型参数 | 身材/胸围/肩宽/腰/臀/腿/肤色/发型，每项独立调节 |
| 17 级写实度 | 0(皮克斯卡通) → 40(半写实推荐) → 100(RAW照片) |
| 7 种服装话术 | 裙装/上衣/裤装/外套/西装/休闲/通用，每种有专属对话和手势 |
| 11 个场景预设 | 公寓/卧室/街拍/商场/停车场/咖啡馆/摄影棚等 |
| 多段自动接链 | 视频 >15 秒时自动拆分为多段 Seedance 延长接龙 |
| 双语支持 | 中文/英文对话脚本 |

## 快速开始

### 安装

```bash
# Claude Code 用户
claude install-skill https://github.com/dingtom336-gif/outfit-video/tree/main/skills/fashion-video-creator
```

### 前置条件

- 火山方舟账号 + API Key
- Seedream 5.0 端点（推荐）或 4.5 模型ID

### 使用

对 Claude 说：
- "帮我做一个穿搭视频，裙子类型"
- "批量生成 5 条带货视频的 Prompt"
- "生成一个男性模特的西装展示视频"

## 文件结构

```
fashion-video-creator/
├── README.md                           # 本文件
├── SKILL.md                            # 核心技能逻辑
└── references/
    ├── model-presets.md                # 模特预设 + 体型参数 + 写实度锚点
    ├── seedream-api.md                 # Seedream API 调用规范
    ├── prompt-assembly.md              # Prompt 组装规则 + 多段接链 + SOP 模板
    └── dialogue-library.md             # 完整对话库：7 类型 x 2 性别 x 2 语言
```

## 兼容性

Claude Code, Claude.ai, 以及所有兼容 SKILL.md 的 Agent。

## 关联技能

- **[viral-video-replicator](/viral-video-replicator/)** — 已有参考视频？用它来逆向分析并生成复刻 Prompt

## 许可证

MIT

---

# fashion-video-creator

Fashion Video Creator — Generate complete e-commerce video assets from scratch

## Overview

One-stop generation of all assets needed for fashion e-commerce videos:
- **Virtual Model Image**: Generate 720x1280 full-body model photos via Seedream 4.5/5.0 text-to-image
- **Seedance 2.0 Video Prompt**: Complete with dialogue scripts, hand gestures, scene descriptions, and camera styles
- **Operator SOP**: Step-by-step guide for the Jimeng (即梦) platform, from uploading assets to generating video

Supports single and batch modes. In batch mode, each video task can be independently configured with different garment types, scenes, and styles.

## Core Capabilities

| Capability | Details |
|------------|---------|
| 9 Model Presets | Asian/European/Black/Latina, slim/curvy/athletic body types |
| Fine-grained Body Params | Build/bust/shoulders/waist/hips/legs/skin/hair, each independently adjustable |
| 17-level Realism | 0 (Pixar cartoon) → 40 (semi-realistic, recommended) → 100 (RAW photo) |
| 7 Garment Dialogue Scripts | Dress/top/pants/jacket/suit/casual/default, each with specialized dialogue and gestures |
| 11 Scene Presets | Apartment/bedroom/street/mall/parking/cafe/studio and more |
| Auto Multi-segment Chaining | Videos >15s auto-split into Seedance extend-chain segments |
| Bilingual | Chinese and English dialogue scripts |

## Quick Start

### Install

```bash
# Claude Code users
claude install-skill https://github.com/dingtom336-gif/outfit-video/tree/main/skills/fashion-video-creator
```

### Prerequisites

- Volcano Engine (火山方舟) account + API Key
- Seedream 5.0 endpoint (recommended) or 4.5 model ID

### Usage

Say to Claude:
- "Create a fashion video for a dress"
- "Batch generate 5 outfit video prompts"
- "Generate a male model suit showcase video"

## File Structure

```
fashion-video-creator/
├── README.md                           # This file
├── SKILL.md                            # Core skill logic
└── references/
    ├── model-presets.md                # Model presets + body params + realism anchors
    ├── seedream-api.md                 # Seedream API call specifications
    ├── prompt-assembly.md              # Prompt assembly rules + multi-segment chaining + SOP templates
    └── dialogue-library.md             # Complete dialogue library: 7 types x 2 genders x 2 languages
```

## Compatibility

Claude Code, Claude.ai, and all SKILL.md-compatible agents.

## Related Skills

- **[viral-video-replicator](/viral-video-replicator/)** — Have a reference video? Use this to reverse-engineer and replicate it

## License

MIT

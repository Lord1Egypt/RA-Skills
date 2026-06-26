---
name: ppt-production-suite
description: PPT制作完整技能套件。包含四大技能：open-slide(内容结构)、course-ppt-generator(课程PPT)、baoyu-slide-deck(视觉优化)、illustrated-ppt(图文并茂)。支持商用、教学、技术等多场景，图片与文字精准对齐。
version: 1.0.0
author: TJMtaotao
tags: [PPT, 演示文稿, 图文并茂, 课程课件, 商用演示, AI生成]
---

# PPT制作完整技能套件

## 包含技能

| 技能 | 用途 | 输入 |
|------|------|------|
| open-slide | 打磨内容结构和逻辑 | 主题描述 |
| course-ppt-generator | 生成.pptx课程课件 | 内容结构 |
| baoyu-slide-deck | 视觉增强优化 | .pptx文件 |
| illustrated-ppt | 图文并茂AI配图 | 文字内容 |

## 三阶段流水线

```
open-slide → course-ppt-generator → baoyu-slide-deck/illustrated-ppt
   内容结构          课程PPT              视觉增强
```

## 使用场景

| 场景 | 推荐技能组合 |
|------|--------------|
| 课程课件 | open-slide + course-ppt-generator |
| 商用演示 | course-ppt-generator + illustrated-ppt |
| 技术分享 | open-slide + course-ppt-generator + baoyu-slide-deck |
| 图文并茂 | course-ppt-generator + illustrated-ppt |

## 场景类型

- **education**: 蓝色科技风，适合课程课件
- **business**: 专业商务风，适合商业演示
- **tech**: 技术简约风，适合技术分享
- **creative**: 创意活力风，适合产品介绍

## 安装

将skills目录解压到 `/root/.openclaw/workspace/skills/`
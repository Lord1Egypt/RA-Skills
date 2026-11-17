---
name: baoyu-seedream-ppt
description: 基于宝玉baoyu-infographic布局框架 + 豆包Seedream 5.0文生图，智能生成图片PPT。支持21种布局 × 21种风格自由组合，根据用户内容自动生成每页一张图片的完整PPT。
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills
---

# 宝玉布局 × Seedream 图片PPT生成器

结合 **宝玉baoyu-infographic** 的21种布局 × 22种风格设计框架，和 **豆包Seedream 5.0** 的高质量文生图能力，一键生成图片PPT。

## 特点

- ✅ **成熟布局系统**：21种布局（时间线、对比图、思维导图、漏斗图等）覆盖绝大多数信息结构
- ✅ **丰富风格库**：22种风格（手绘、黏土、黑板报、赛博朋克、像素风等）自由选择
- ✅ **高质量生图**：Seedream 5.0 支持 2560x1440 高分辨率，文字生成质量优秀
- ✅ **自动整合PPT**：生成完所有图片后自动打包成完整PPT，每页一张图片，直接使用
- ✅ **支持用户素材**：可根据用户提供的内容链接/素材智能分析结构

## 工作流程

### 优化后的交互式分步流程（推荐）

按照用户要求，现在采用**分步确认流程**，减少反复修改浪费API配额：

1. **第一步：分析内容** - 读取用户提供的文本内容，分析信息结构
2. **推荐方案** - 根据内容推荐 **3种布局×风格组合**，同时建议比例
3. **用户确认** - 用户选择方案、确认比例，回答是否需要确认每页提示词
4. **生成提示词** - 用户确认方案后，生成每页的完整提示词
5. **提示词确认** - 如果用户要求，展示所有提示词供确认调整
6. **批量生成图片** - 提示词确认后，使用Seedream 5.0逐页生成图片
7. **整合输出PPT** - 自动将所有图片整合为最终PPT

### 原有一键流程（仍支持）

1. **分析内容** - 读取用户提供的文本内容，分析信息结构
2. **生成结构化内容** - 按照布局模板整理内容
3. **生成prompt** - 组合布局+风格+内容得到最终prompt
4. **批量生成图片** - 使用Seedream 5.0逐页生成图片（多页PPT）
5. **整合输出PPT** - 自动将所有图片整合为16:9PPT输出

## 用法

### 交互式分步生成（推荐，减少浪费）

```bash
# 第一步：分析内容，推荐方案
python interactive.py content.md --step analyze [--aspect landscape]

# 用户确认方案后，第二步：生成提示词
python interactive.py content.md --step prompts --layout bento-grid --style craft-handmade --aspect landscape

# 用户确认提示词后，第三步：生成图片并整合PPT
python interactive.py --step generate --config output/project-name/config.json
```

在 OpenClaw 对话中使用：
> 用户：帮我用baoyu-seedream-ppt生成这个content.md的PPT
> 
> 助手：分析内容 → 推荐3个方案 → 请你确认
> 
> 你：选方案1，比例16:9，需要确认提示词
> 
> 助手：生成所有提示词 → 请你确认
> 
> 你：提示词没问题，开始生成
> 
> 助手：逐页生成 → 输出最终PPT

### 直接一键生成（需求明确时仍支持）

```
/baoyu-seedream-ppt path/to/content.md
/baoyu-seedream-ppt 然后粘贴内容
python baoyu_seedream_ppt.py content.md --layout binary-comparison --style chalkboard --aspect landscape
```

## 选项

| Option | Values |
|--------|--------|
| `--layout` | 21种布局，见宝玉baoyu-infographic文档 |
| `--style` | 21种风格，见宝玉baoyu-infographic文档 |
| `--aspect` | landscape (16:9 默认), portrait (9:16), square (1:1), 自定义 3:4 等 |

## 配置

需要配置火山方舟API Key：
- API Key: 放在 `~/.openclaw/config.json` 中 `volces.api_key`

## 依赖

- 基于 `baoyu-infographic` 布局系统
- 使用 `doubao-seedream-5-0-260128` 模型生成图片
- 使用 `python-pptx` 整合输出PPT

## 布局×风格对照表

完全继承 baoyu-infographic 的21×21组合：

### 布局 (21种)
- `linear-progression` - 时间线/流程
- `binary-comparison` - A vs B 对比
- `comparison-matrix` - 多因素对比表格
- `hierarchical-layers` - 层级/金字塔
- `tree-branching` - 分类/分支
- `hub-spoke` - 中心概念辐射
- `structural-breakdown` - 结构分解
- `bento-grid` - 多主题概览（默认）
- `iceberg` - 表面vs深层
- `bridge` - 问题-方案
- `funnel` - 转化/过滤
- `isometric-map` - 空间关系
- `dashboard` - 指标/KPI
- `periodic-table` - 分类集合
- `comic-strip` - 叙述/序列
- `story-mountain` - 情节结构
- `jigsaw` - 互联部分
- `venn-diagram` - 重叠概念
- `winding-roadmap` - 旅程/里程碑
- `circular-flow` - 循环流程
- `dense-modules` - 高密度信息模块

### 风格 (22种)
- `craft-handmade` - 手绘纸艺（默认）
- `claymation` - 3D黏土定格
- `kawaii` - 日系可爱马卡龙
- `storybook-watercolor` - 水彩童话
- `chalkboard` - 黑板黑板报
- `cyberpunk-neon` - 赛博朋克霓虹
- `bold-graphic` - 漫画粗线
- `aged-academia` - 复古科学 sepia
- `corporate-memphis` - 扁平化活力
- `technical-schematic` - 工程蓝图
- `origami` - 折纸几何
- `pixel-art` - 复古8位像素
- `ui-wireframe` - 灰阶线框图
- `subway-map` - 地铁线路图
- `ikea-manual` - 宜家简约线稿
- `knolling` - 整齐平铺
- `lego-brick` - 乐高积木
- `pop-laboratory` - 实验室坐标网格
- `morandi-journal` - 莫兰迪手绘
- `retro-pop-grid` - 70年代复古网格
- `hand-drawn-edu` - 马卡龙手绘教育风
- `retro-popup-pop` - 复古拼贴弹窗风（v1.117 新增）

## 推荐组合

| 内容类型 | 推荐组合 |
|----------|----------|
| 对比测评 | `binary-comparison` + `chalkboard` |
| 产品介绍 | `bento-grid` + `chalkboard` |
| 时间线 | `linear-progression` + `craft-handmade` |
| 教程步骤 | `linear-progression` + `hand-drawn-edu` |
| 分类汇总 | `periodic-table` + `bold-graphic` |
| 高密度信息 | `dense-modules` + `morandi-journal` |

## 输出

```
output/{project-name}/
├── *.md (分析和结构化内容)
├── images/ (生成的PNG图片)
└── {project-name}.pptx (最终PPT)
```

## 授权

遵循原宝玉技能MIT协议，开源共享。

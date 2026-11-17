---
name: video-editing
description: 视频编辑：剪辑流程、转场设计、色彩分级、字幕制作、多格式导出
source:
  type: derived
  repo: skills-repo/content-creator
  path: skills/video-editing/SKILL.md
  url: https://skills.sh/affaan-m/everything-claude-code/video-editing
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 内容创作
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - video
  - editing
  - content-creation
  - post-production
---

# Video Editing — 视频编辑

> 好视频不是拍出来的，是剪出来的。本技能帮你从毛坯素材到成片输出，覆盖剪辑全流程——不需要 Premiere Pro 经验，只要你有故事要讲。

## 能力

- **剪辑流程**：粗剪 → 精剪 → 调色 → 音效 → 导出，每步的标准和检查点
- **转场与节奏**：Cut / Dissolve / Wipe 的选择逻辑，节奏控制（B-roll 比例、J-cut/L-cut）
- **字幕制作**：SRT 格式、时间轴对齐、多语言字幕、烧录字幕样式
- **调色基础**：色温/曝光/对比度/饱和度调整，LUT 应用，风格一致性
- **多格式导出**：平台适配（YouTube 16:9、TikTok 9:16、IG 1:1），编码和比特率

## 使用方式

在 Claude Code 中使用 `/video-editing` 调用。

```
/video-editing 帮我规划这条产品演示视频的剪辑结构
/video-editing 我的视频节奏太拖沓了，怎么优化？
/video-editing 这条视频要适配 TikTok 和 YouTube，导出什么格式？
```

## 工作流

1. **素材整理** — 按场景/镜头/日期分类，标记亮点和废弃镜头
2. **粗剪** — 按脚本或大纲排列镜头顺序，去掉明显废片
3. **精剪** — 节奏调整、转场优化、B-roll 插入、字幕同步
4. **调色混音** — 基础调色 + 音效/背景音乐平衡
5. **导出发布** — 平台适配导出，检查画质和音质

## 视频节奏参考

```
YouTube 教程：    保持 0.8-1.2x 语速，B-roll 占 30-40%
TikTok/Reels：    前 0.5 秒 Hook，每 2-3 秒切换画面
产品演示：        关键操作放慢，过渡部分加速
播客/采访：       以内容为主，剪辑以去掉废话和停顿为原则
```

## 适用场景

- 独立创作者制作 YouTube/TikTok 视频
- 创业者制作产品演示视频
- 技术内容创作者制作教程视频
- 播客转视频的后期制作

## 限制

- 聚焦视频剪辑概念和流程，不涉及具体软件操作（DaVinci Resolve/Premiere Pro/FCP）
- 不涉及 3D 动画和 VFX 特效制作
- 不涉及拍摄（灯光/相机/收音）
- 不涉及直播推流技术

## 相关参考（Playbook）

- 选题与平台定调（策略层）→ [references/content-strategy.md](../../references/content-strategy.md)
- 制作工作流与发布前检查清单（流程层）→ [references/production-workflow.md](../../references/production-workflow.md)
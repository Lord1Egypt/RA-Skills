---
name: video-generation
description: AI 视频生成，覆盖文生视频、图生视频、视频生视频的路线选型与工具对接，产出可交付短片
source:
  type: derived
  repo: prime-skills/runcomfy-agent-skills
  path: ai-video-generation/SKILL.md
  version: 1.0.0
  updated: 2026-05-15
  url: https://skills.sh/prime-skills/runcomfy-agent-skills/ai-video-generation
metadata:
  category: 视频生成
  platform: 通用
  difficulty: 进阶
tags:
  - video-generation
  - text2video
  - image2video
  - veo
  - comfyui
---

# Video Generation — AI 视频生成

> 把 AI 变成短片生产线：文生视频、图生视频、视频生视频，选对工具、控住参数，产出可交付的短视频素材。基于 runcomfy-agent-skills 的 ai-video-generation（352.3K 安装）改编，补充多工具对比（Veo / MiniMax / LTX）与片段化纪律。

## 能力

- **路线选型**：文生视频 / 图生视频 / 视频生视频 / 数字人口播 按素材与需求选
- **工具对接**：本地 ComfyUI 视频节点、RunComfy 云端、Veo 3.1、MiniMax H3、LTX-2
- **参数控制**：frames / fps / CFG / motion scale / denoise 的换算与调整
- **片段化生产**：3-8 秒片段多段拼接，规避长视频一致性问题
- **质检与重生成**：首/中/尾帧抽检、坏片段重生成不硬救

## 使用方式

在 Claude Code 中使用 `/video-generation` 调用。

```
/video-generation 把这个产品图做成 5 秒的展示视频，带运镜
/video-generation 写一段产品宣传短视频方案：文生+图生+拼接
/video-generation 这段视频人物崩脸了，帮我分析原因并重生成
```

## 工作流

1. **选路线** — 按 [references/video-generation-playbook.md](../../references/video-generation-playbook.md) 决策树：纯文生 / 图生（更可控）/ 视频生
2. **选工具** — 成本敏感→本地 ComfyUI；速度→MiniMax；质量+预算→Veo；口播→HeyGen
3. **定参数** — 片段 3-8 秒；frames/fps 换算正确（时长=frames/fps）；分辨率匹配模型
4. **单片段验证** — 抽首/中/尾帧质检，崩坏立即重生成（修 prompt/seed）
5. **拼接交付** — 同参数片段 concat；转场/配乐/字幕后处理
6. **记录** — 每片段 seed 与参数入档，可复现

## 适用场景

- 独立开发者做产品演示短片、App 宣传素材
- 内容创作者批量产出短视频素材
- 电商产品动态展示（图生视频）
- 数字人口播（HeyGen 等专属工具）

## 限制

- 单段 3-8 秒为质量上限，长视频走拼接
- 生成不稳定是常态：必须抽帧质检，不能直接交付
- 依赖算力/API 额度；商业 API 按量计费需预算
- 不处理已生成视频的剪辑/转场细节（见 `video-editing`）
- 版权风险自负：不生成仿冒真人形象/受版权素材

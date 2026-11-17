# AI Media Generation — AI 媒体生成技能库

> 面向独立开发者和内容创作者的 AI 媒体生成技能集合。覆盖图像生成/编辑与视频生成/编辑，从模型选型、提示词工程到批量出图与视频后处理，帮你把 AI 变成媒体生产流水线。

## 架构说明（superpower）

本仓库采用 skills-repo 的 **superpower 架构**（五层）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（ComfyUI 工作流、图像生成、视频生成），按需加载
- `skills/` — L3 细粒度子技能（图像生成 / 图像编辑 / 视频生成 / 视频编辑），可单独安装
- `scripts/` — L4 确定性脚本（工作流 JSON 校验、批量媒体处理）
- `assets/` — L5 可复用模板（ComfyUI 工作流样例、prompt 模板库）

## 技能清单

| 技能 | 描述 | 来源 |
|------|------|------|
| [image-generation](skills/image-generation/SKILL.md) | AI 文生图与图生图：模型选型、提示词工程、参数调优、批量出图 | [skills.sh](https://skills.sh/prime-skills/runcomfy-agent-skills/ai-image-generation) |
| [image-editing](skills/image-editing/SKILL.md) | AI 图像编辑与修图：局部重绘、扩图、抠图换背景、老照片修复 | [skills.sh](https://skills.sh/prime-skills/runcomfy-agent-skills/image-edit) |
| [video-generation](skills/video-generation/SKILL.md) | AI 视频生成：文生/图生/视频生视频，工具对接与片段化生产 | [skills.sh](https://skills.sh/prime-skills/runcomfy-agent-skills/ai-video-generation) |
| [video-editing](skills/video-editing/SKILL.md) | AI 视频编辑与后期：剪辑拼接、转场、字幕、配乐、格式转码 | [skills.sh](https://skills.sh/prime-skills/runcomfy-agent-skills/video-edit) |

## 工作流

```
模型选型/路线决策 ──→ 生成（图像 or 视频）──→ 批量处理 ──→ 后处理/交付
 (references/playbook)   (skills/*)          (scripts/)   (video-editing/ffmpeg)
```

## 安装

```bash
# 整库安装（推荐）—— 拿到路由层 + 全部 references/scripts/assets
npx skills add skills-repo/ai-media-generation -g -y

# 单技能安装 —— 只要某一个细粒度能力，例如只要视频生成
npx skills add skills-repo/ai-media-generation@video-generation -g -y
```

## 内置脚本与模板

```bash
# 校验 ComfyUI 工作流 JSON（期望 0 error）
python3 scripts/workflow_validator.py assets/workflows/text2image-basic.json --strict

# 批量图片缩放 + 转 WebP（先 --dry-run 预览）
python3 scripts/media_batch.py --in ./output --out ./deliver --max-dim 1024 --format webp --dry-run
```

详见 `SKILL.md` 的「内置脚本」与「模板资源」两节。

## 与本组织其他仓库的关系

- **animation-engineer** — Web/移动端 UI 动效实现；本仓库聚焦 AI 生成图像/视频
- **indie-game-developer** — 游戏开发与游戏美术管线；本仓库提供 AI 素材生成能力
- **design-studio** — UI/UX 设计；本仓库聚焦 AI 媒体生成而非界面设计
- **content-creator** — 内容创作与文案；本仓库提供配套的配图/视频生成

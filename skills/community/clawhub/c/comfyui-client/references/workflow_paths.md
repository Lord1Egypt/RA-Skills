# ComfyUI 工作流路径参考

本文档列出技能内及项目内可用的 ComfyUI 工作流文件路径，供技能调用时参考。

## 技能内工作流（assets/workflows，推荐）

本技能在 `assets/workflows/` 目录下捆绑了常用工作流，优先使用：

| 工作流类型 | 路径 | 说明 |
|-----------|------|------|
| Z-Image 文生图 | `.claude/skills/comfyui-client/assets/workflows/image_z_image.json` | Z-Image 高质量文生图，25 步出图（推荐 30-50 步） |
| Z-Image Turbo + ControlNet | `.claude/skills/comfyui-client/assets/workflows/image_z_image_turbo_fun_union_controlnet.json` | 文生图 + Fun Union ControlNet 控制 |
| Qwen 图片编辑 | `.claude/skills/comfyui-client/assets/workflows/image_qwen_image_edit_2511.json` | Qwen-Image-Edit 2511 图片编辑 |
| Wan 2.2 图生视频 | `.claude/skills/comfyui-client/assets/workflows/video_wan2_2_14B_i2v.json` | Wan 2.2 14B 单图生成视频 |
| Wan 2.2 首尾帧视频 | `.claude/skills/comfyui-client/assets/workflows/video_wan2_2_14B_flf2v.json` | Wan 2.2 14B 首尾帧生成视频 |

## 其他工作流（项目内）

| 工作流类型 | 路径 | 说明 |
|-----------|------|------|
| 文生图 (txt2img) | `scripts/githubToXPost/workflows/txt2img.json` | githubToXPost 基础文生图 |
| 图片编辑 | `scripts/githubToXPost/workflows/img_edit.json` | 图片编辑工作流 |
| ControlNet 图生图 | `scripts/githubToXPost/workflows/controlnet.json` | 使用 ControlNet 的图生图 |
| 图生视频 | `scripts/githubToXPost/workflows/img2video.json` | 单图生成视频 |
| 首尾帧视频 | `scripts/githubToXPost/workflows/flf2video.json` | 首尾帧生成视频 |
| Z-Image | `local-model-server/workflows/image_z_image_turbo.json` | local-model-server 版本（待更新） |
| 常用工作流（源） | `scripts/comfyui_workflows/` | 与技能 assets 同源，可作备份参考 |

## 路径使用说明

- 所有路径相对于**项目根目录**
- 技能内脚本会自动将相对路径解析为绝对路径
- 工作流文件需包含 ComfyUI 完整格式（nodes、links）或 API 格式

## 模型依赖

各工作流可能依赖不同的模型文件，需预先下载到 ComfyUI 的 `models/` 目录。工作流内的 MarkdownNote 节点通常包含模型下载链接说明。

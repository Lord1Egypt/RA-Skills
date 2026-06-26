---
name: ffmpeg-master-pro
description: FFmpeg Master Pro - 全能视频处理技能。当用户需要视频处理时使用，支持视频转换、视频压缩、视频编辑等。当用户要求视频处理, 视频转换, 视频压缩, FFmpeg, 视频编辑, 视频转码, 视频剪辑, 字幕处理, 视频优化, 批量视频处理, GIF转换, 视频翻转, 速度调节, 音频提取, 视频合并, 宽高比, 水印, 截图, 抽帧时使用此技能。
---

## 环境要求

- **必装**：`ffmpeg` 和 `ffprobe`（建议从 [ffmpeg.org](https://ffmpeg.org) 或 via winget/choco 安装）
- **可选**：`nvidia-smi`（NVIDIA 加速）、`vainfo`（Intel QSV）、`amdgpu-info`（AMD 加速）

首次使用前验证：`ffmpeg -version` 和 `ffprobe -version`。

## 执行建议

### 执行方式

FFmpeg 处理推荐使用 `exec background:true` 避免长时间阻塞会话。示例：

```bash
exec background:true command:"ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4"
```

### 完成后通知（可选）

任务完成后推荐使用 `message` 工具通知用户：

```
✅ 视频处理完成
文件：output.mp4 | 操作：转码压缩
```

> 注意：仅发送文件名即可，避免暴露完整路径。

### 文件路径处理

- 输入/输出路径直接使用用户提供的位置，不做跨分区复制
- Windows 路径（如 `C:\Users\...`）和 Unix 路径（如 `/mnt/c/...`）均支持
- 临时文件处理：如有需要可使用系统临时目录，任务结束后清理

## 核心工作流

所有工作流的完整命令、参数说明和代码示例见 [详细工作流](references/detailed_workflows.md)。

### 转码与优化

| # | 工作流 | 触发词 | 详细文档 |
|---|--------|--------|----------|
| 1 | 智能转码与压缩 | 压缩、转码、格式转换、减小文件 | [→](references/detailed_workflows.md#工作流1智能转码与压缩) |
| 2 | 智能参数优化 | 自动识别6种视频类型并优化编码 | [→](references/detailed_workflows.md#工作流2智能参数优化) |
| 3 | 预设模板系统 | YouTube/B站/微信/抖音等平台预设 | [→](references/detailed_workflows.md#工作流3预设模板系统) |
| 4 | 精确文件大小控制 | 指定目标大小，两遍编码偏差<5% | [→](references/detailed_workflows.md#工作流4精确文件大小控制) |

### 剪辑与分析

| # | 工作流 | 触发词 | 详细文档 |
|---|--------|--------|----------|
| 5 | Smart Cut 混合剪辑 | 剪辑、裁剪、cut | [→](references/smart_cut_guide.md) |
| 6 | 关键帧分析 | 关键帧、最佳剪辑点 | [→](references/keyframe_analysis.md) |

### 编辑与特效

| # | 工作流 | 触发词 | 详细文档 |
|---|--------|--------|----------|
| 7 | 字幕处理 | 提取/嵌入/烧录字幕 | [→](references/detailed_workflows.md#工作流7字幕处理) |
| 8 | 滤镜与特效 | 水印、旋转、翻转 | [→](references/detailed_workflows.md#工作流8滤镜与特效) |
| 9 | GIF 转换 | GIF、动图 | [→](references/detailed_workflows.md#工作流9gif转换) |
| 10 | 翻转与镜像 | 镜像、左右/上下翻转 | [→](references/detailed_workflows.md#工作流10翻转与镜像) |

### 变换与合并

| # | 工作流 | 触发词 | 详细文档 |
|---|--------|--------|----------|
| 11 | 速度调节 | 加速、慢动作、倍速 | [→](references/detailed_workflows.md#工作流11速度调节) |
| 12 | 音频提取与移除 | 提取音频、去音频、静音 | [→](references/detailed_workflows.md#工作流12音频提取与移除) |
| 13 | 视频合并 | 合并、拼接、concat | [→](references/detailed_workflows.md#工作流13视频合并) |
| 14 | 宽高比调整 | 16:9、9:16、竖屏、横屏 | [→](references/detailed_workflows.md#工作流14宽高比调整) |

## 智能决策系统

技能会自动执行以下决策，无需手动干预：

- **内容类型识别**：自动检测电影/动漫/屏幕录制/体育/音乐视频/老旧视频，选择最优编码参数。详见 [优化指南](references/optimization_guide.md)
- **GPU 加速**：自动检测 NVIDIA NVENC / AMD AMF / Intel QSV 并优先使用
- **质量验证**：自动校验输出文件的分辨率、时长、码率，可选 VMAF/SSIM/PSNR 评估

## 预设模板

内置 8+ 平台预设（`assets/presets/`）：youtube、bilibili、wechat、douyin、social\_media、archival、preview、web\_optimized。使用时提及平台名称即可自动匹配。

## 参考文档

- **详细工作流**：[detailed_workflows.md](references/detailed_workflows.md) — 所有14个工作流的完整命令和代码
- **Smart Cut 指南**：[smart_cut_guide.md](references/smart_cut_guide.md)
- **关键帧分析**：[keyframe_analysis.md](references/keyframe_analysis.md)
- **优化算法**：[optimization_guide.md](references/optimization_guide.md)
- **最佳实践**：[best_practices.md](references/best_practices.md)
- **API 参考**：[api_reference.md](references/api_reference.md)
- **快速入门**：[quickstart.md](references/quickstart.md)
- **故障排除**：[troubleshooting.md](references/troubleshooting.md)

## 工作流程

1. 分析用户需求，匹配触发词到对应工作流
2. 用 `ffprobe` 分析输入视频（格式、编码、分辨率、码率、时长）
3. 如有脚本可用（`scripts/`），优先执行脚本；否则按详细工作流文档构建 ffmpeg 命令
4. 执行转换，验证输出质量
5. 批量任务参考 detailed_workflows.md 附录中的批量处理器

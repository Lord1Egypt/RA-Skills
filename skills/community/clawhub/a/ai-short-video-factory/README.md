# AI 短视频工厂｜HTML-to-Video Studio

基于 HyperFrames 的 AI 视频生成 Skill，将文字创意自动转化为 HTML + CSS + GSAP 动画视频，并渲染为 MP4。

## ✨ 核心能力

- 🎬 从文字描述一键生成完整视频（15s ~ 3min）
- 🎨 完全自定义：布局、配色、动画、字体均由 HTML/CSS 控制
- 🔄 AI 全流程自动化：初始化 → 编写 → 动画 → 渲染 → 交付
- 🎵 支持字幕同步、原片音频保留、按需 BGM 合成与音量调校
- ✅ 自检管线确保视觉完整性和技术正确性

## 适用场景

| 视频类型 | 典型时长 |
|----------|---------|
| 科技资讯 / 行业速报 | 30-60s |
| 产品发布 / 功能介绍 | 15-45s |
| 数据可视化 | 20-40s |
| 教程 / 代码讲解 | 30-120s |
| 社交媒体短视频 | 15-30s |
| 口播 + 字幕 | 任意 |
| 品牌宣传 / 活动预热 | 15-45s |

## 前置依赖

- **Node.js** 22+
- **FFmpeg** 5.0+
- **Chrome Headless Shell**（`npx hyperframes browser ensure` 自动下载）
- **HyperFrames CLI** 0.6.90+（`npx hyperframes@latest`）

## 快速开始

一句话触发视频生成：

> "帮我做一个 30 秒的科技资讯短视频，主题是 AI 编程工具的发展趋势"

AI 会自动完成：
1. 初始化项目
2. 编写 HTML 视频内容（场景规划 + 动画编排）
3. 渲染为 MP4
4. 按需处理音频
5. 执行自检管线 → 交付

## Overview (English)

AI Short Video Factory is a HyperFrames-based skill that transforms text ideas into MP4 videos via HTML + CSS + GSAP animations. Supports product launches, tech news, data visualization, code walkthroughs, talking-head captions, and more.

## Author

- **raelzhang** — WorkBuddy Skill

## License

MIT-0

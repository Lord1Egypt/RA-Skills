---
name: remotion
description: 用 React 代码程序化生成视频的框架，支持 CSS/Canvas/SVG/WebGL，可部署到 Lambda/Cloud Run 大规模渲染，适合创意视频生成、数据可视化视频和个性化视频批量生产
version: 0.1.0
metadata:
  openclaw_requires: ">=1.0.0"
  emoji: 🎥
  homepage: https://remotion.dev
---

# Remotion — 用 React 写视频

Remotion 让开发者用 React 组件和 TypeScript 代码程序化创建视频，把视频创作变成软件工程问题。整个 Web 技术栈都可以用于视频：CSS 动画、Canvas 绘图、SVG、WebGL 特效，乃至调用外部 API 生成个性化内容。从本地预览到云端大规模渲染（AWS Lambda / Google Cloud Run），一套代码覆盖全流程。

## 核心使用场景

- **程序化视频生成**：用数据驱动视频内容，批量生成个性化视频（如 GitHub Unwrapped 年报）
- **数据可视化视频**：将图表、指标、实时数据渲染成动态视频
- **营销/社交媒体视频**：用 React 组件快速生成品牌一致的视频素材
- **字幕与标注视频**：用 `@remotion/captions` 自动生成带字幕的视频
- **云端大规模渲染**：用 `@remotion/lambda` 在 AWS Lambda 上并行渲染，缩短渲染时间

## AI 辅助使用流程

1. **初始化项目** — AI 执行 `npx create-video@latest` 创建项目并安装依赖
2. **编写 React 组件** — AI 根据需求生成视频组件，配置 `<AbsoluteFill>`、`useCurrentFrame` 等核心 API
3. **本地预览调试** — AI 启动 `npx remotion studio` 在浏览器中实时预览视频
4. **配置视频元数据** — AI 设置分辨率、帧率、时长等参数
5. **本地渲染导出** — AI 运行 `npx remotion render` 输出 MP4/WebM/GIF
6. **云端部署渲染** — AI 配置 Lambda 或 Cloud Run 进行大规模批量渲染

## 关键章节导航

- [安装指南](guides/01-installation.md) — 项目初始化、模板选择、环境配置
- [快速开始](guides/02-quickstart.md) — React 组件编写、核心 API、本地渲染
- [高级用法](guides/03-advanced-usage.md) — Lambda 渲染、批量生成、字幕、动态数据
- [故障排查](troubleshooting.md) — 渲染错误、性能问题、云端部署问题

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 创建 Remotion 项目（`npx create-video@latest`）并选择合适模板
- ✅ 编写 React 视频组件，使用 `useCurrentFrame`、`interpolate`、`spring` 等动画 API
- ✅ 配置 `<Composition>` 的分辨率、帧率和时长
- ✅ 启动 Remotion Studio 进行本地预览（`npx remotion studio`）
- ✅ 执行本地渲染导出视频（`npx remotion render`）
- ✅ 配置 `@remotion/lambda` 在 AWS Lambda 上部署渲染服务
- ✅ 使用 `@remotion/captions` 生成带字幕的视频
- ✅ 实现数据驱动的个性化视频批量生成

## 核心功能

- ✅ **React 视频组件** — 用 JSX 和 CSS 编写视频帧，完整 Web 技术栈支持
- ✅ **动画 API** — `interpolate`、`spring`、`useCurrentFrame` 精确控制每一帧
- ✅ **Remotion Studio** — 浏览器内实时预览和时间轴编辑器
- ✅ **多格式输出** — MP4（H.264/H.265）、WebM、GIF、图片序列
- ✅ **Lambda 渲染** — AWS Lambda 并行渲染，大幅缩短长视频渲染时间
- ✅ **Cloud Run 渲染** — Google Cloud Run 渲染方案
- ✅ **字幕组件** — `@remotion/captions` 自动生成 SRT/VTT 格式字幕
- ✅ **动态数据** — 通过 props 注入外部数据，生成个性化内容
- ✅ **GIF 支持** — `@remotion/gif` 在视频中嵌入 GIF 动画
- ✅ **字体支持** — `@remotion/google-fonts` 使用 Google Fonts
- ✅ **Lottie 动画** — `@remotion/lottie` 嵌入 Lottie 动画文件
- ✅ **音频/视频合成** — `<Audio>` 和 `<Video>` 组件混合媒体

## 快速示例

```bash
# 创建新项目（选择模板）
npx create-video@latest

# 启动 Studio 预览
cd my-video
npx remotion studio

# 渲染视频
npx remotion render src/index.ts MyComposition out/video.mp4

# 渲染 GIF
npx remotion render src/index.ts MyComposition --output out/video.gif
```

```typescript
// 基础视频组件
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion'

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame()
  const opacity = interpolate(frame, [0, 30], [0, 1])
  
  return (
    <AbsoluteFill style={{ backgroundColor: 'white', opacity }}>
      <h1>Hello, Remotion!</h1>
    </AbsoluteFill>
  )
}
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Node.js | >= 18.0 |
| npm / pnpm / yarn | 任意版本 |
| FFmpeg | 可选（本地渲染使用内置版本） |

**许可证注意：** Remotion 对个人/学生免费，公司使用需要购买许可证。详见 [remotion.dev/license](https://remotion.dev/license)。

## 项目链接

- GitHub：https://github.com/remotion-dev/remotion
- 文档：https://remotion.dev/docs
- API 参考：https://remotion.dev/api
- 展示作品：https://remotion.dev/showcase
- Discord：https://remotion.dev/discord

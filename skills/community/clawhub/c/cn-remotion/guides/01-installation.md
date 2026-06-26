# 安装指南

## 适用场景

- 从零创建 Remotion 视频项目
- 选择合适的项目模板
- 在现有 React 项目中集成 Remotion

---

## 方式一：创建新项目（推荐）

> **AI 可自动执行**

```bash
npx create-video@latest
```

按提示选择：
1. **项目名称**：输入你的项目名
2. **模板**：选择起始模板（见下方模板列表）
3. **包管理器**：npm / yarn / pnpm

完成后进入项目：
```bash
cd my-video
npx remotion studio
```

浏览器自动打开 `http://localhost:3000`，Remotion Studio 就绪。

---

## 可用模板

| 模板名 | 说明 |
|--------|------|
| `Hello World` | 最简单的入门示例 |
| `Blank` | 空白项目 |
| `Tailwind` | 集成 Tailwind CSS |
| `Next.js` | 与 Next.js 集成 |
| `Astro` | 与 Astro 集成 |

---

## 方式二：在现有 React 项目中安装

```bash
# npm
npm install remotion @remotion/cli

# yarn
yarn add remotion @remotion/cli

# pnpm
pnpm add remotion @remotion/cli
```

创建入口文件 `src/index.ts`：
```typescript
import { registerRoot } from 'remotion'
import { RemotionRoot } from './Root'

registerRoot(RemotionRoot)
```

---

## 安装可选功能包

```bash
# Lambda 渲染（AWS）
npm install @remotion/lambda

# Google Cloud Run 渲染
npm install @remotion/cloudrun

# 字幕支持
npm install @remotion/captions

# Google Fonts
npm install @remotion/google-fonts

# GIF 支持
npm install @remotion/gif

# Lottie 动画
npm install @remotion/lottie

# 媒体解析工具
npm install @remotion/media-utils

# ElevenLabs 语音合成
npm install @remotion/elevenlabs
```

---

## 验证安装

```bash
# 检查版本
npx remotion --version

# 启动 Studio
npx remotion studio

# 渲染测试
npx remotion render src/index.ts HelloWorld out/test.mp4
```

期望结果：`out/test.mp4` 文件成功生成。

---

## 完成确认检查清单

- [ ] `npx create-video@latest` 创建项目成功
- [ ] `npm install` 依赖安装完成
- [ ] `npx remotion studio` 启动，浏览器打开预览界面
- [ ] 能在 Studio 中看到视频组件预览

---

## 下一步

- [快速开始](02-quickstart.md) — React 组件编写、核心动画 API、本地渲染

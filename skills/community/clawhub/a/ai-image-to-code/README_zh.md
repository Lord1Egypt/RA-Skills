# AI Image To Code

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将 UI 截图转换为 HTML/CSS 或 React 组件 — 以工作代码重建设计

## 解决什么问题

用户有设计模型或截图，需要将其转换为可以实际运行的代码——不是描述，不是 Figma 导出，而是看起来像原始设计的工作 HTML/CSS 或 React 组件。

**触发条件：** UI 截图/图片 + 代码/生成/重建意图。

## 功能特性

- **视觉驱动布局提取** — 分析截图的结构（头部、侧边栏、主内容）、配色、字体层次和间距
- **多格式输出** — 纯 HTML/CSS（默认）或 React + Tailwind CSS（用于组件请求）
- **移动端优先响应式** — 检测移动端截图并输出 `max-width: 375px` 容器
- **适配的占位符内容** — 使用上下文适当文本（"价格：￥49.99"而非通用占位符）

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install ai-image-to-code

# 或手动复制
cp -r ai-image-to-code ~/.openclaw/skills/
```

### 使用方法

```
/ai-image-to-code
```

粘贴截图，要求生成 HTML/CSS。

```
/ai-image-to-code/react
```

要求 React + Tailwind 输出，而不是纯 HTML。

```
/ai-image-to-code/describe
```

只想先获取布局的文本描述——不生成代码。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/ai-image-to-code` | 将 UI 图片转换为 HTML/CSS |
| `/ai-image-to-code/react` | 输出 React 函数组件 + Tailwind |
| `/ai-image-to-code/describe` | 布局的文本描述，无代码 |

## 示例

| 输入 | 输出 |
|------|------|
| 电商产品卡片 | "价格：￥49.99 — 加入购物车" 上下文适当 |
| 深色模式 UI 截图 | 应用深色背景、浅色文字、正确对比度 |
| 移动端 App 截图 | `max-width: 375px` 容器，移动端优先 |
| 复杂仪表盘 | 网格布局：侧边栏、头部、主面板 |

## 目录结构

```
ai-image-to-code/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 颜色提取、布局模式、Tailwind 映射
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。
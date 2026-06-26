---
title: Browser Canvas Poetry
description: 将诗歌、文学意象、视觉艺术概念转化为浏览器原生艺术作品
tags: [browser-art, creative-coding, generative-art, poetry, frontend]
author: Browser Canvas Poetry Collective
homepage: https://github.com/browser-canvas-poetry
version: 1.7.0
---

# Browser Canvas Poetry
## 浏览器画布诗意 - 将艺术想象编译为浏览器原生体验

### Skill Overview

**本Skill用于**: 将诗歌、文学意象、视觉艺术概念转化为浏览器原生艺术作品。

**核心能力**:
- 将抽象艺术概念翻译为前端代码提示词
- 提供丰富的生成式艺术风格参考
- 水墨与丹青双智能体协同创作
- 可导入的交互组件库（粒子、物理、生物、动画等）
- **BCPP Protocol v1.7.0** - 极简核心协议
  - 意图层：艺术概念定义
  - 描述层：视觉元素结构
  - **表演层** - 时间轴演绎（新增）
  - 渲染层：跨平台适配
  - 交互层：行为映射
- **画布考古学** - 作品历史记录与签名
- **艺术流派系统** - 流派定义与分类
- **去中心化Registry** - 开放渲染器/流派注册

**使用场景**:
- AI Coding IDE (Cursor/Codex/Trae) 生成创意前端项目
- 双智能体协同创作（视觉 x 交互）
- **BCPP协议解析与生成** - 结构化艺术描述
- 创意编程教学与灵感激发
- 生成式艺术作品快速原型
- 诗歌可视化与互动文学

**技术框架支持**:
- 单一HTML文件（快速原型）
- **Pretext框架**（多文件交互项目）- 支持文本测量、动态排版、粒子动画等复杂交互
- 原生Canvas/WebGL/CSS/SVG
- 任何前端框架集成

---

## Input Schema

用户可通过以下方式调用本Skill：

```
用户输入: 艺术概念描述 / 诗歌片段 / 情绪关键词 / 视觉风格偏好
```

### 支持的输入格式

```yaml
输入类型:
  - 诗歌文本: "落霞与孤鹜齐飞，秋水共长天一色"
  - 情绪关键词: "孤独的、流动的、碎片化的"
  - 视觉风格: "赛博朋克、和风极简、后现代解构"
  - 艺术流派: "表现主义、抽象表现主义、极简主义"
  - 技术偏好: "纯CSS动画、WebGL粒子、SVG路径动画"
```

---

## Output Schema

```yaml
输出格式:
  prompt: 生成给AI IDE的代码生成提示词
  style_reference: 相关艺术风格参考
  technical_hints: 技术实现提示
  bcpp_manifest: BCPP协议结构化描述
  suggestions: 互动建议与改进方向
```

---

## Execution Context

### 环境要求
- 无需特殊环境变量
- 需要访问互联网获取艺术参考资料（可选）
- 支持所有主流浏览器环境

### 外部依赖
- 无强制依赖
- 可选：Wikipedia API（获取艺术流派信息）
- 可选：诗歌数据库API（获取中文诗词意象）

---

## References | 参考资料

本Skill包含以下参考文档，位于 `references/` 目录：

### 协议文档

1. **bcpp-protocol.md** - BCPP协议规范（v1.7.0极简版：去掉验证层，增加表演层、画布考古学）
2. **bcpp-examples.md** - BCPP协议示例集（完整manifest.yaml示例）
3. **bcpp-registry.md** - BCPP Registry（去中心化渲染器/流派/作品注册系统）
4. **bcpp-improvements.md** - BCPP问题分析与改进方案

### 智能体与协作

5. **ai-partner.md** - AI伙伴人格与情绪系统（水墨/丹青人格）
6. **multi-agent.md** - 水墨与丹青双智能体协同创作系统
7. **interactive-api-components.md** - 可导入的交互组件库（粒子、物理、生物、动画等）

### 艺术与风格

8. **literary-imagery.md** - 中西文学意象对照表
9. **art-movements.md** - 现代艺术流派与浏览器艺术对应关系
10. **browser-capabilities.md** - 浏览器独特能力与艺术可能性
11. **nebula-rendering.md** - 星云渲染专项技术指南（Three.js Shader/WebGL Raymarching）
12. **frontend-rendering-libraries.md** - 前端渲染开源库完整分类指南
13. **interactive-creatures.md** - 互动生物行为系统指南

### 选读参考

14. **technical-poetry.md** - 代码即诗歌：程序员的文学修养
15. **case-studies.md** - 浏览器原生艺术案例分析
16. **performance-tips.md** - 性能优化与艺术效果的平衡
17. **accessibility.md** - 无障碍艺术：让每个人都能体验
18. **curation-guide.md** - 如何策展浏览器原生艺术展

---

## Contribution | 贡献指南

欢迎为本Skill贡献：

1. Fork本仓库
2. 添加新的艺术风格或参考文档
3. 在BCPP Registry注册新的渲染器或流派
4. 提交Pull Request

---

## License | 许可

本Skill遵循 MIT License，可自由使用、修改和分发。

---

## Author | 作者

**Browser Canvas Poetry Collective**
- 浏览器原生艺术爱好者社区
- 欢迎交流：creative-coding@art-web.dev

---

**"代码是诗，浏览器是画布，你的手指是最后的笔触。"**
**"Code is poetry, the browser is canvas, your fingers are the final brushstroke."**

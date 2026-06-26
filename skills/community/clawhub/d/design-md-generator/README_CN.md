# 🎨 Design MD Generator — 一键偷师任意网站的设计语言

> **[English](README.md)**

**输入一个 URL，输出完整的 DESIGN.md。** 自动提取任意网站的视觉 DNA，生成结构化的 Markdown 设计系统文档，让 AI coding agent 读了就能做出像素级匹配的 UI。

## 什么是 DESIGN.md？

[DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) 是 Google Stitch 提出的新概念 — 一个纯文本的设计系统文档，AI agent 读了就知道 UI 该长什么样。

类比：
- `AGENTS.md` → 告诉 agent **怎么构建**项目
- `DESIGN.md` → 告诉 agent 项目**该长什么样**

这个 Skill 把手动创建 DESIGN.md 的过程完全自动化了。

## 工作原理

```
网站 URL → 截图 + CSS 提取 → 结构化 DESIGN.md
```

1. **截图** — 用浏览器加载目标网站，截图 + DOM 快照
2. **提取** — 自动采集所有设计 token：颜色、字体、间距、阴影、边框、组件样式
3. **生成** — 输出包含 9 个标准 Section 的完整 DESIGN.md

## 输出格式

遵循 [Google Stitch DESIGN.md 格式规范](https://stitch.withgoogle.com/docs/design-md/format/)：

| # | Section | 提取内容 |
|---|---------|---------|
| 1 | 视觉主题与氛围 | 设计哲学、风格基调、视觉密度 |
| 2 | 色彩体系 | 语义化颜色命名 + hex + 使用场景 |
| 3 | 排版规则 | 字体族、完整的文字层级表 |
| 4 | 组件样式 | 按钮、卡片、输入框（含交互状态） |
| 5 | 布局原则 | 间距系统、网格、留白哲学 |
| 6 | 深度与层级 | 阴影系统、表面层级 |
| 7 | 设计准则 | 该做什么、不该做什么 |
| 8 | 响应式行为 | 断点、触摸目标、折叠策略 |
| 9 | Agent 提示指南 | 快速颜色参考 + 可直接用的 prompt |

## 使用方法

### OpenClaw 安装

```bash
clawhub install design-md-gen
```

然后告诉你的 agent：
> "帮我从 https://linear.app 生成一份 DESIGN.md"

### 用法

把生成的 `DESIGN.md` 放到项目根目录，然后告诉 AI coding agent：
> "按照 DESIGN.md 的设计规范，帮我做一个落地页"

Agent 读完设计系统文档后，生成的 UI 就能匹配目标网站的视觉风格。

## 案例

已成功为以下网站生成 DESIGN.md：
- **Linear** — 极简暗色模式，靛蓝紫色调
- **Vercel** — 黑白精确美学，Geist 字体系统
- **Supabase** — 暗色翡翠主题，代码优先
- **Stripe** — 标志性紫色渐变，轻盈优雅

## Skill 结构

```
design-md-generator/
├── SKILL.md                          # 工作流指南
├── scripts/
│   └── extract-tokens.js             # CSS token 提取脚本
└── references/
    ├── format-spec.md                # 9 Section 格式规范
    └── example-linear.md             # 高质量参考范例
```

## 灵感来源

- [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) — 原始概念
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 55 个手工整理的 DESIGN.md 合集

## License

MIT

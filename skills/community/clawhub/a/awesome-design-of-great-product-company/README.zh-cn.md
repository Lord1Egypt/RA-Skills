# Awesome DESIGN SKILL

[EN](README.md) | 简体中文

> 精心整理的 58 个世界级产品设计系统风格 — 可直接放入项目，供任何 AI 编码 agent 使用。


[演示页](https://www.jackyshen.com/awesome-design-of-great-product-company-skill/)

---

## 快速开始

### 安装

```bash
npx skills add https://github.com/mebusw/awesome-design-of-great-product-company-skill
```

### 查询品牌设计

```
/awesome-design-of-great-product-company
查一下 Spotify 的设计
帮我用 Vercel 风格做个登录页
给我看看 Apple 的颜色和字体
```

### 在项目中使用

1. 将某个品牌的 `DESIGN.md` 复制到项目根目录
2. 告诉你的 AI agent：*"按照本目录中的 DESIGN.md，帮我构建一个风格一致的页面"*
3. 获得像素级匹配品牌设计语言的 UI

---

## 每个品牌包含的文件

```
design-md/<品牌>/
├── DESIGN.md         ← 设计系统文档（供 AI agent 阅读）
├── README.md         ← 品牌简介
├── preview.html      ← 视觉目录（亮色模式）
└── preview-dark.html ← 视觉目录（暗色模式）
```

### DESIGN.md 包含的内容

| 章节 | 涵盖内容 |
|------|---------|
| 视觉主题与氛围 | 调性、密度、设计哲学 |
| 色彩系统与角色 | 语义化命名 + hex 值 + 功能角色 |
| 字体规范 | 字体家族、完整层级表 |
| 组件样式 | 按钮、卡片、输入框、导航及各种状态 |
| 布局原则 | 间距体系、网格、留白哲学 |
| 深度与层级 | 阴影系统、表面层级 |
| Do's and Don'ts | 设计准则与反模式 |
| 响应式行为 | 断点、触控目标、折叠策略 |

---

## 全部品牌（58 个）

### AI & 机器学习
`claude` · `cohere` · `elevenlabs` · `minimax` · `mistral.ai` · `ollama` · `opencode.ai` · `replicate` · `runwayml` · `together.ai` · `voltagent` · `x.ai`

### 开发者工具
`cursor` · `expo` · `linear.app` · `lovable` · `mintlify` · `posthog` · `raycast` · `resend` · `sentry` · `supabase` · `superhuman` · `vercel` · `warp` · `zapier`

### 基础设施 & 云
`clickhouse` · `composio` · `hashicorp` · `mongodb` · `sanity` · `stripe`

### 设计 & 生产力
`airtable` · `cal` · `clay` · `figma` · `framer` · `intercom` · `miro` · `notion` · `pinterest` · `webflow`

### 金融科技 & 加密
`coinbase` · `kraken` · `revolut` · `wise`

### 企业 & 消费品
`airbnb` · `apple` · `ibm` · `nvidia` · `spacex` · `spotify` · `uber`

### 汽车品牌
`bmw` · `ferrari` · `lamborghini` · `renault` · `tesla`

### 咨询服务
`scrum-alliance` · `uperform`

---

## 与 AI Agent 配合使用

### 示例一：生成 Spotify 风格的落地页

```
将 design-md/spotify/DESIGN.md 复制到项目，然后提示：
"Build me a landing page for a music streaming app using this DESIGN.md"
```

### 示例二：用 Vercel 美学构建开发者工具仪表盘

```
将 design-md/vercel/DESIGN.md 复制到项目，然后提示：
"Build me a dashboard for a deployment tool using this DESIGN.md"
```

### 示例三：匹配 Apple 的字体层级与间距

```
将 design-md/apple/DESIGN.md 复制到项目，然后提示：
"Build me a product page with Apple's typography scale and section rhythm"
```

---

## 设计哲学对比

| 品牌 | 整体调性 | 主色调 | 字体 |
|------|---------|--------|------|
| Apple | 克制的戏剧感 | `#0071e3` | SF Pro Display |
| Spotify | 鲜明活力 | `#1DB954` | Circular |
| Vercel | 精准极简 | `#000000` | Inter |
| Linear | 聚焦张力 | `#5E6AD2` | Inter |
| Stripe | 开发者信任感 | `#635BFF` | Inter |
| Notion | 温暖清晰 | `#000000` | SF Pro Text |

---

## License

MIT — 可自由用于个人和商业项目。

致谢： [DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) 是 Google Stitch 推出的纯文本设计系统格式。本仓库提供从真实产品中提取的**可直接使用的 DESIGN.md 文件** — 包括 Spotify 的鲜明绿色、Vercel 的精准黑白美学、Apple 的克制戏剧感等。

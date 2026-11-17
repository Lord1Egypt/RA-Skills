# Awesome DESIGN SKILL

EN | [简体中文](README.zh-cn.md)
  
> Curated design system documents extracted from 58 world-class products — ready to drop into your project and feed to any AI coding agent.

[Demos](https://www.jackyshen.com/awesome-design-of-great-product-company-skill/)


---

## Quick Start

### Installation

```bash
npx skills add https://github.com/mebusw/awesome-design-of-great-product-company-skill
```

### Query a brand design

```
/awesome-design-of-great-product-company
Look up Spotify's design system
Build me a login page in Vercel's style
Show me Apple's colors and typography
```

### Use in your project

1. Copy a brand's `DESIGN.md` into your project root
2. Tell your AI agent: *"Build me a page that looks like this, following the DESIGN.md in this directory"*
3. Get pixel-perfect UI that matches the brand's design language

---

## What's Inside Each Brand

```
design-md/<brand>/
├── DESIGN.md         ← Design system document (for AI agents)
├── README.md         ← Brand overview
├── preview.html      ← Visual catalog (light mode)
└── preview-dark.html ← Visual catalog (dark mode)
```

### What DESIGN.md Captures

| Section | What it defines |
|---------|----------------|
| Visual Theme & Atmosphere | Mood, density, design philosophy |
| Color Palette & Roles | Semantic name + hex + functional role |
| Typography Rules | Font families, full hierarchy table |
| Component Stylings | Buttons, cards, inputs, navigation with states |
| Layout Principles | Spacing scale, grid, whitespace philosophy |
| Depth & Elevation | Shadow system, surface hierarchy |
| Do's and Don'ts | Design guardrails and anti-patterns |
| Responsive Behavior | Breakpoints, touch targets, collapsing strategy |

---

## Available Brands (58)

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

## Usage with AI Agents

### Example 1: Generate a Spotify-style landing page

```
Copy design-md/spotify/DESIGN.md into your project, then prompt:
"Build me a landing page for a music streaming app using this DESIGN.md"
```

### Example 2: Get Vercel's aesthetic for a developer tool

```
Copy design-md/vercel/DESIGN.md into your project, then prompt:
"Build me a dashboard for a deployment tool using this DESIGN.md"
```

### Example 3: Match Apple's typography and spacing

```
Copy design-md/apple/DESIGN.md into your project, then prompt:
"Build me a product page with Apple's typography scale and section rhythm"
```

---

## Design Philosophy Examples

| Brand | Primary Vibe | Accent Color | Typography |
|-------|-------------|--------------|------------|
| Apple | Controlled drama | `#0071e3` | SF Pro Display |
| Spotify | Vivid energy | `#1DB954` | Circular |
| Vercel | Precision minimal | `#000000` | Inter |
| Linear | Focused intensity | `#5E6AD2` | Inter |
| Stripe | Developer trust | `#635BFF` | Inter |
| Notion | Warm clarity | `#000000` | SF Pro Text |

---



## License

MIT — Use freely for personal and commercial projects.

Thanks to [DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) is a plain-text design system format introduced by Google Stitch. This repo provides **ready-to-use DESIGN.md files** extracted from real products — Spotify's vivid green, Vercel's precision black-and-white, Apple's controlled drama, and more.

---
name: design-spec-personal
description: >-
  生成并验证 UI 设计交付物：可交互 preview.html、annotated.html、tokens.css、spec.json 与
  assumptions.log。支持文字、截图、Sketch、Figma 输入，以及 mobile-h5/web-pc 平台；按需加载
  universal、内置或用户导入的 design profile，执行组件路由、场景模板、token 约束、静态 QA 和
  真实浏览器验收。支持 W3C/Style Dictionary Token 导入。用户要求设计稿、原型、UI、页面设计、视觉稿、交互稿、design、prototype、
  mockup、wireframe、hi-fi、设计还原、design token、annotated spec、d2c、Ant Design、antd、
  antd-mobile、Arco Design、Arco、中后台或移动端 H5 时使用。
metadata:
  release.version: "v0.6.1"
  release.phase: "icon-quality-gate"
  release.profile_schema: "2"
  tags: "design,ui,spec,d2c,prototype,token,figma,sketch,ant-design,arco-design,mobile-h5,web-pc"
---

# design

A unified design skill that produces hi-fi interactive prototypes and implementation-ready specs in a single run. Every output is simultaneously a visual artifact and a precise engineering specification.

## What it produces

From any input, always generates the design deliverables plus browser evidence:

| File | For whom | What it is |
|------|---------|-----------|
| `preview.html` | PM / Designer | Hi-fi interactive prototype |
| `annotated.html` | Engineer / AI coding tool | Spec-annotated HTML with `data-spec-*` attributes |
| `tokens.css` | Everyone | CSS custom properties — the single source of truth |
| `spec.json` | AI coding tool | Machine-readable full spec with states and assumptions |
| `assumptions.log` | AI coding tool | Every inferred/estimated value, marked with confidence |
| `preview.measure-report.json` | QA / AI coding tool | Browser-measured geometry, contrast, overflow, and P0/P1 findings |
| `preview.measured.png` | Reviewer | Screenshot captured from the same measured browser session |
| `acceptance.spec.mjs` | Engineer / CI | Executable P0/P1 and geometry regression contract |

## How to use this skill

**1. Detect your harness.** Read the matching reference doc once:
- Claude Code (`AskUserQuestion`, `SendUserFile`, Claude Preview MCP) → read [`references/claude.md`](references/claude.md)
- Cursor (`AskQuestion`, `cursor-ide-browser` MCP) → read [`references/cursor.md`](references/cursor.md)
- Codex Agent (`functions.*`, Codex Browser) → read [`references/codex.md`](references/codex.md)

**2. Load the core methodology.** Read [`system-prompt.md`](system-prompt.md) — the L1→L4 pipeline, quality rules, and output generation guidelines.

**3. Identify input type.** Read the matching handler:
- Text description → [`input-handlers/text.md`](input-handlers/text.md)
- Screenshot / image → [`input-handlers/screenshot.md`](input-handlers/screenshot.md)
- Sketch file (.sketch) → [`input-handlers/sketch.md`](input-handlers/sketch.md)
- Figma URL → [`input-handlers/figma.md`](input-handlers/figma.md)

**4. Load the design system.** Three-layer stack: universal → standard → brand. Load in order, later layers override earlier ones.

*Layer 1 — Universal (progressive load):*

Core:
- Copy [`tokens.css`](design-system/universal/tokens.css) and [`component-tokens.css`](design-system/universal/component-tokens.css) to the output without preloading their full contents; query only selected token definitions when needed.
- Read [`component-routing.md`](design-system/universal/references/component-routing.md) once as the fallback binding gate.

Load only when the current decision needs it:
- Universal component is selected → [`components.md`](design-system/universal/components.md)
- Token semantics are unresolved → [`usage-guidelines.md`](design-system/universal/usage-guidelines.md)
- Page skeleton is unresolved → [`layout-patterns.md`](design-system/universal/layout-patterns.md)
- A concrete interaction pattern is used → [`interaction-patterns.md`](design-system/universal/interaction-patterns.md)
- `apple-hig` only → [`macos-patterns.md`](design-system/universal/references/macos-patterns.md)
- Hardcoded platform/SVG/preview constants appear → [`token-exceptions.md`](design-system/universal/references/token-exceptions.md)
- Functional icons or simulated platform chrome appear → [`icon-policy.md`](design-system/universal/references/icon-policy.md)
- Relevant failure pattern only → [`anti-examples.md`](design-system/universal/references/anti-examples.md)
- Before visual delivery → [`critic-checklist.md`](design-system/universal/references/critic-checklist.md) and [`visual-critic.md`](design-system/universal/references/visual-critic.md)

*Layer 2 — Design Standard Profile (load when user specifies a standard, or when platform implies one):*
- 先读 [`design-system/profiles/registry.json`](design-system/profiles/registry.json)，把用户指定标准按忽略大小写、合并空白的规则匹配唯一 `profile_id` 或 alias；未知或冲突时阻断，不猜测。
- 命中后先读 `profile.json` 和 `<profile.entry>`，按 `tier`/`capabilities` 加载，不通过目录猜能力。禁止在根入口硬编码新增 profile 的文件清单。
- Tier 1：读 `semantic/token-map.json`、`semantic/unmapped-tokens.json` 与 `tokens.css`；组件和布局使用 universal，未映射语义必须阻断确认。
- Tier 2：在 Tier 1 基础上读取 `routing/component-routing.md` 和当前平台 registry；Profile 组件路由是权威来源。
- Tier 3：再读取 `<profile.guide>`、深组件规格、templates 和 runtime；Ant Design、Arco Design 属于 Tier 3。
- 请求的平台必须存在于 `profile.platforms`。只有 Profile 声明对应 capability 时，才要求 component registry、templates 或 runtime。
- Ant Design 旧路径 [`design-system/standards/ant-design`](design-system/standards/ant-design) 仅作兼容入口；新增规范只进入 `design-system/profiles/<profile_id>/`。

When the user supplies W3C Design Tokens or Style Dictionary JSON, create a
Tier 1 profile with:

```bash
node scripts/create-profile.mjs --profile <profile-id> --name "<name>" \
  --tokens <tokens.json> --register
```

Review `semantic/unmapped-tokens.json` before generation. Do not promote a
partial profile to stable or infer unresolved semantic roles without user input.

*Layer 3 — Brand (load when user specifies a brand):*
- Read [`design-system/brand/index.md`](design-system/brand/index.md), then check
  `design-system/brand/<name>/` for matching brand tokens and override standard defaults.

**5. Run the pipeline.** Follow `system-prompt.md` through L1 → Scene Engine → design-system load → binding gate → L2 → L3 → L4 → output.

**6. Verify and deliver.** Run `agents/run-pipeline.mjs <project-dir> --strict-measure` with Node >= 22. A P0/P1 measurement, including icon provenance/rendering/alignment failure, blocks acceptance. Per your harness reference: serve over HTTP, inspect the measured screenshot, fix errors, rerun, then send file + URL.

## Output location

All files go to `designs/<project-name>/`:

```
designs/<project-name>/
├── preview.html
├── annotated.html
├── tokens.css
├── spec.json
├── assumptions.log
├── preview.measure-report.json
├── preview.measured.png
└── acceptance.spec.mjs
```

## Invocation examples

```
设计一个商品详情页，移动端，有加购栏和图文详情
```

```
从这张截图还原规格，输出给 AI coding 工具用
```

```
用 Example Brand 设计系统，设计一个入职申请表单页面
```

```
用 Ant Design，设计一个移动端 H5 商品列表页，支持筛选和排序
```

```
用 Ant Design，设计一个 PC 后台数据报表页面，含图表和数据表格
```

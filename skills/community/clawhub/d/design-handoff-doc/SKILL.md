---
name: design-handoff-doc
description: "Generate developer-facing design handoff documents from screenshots or design descriptions. Use when user needs a design delivery doc, handoff spec, cut asset list, or annotation guide for developers."
---

# Design Handoff Doc Generator

Generate complete, developer-ready design handoff documents (设计交付说明) from design screenshots, Figma links, or design descriptions. Produces a structured doc that developers can directly use to implement the design.

## When to Use

- User needs a design handoff document (设计交付文档/设计交付说明)
- User needs a cut asset list (切图清单)
- User needs an annotation guide (标注说明)
- User needs interaction notes (交互备注)
- User mentions any of: 交付、切图、标注、handoff、设计说明、design delivery

## Inputs Needed

Before generating, gather (or ask if missing):

1. **项目名称** (project name)
2. **平台** (platform): 小程序 / App / Web / 大屏
3. **设计稿来源** (design source): 截图上传 / Figma 链接 / 文字描述
4. **页面/模块名称** (page or module name)
5. **特殊说明** (special notes, optional): 动效、异常态、特殊交互等

If the user provides a screenshot, analyze it and extract layout, components, colors, spacing, typography automatically.

If the user provides a Figma link, note that direct API access may not be available — ask for key specs or screenshot instead.

If the user gives only a description, generate based on the description + platform best practices.

## Workflow

1. **确认项目与页面信息** — If critical info is missing (project name, platform, page name), ask. Otherwise proceed.
2. **分析设计稿** — If a screenshot/image is provided:
   - Identify layout structure (header, content, footer, sidebar, etc.)
   - Extract visible components (buttons, inputs, cards, lists, tabs, etc.)
   - Note color usage (background, text, accent, borders)
   - Estimate spacing and sizing patterns
   - Identify typography hierarchy
   - Flag any states visible (normal, selected, disabled, error, etc.)
3. **选择模板** — Load the appropriate template from `assets/`:
   - `handoff-template-mini-program.md` for 小程序
   - `handoff-template-app.md` for App
   - `handoff-template-web.md` for Web
   - `handoff-template-large-screen.md` for 大屏
   - `handoff-template-general.md` for通用/不确定平台
4. **生成交付文档** — Fill in the template with:
   - Page structure overview
   - Component breakdown with specs (size, color, spacing, font, radius, states)
   - Asset/cut list (what needs to be exported)
   - Interaction notes (click, hover, scroll, animation, edge cases)
   - Responsive/adaptation notes
   - Data requirements (what data each component needs from backend)
5. **输出** — Present the full handoff doc in chat. If user wants a file, save to `.md` in workspace.

## Output Structure

Every generated handoff doc includes:

1. **页面概述** — Page name, platform, design size, brief description
2. **设计稿信息** — Design file link, designer, version, date
3. **页面结构** — Layout breakdown (regions, hierarchy)
4. **组件清单** — Each component with detailed specs:
   - 尺寸 (width × height)
   - 色值 (background, text, border — HEX)
   - 字体 (family, size, weight, line-height)
   - 间距 (padding, margin)
   - 圆角 (radius)
   - 阴影 (shadow)
   - 状态 (normal / hover / active / disabled / error / loading / empty)
5. **切图清单** — Assets that need to be exported:
   - 图标 (icons)
   - 图片 (images/illustrations)
   - 背景图 (background patterns)
   - Format, size, naming
6. **交互说明** — Interaction and animation notes:
   - 点击行为 (tap/click behavior)
   - 页面跳转 (navigation)
   - 动效 (transitions, loading, feedback)
   - 异常态 (error, empty, loading, no-network)
7. **数据需求** — What data fields each component needs
8. **适配说明** — Responsive, safe area, platform-specific notes
9. **验收标准** — Acceptance checklist for QA

## Platform-Specific Handoff Notes

### 小程序
- 标注单位用 rpx（设计稿 750px 宽）
- 注明原生组件 vs 自定义组件
- TabBar / NavigationBar 用原生还是自定义
- 注意底部安全区适配
- 分享卡片设计（封面图 5:4）

### App
- iOS / Android 差异点需分别标注
- 标注单位用 pt（iOS）/ dp（Android）
- 注明原生导航栏还是自定义导航栏
- 深色模式适配说明
- 手势交互（侧滑返回、长按等）
- Haptics 反馈

### Web
- 标注单位用 px
- 响应式断点（768 / 1024 / 1440 / 1920）
- hover / focus 状态必须标注
- 键盘可访问性说明
- 浏览器兼容性要求

### 大屏
- 标注单位用 px（注明设计基准分辨率）
- 适配缩放策略（等比缩放 / 自适应）
- 数据刷新频率
- 远距离可读性确认（字号、对比度）

## Quality Checklist

Before delivering, verify:
- ✅ Every interactive element has a clear behavior note
- ✅ Every visible component has size + color + font specs
- ✅ All states are documented (normal / pressed / disabled / error / empty / loading)
- ✅ Cut asset list is complete with format + naming
- ✅ Edge cases are covered (empty data, error, no network, loading)
- ✅ Platform-specific constraints are noted
- ✅ Data fields are mapped for backend integration

## References

- `references/component-checklist.md` — Component spec checklist to ensure nothing is missed
- `references/naming-convention.md` — Asset naming conventions per platform
---
name: design-spec-generator
description: "Generate complete design system specification documents for mini-program, App, and large-screen interfaces. Use when user needs a design spec, design system, style guide, or design handoff document."
---

# Design Spec Generator

Generates complete, production-ready design system specification documents for 小程序 (mini-program), App, and 大屏 (large-screen) interfaces. Produces a cohesive spec that can be handed directly to developers or team members.

## When to Use

- User needs a design specification document (设计规范文档)
- User needs a design system (设计系统) for a new project
- User needs to standardize an existing product's design
- User needs a design handoff document (设计交付文档) for developers
- User mentions any of: 规范、设计系统、样式指南、design system、style guide

## Inputs Needed

Before generating, gather (or ask if missing):

1. **项目名称** (project name)
2. **平台类型** (platform): 小程序 / App / 大屏 / Web / 多端
3. **业务领域** (business domain): e.g. 电商、教育、金融、医疗、政务、IoT
4. **品牌色或主色调** (brand color or main hue, optional)
5. **设计风格方向** (style direction, optional): 简约/活泼/科技感/高端/国潮/扁平/拟物等

If the user gives minimal input, use sensible defaults per platform and state assumptions clearly.

## Workflow

1. **确认项目信息** — If any critical input is missing (platform, business domain), ask. Otherwise proceed with what's given.
2. **选择模板** — Load the appropriate template from `assets/`:
   - `mini-program-spec.md` for 小程序
   - `app-spec.md` for App
   - `large-screen-spec.md` for 大屏
   - `web-spec.md` for Web
   - `multi-platform-spec.md` for 多端 (used with a base spec + platform deltas)
3. **生成规范内容** — Fill in the template with:
   - Logically consistent color system (primary, secondary, neutral, semantic) derived from brand color
   - Typography scale with px/pt values appropriate to the platform
   - Spacing system (4pt / 8pt grid)
   - Component design tokens
   - Platform-specific constraints and best practices
4. **输出** — Present the full spec document in chat. If user wants a file, save to `.md` or `.docx` in the workspace.

## Output Structure

Every generated spec includes these sections (platform variants adjust details):

1. **概述 & 设计原则** — Project overview, design philosophy, core principles
2. **色彩系统** — Primary/secondary/neutral/semantic colors with HEX values and usage guidelines
3. **字体系统** — Type scale, font families, weights, line heights
4. **间距与栅格** — Spacing tokens, grid system, breakpoints
5. **圆角与阴影** — Corner radius tokens, elevation/shadow levels
6. **图标规范** — Icon size standards, stroke weight, style guidance
7. **组件规范** — Button/input/card/navigation/etc. design tokens
8. **平台规范** — Platform-specific: safe areas, status bar, navigation styles, screen sizes, density
9. **交付说明** — How to hand off (切图、标注、命名规范)

## Platform-Specific Notes

### 小程序 (Mini-Program)
- Design at **750px 视觉稿宽度** (rpx convention)
- 1rpx = 屏幕宽度/750
- TabBar: 48px 高 (iOS) / 安全区适配
- NavigationBar: 44px 状态栏 + 40px 导航栏
- Safe area: 底部安全区 (iPhone X+ 系列需适配)
- 按钮最小点击区域: 88rpx (44pt)

### App
- Design at **375pt / 750px** base (iOS) with Android dp conversion (1pt ≈ 1dp at xxhdpi)
- 状态栏: iOS 44pt / Android 24dp
- NavigationBar: 44pt (iOS) / 56dp (Android)
- TabBar: 49pt (iOS) / 56dp (Android)
- 最小点击目标: 44×44pt (iOS) / 48×48dp (Android)
- iOS 安全区: 刘海 44pt, 底部 home indicator 34pt

### 大屏 (Large Screen)
- Typical resolutions: 1920×1080, 2560×1440, 3840×2160 (4K)
- 常用 12 列 / 24 列栅格系统
- 数据可视化是核心，需强化图表规范
- 字体: 标题建议使用较粗字重，正文保持清晰
- 色彩: 深色背景 (深蓝/深灰) 是主流，需注意对比度
- 适配策略: 建议按固定设计分辨率设计，用 scale 缩放适配

## Design Token Naming

Use consistent token naming convention:

```text
color-primary-500      → 品牌主色
color-secondary-500    → 辅助色
color-neutral-100      → 浅灰背景
color-semantic-success → 成功绿
font-size-base         → 正文基准字号
spacing-4              → 4px 基础间距
radius-sm / md / lg    → 圆角
shadow-1 / 2 / 3       → 阴影层级
```

## Quality Checklist

Before delivering, verify:
- ✅ Color palette is harmonious and accessible (WCAG AA contrast for text)
- ✅ Type scale has clear hierarchy (min 3 levels: display/title/body/caption)
- ✅ Spacing follows a consistent base unit (4 or 8pt)
- ✅ Radius & shadow tokens are consistent
- ✅ Platform constraints are included (safe areas, minimum touch targets)
- ✅ Component tokens cover at least: button, input, card, navigation, feedback (toast/dialog)
- ✅ Naming convention is consistent throughout

## Templates

Templates live in `assets/`. If user needs the spec as a file, generate from template and save to workspace root (or ask where to save).
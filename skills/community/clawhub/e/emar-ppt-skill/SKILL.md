---
name: emar-ppt-skill-clawhub
description: Create Emar-branded horizontal web PPT decks as single HTML files. Use when making presentation slides, keynote-style share decks, event decks, report decks, image-backed covers, or Swiss Style / electronic magazine style HTML slides for Emar Online internal use. 创建 Emar 品牌横向网页 PPT，输出单 HTML 文件；适用于演讲分享、活动发布、报告汇报、图片封面、瑞士风或电子杂志风内部展示。
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/op7418/emar-ppt-skill
---

# Emar PPT Skill / Emar PPT 技能

Create a single-file horizontal HTML slide deck for Emar Online internal presentations.

为 Emar Online 内部展示创建单文件横向 HTML 幻灯片。除非用户明确要求移除，否则每份生成的演示稿都应保留模板内置的 EMAR logo header。

Every generated deck should keep the built-in EMAR logo header from the templates unless the user explicitly asks to remove it.

## Output / 输出

Produce `index.html` by copying and editing one of the bundled templates.

通过复制并编辑内置模板生成 `index.html`。

- `assets/template.html`: Style A, electronic magazine plus e-ink, serif titles, fluid visual background, warmer editorial feeling.
- `assets/template.html`：风格 A，电子杂志 × 电子墨水，衬线标题、流体视觉背景，整体更温暖、更具编辑感。
- `assets/template-swiss.html`: Style B, Swiss International Style, grid-first layout, high contrast anchor color, stronger data/report feeling.
- `assets/template-swiss.html`：风格 B，瑞士国际主义，网格优先、高对比锚点色，更适合数据、报告和结构化信息表达。

The generated deck should support keyboard, wheel, touch navigation, ESC index view, local Motion One fallback, and static mode where supported by the template.

生成的演示稿应支持键盘、滚轮、触摸导航、ESC 索引视图、本地 Motion One fallback，以及模板支持的静态模式。

## Workflow / 工作流

1. Clarify only the blocking inputs before editing: style A or B, audience, duration/page count, source material, image/screenshot needs, theme color, and hard constraints.
2. If the user gives enough material, make reasonable assumptions and start; do not stall on minor gaps.
3. Copy the selected template into the project output folder as `index.html`.
4. Replace slide content section by section while preserving the template's navigation, logo header, CSS variables, scripts, and data attributes.
5. Use bundled references only when needed; do not load every reference file by default.
6. Preview or statically inspect the final HTML. For Swiss decks, run the validator when Node is available.

1. 编辑前只确认阻塞性输入：风格 A 或 B、受众、时长/页数、源材料、图片/截图需求、主题色和硬约束。
2. 如果用户已提供足够材料，进行合理假设并开始制作，不因细小信息缺口停滞。
3. 将选中的模板复制到项目输出目录并命名为 `index.html`。
4. 按章节替换幻灯片内容，同时保留模板导航、logo header、CSS 变量、脚本和 data attributes。
5. 只在需要时读取内置参考文件，不要默认加载全部 reference。
6. 对最终 HTML 进行预览或静态检查。使用瑞士风模板时，如果 Node 可用，应运行验证器。

## Style Selection / 风格选择

Use Style A when the user asks for a magazine feel, narrative talk, industry observation, personal sharing, warm editorial style, documentary photos, or does not specify a style.

当用户要求杂志感、叙事型分享、行业观察、个人分享、温暖编辑风、纪实图片，或没有明确指定风格时，使用风格 A。

Use Style B when the user asks for Swiss Style, Helvetica/grid/minimal design, product or engineering content, data reports, KPI pages, roadmaps, process diagrams, evidence walls, or strong information hierarchy.

当用户要求 Swiss Style、Helvetica/网格/极简设计、产品或工程内容、数据报告、KPI 页面、路线图、流程图、证据墙，或强信息层级时，使用风格 B。

## Resource Guide / 资源指南

Read these files only when relevant.

仅在相关场景读取以下文件。

- `references/themes.md`: Style A color themes. / 风格 A 配色主题。
- `references/layouts.md`: Style A slide layouts and HTML patterns. / 风格 A 页面布局和 HTML 模式。
- `references/themes-swiss.md`: Style B color themes. / 风格 B 配色主题。
- `references/layouts-swiss.md`: Style B locked slide layouts S01-S22. / 风格 B 锁定布局 S01-S22。
- `references/swiss-layout-lock.md`: Swiss layout constraints and rules. / 瑞士风布局约束和规则。
- `references/components.md`: Shared visual components. / 通用视觉组件。
- `references/image-prompts.md`: Image and cover prompt patterns. / 图片与封面提示词模式。
- `references/screenshot-framing.md`: Screenshot treatment and framing rules. / 截图处理与构图规则。
- `references/swiss-map-component.md`: Swiss map component patterns. / 瑞士风地图组件模式。
- `references/checklist.md`: Final QA checklist. / 最终 QA 检查清单。

## Image Handling / 图片处理

Place slide images beside the deck in `images/` and use stable names like `01-cover.jpg`, `03-dashboard.png`, or `05-flow.jpg`.

将幻灯片图片放在演示稿旁边的 `images/` 目录中，并使用稳定命名，例如 `01-cover.jpg`、`03-dashboard.png` 或 `05-flow.jpg`。

Prefer source images at least 1600px wide. Keep generated presentation assets small enough for smooth local browser playback.

优先使用宽度至少 1600px 的源图。生成的演示资源应保持适当体积，确保本地浏览器播放顺畅。

For local image tags inside the deck, use `images/...` paths. For Swiss image slots, keep `data-image-slot` attributes aligned with the selected locked layout.

演示稿内的本地图片标签使用 `images/...` 路径。瑞士风图片槽位需要保持 `data-image-slot` 属性与所选锁定布局一致。

## Swiss Validation / 瑞士风验证

When the generated deck uses Style B and Node is available, run:

当生成的演示稿使用风格 B 且 Node 可用时，运行：

```bash
node scripts/validate-swiss-deck.mjs <path-to-index.html>
```

Fix reported errors before delivering the deck. Use `--allow-experimental` only when the user explicitly accepts experimental layouts.

交付前修复验证器报告的问题。仅当用户明确接受实验性布局时，才使用 `--allow-experimental`。

## Design Rules / 设计规则

- Preserve the EMAR logo header in both templates. / 在两个模板中都保留 EMAR logo header。
- Keep one strong visual idea per slide. / 每页保留一个清晰有力的视觉主张。
- Avoid stuffing training-manual density into the deck. / 避免把演示稿做成培训手册式的高密度材料。
- Prefer large type, strong contrast, and intentional whitespace. / 优先使用大字号、强对比和有意识的留白。
- Avoid center-aligned Swiss body titles unless the locked layout explicitly uses a statement/cover structure. / 除非锁定布局明确使用 statement/cover 结构，否则避免瑞士风正文标题居中。
- Keep SVG for geometry; put visible labels in HTML text so the deck remains readable and editable. / SVG 用于几何图形；可见文字标签应放在 HTML 文本中，保证可读、可编辑。
- Do not write provenance notes, repository URLs, or skill implementation details into generated slides unless the user asks for them. / 除非用户要求，不要把来源说明、仓库 URL 或技能实现细节写入生成的幻灯片。

## Delivery / 交付

Return the path to the generated `index.html`, summarize the selected style, page count, key assumptions, and any validation that was run.

交付时返回生成的 `index.html` 路径，并总结所选风格、页数、关键假设和已运行的验证。

If preview or validation could not run, state that explicitly.

如果无法预览或无法运行验证，需要明确说明。

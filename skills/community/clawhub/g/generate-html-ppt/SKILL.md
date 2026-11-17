---
name: generate-html-ppt
description: When the user asks to create an HTML PPT, presentation slides, or a deck, or convert an existing PowerPoint (.pptx) file, use this skill to generate a modern, responsive HTML presentation based on design system specifications (design.md). This includes Chinese requests such as 做PPT、幻灯片、演示文稿、网页版PPT、PPT转换.
---

> ## ⚡ Quick Reference (速查表)
>
> 第一次回复就把用户意图对应到三种模式之一：
>
> | 用户原话 | 模式 | 跳到 | 产物 |
> | :--- | :--- | :--- | :--- |
> | 做PPT / 幻灯片 / 做个 deck | **A · 从零创作** | Phase 1 | 单个自包含 HTML |
> | 把 .pptx 转 HTML | **B · PPTX 转换** | Phase 4 | 镜像源结构的 HTML |
> | 封面 / 公众号头图 / 小红书 | **C · 封面生成** | Phase 5 | 1+ 平台尺寸图 |
>
> **不确定？** 默认 Mode A + Beautiful Modern，主动提议先生成 1-3 页风格预览
> （Phase 1.3）。用户随时可改口："换 Mode B" 或 "其实我有个 .pptx" 都被尊重。
>
> **没想好风格？** 先读 `designs/bold-template-pack/selection-index.json` 元
> 数据推荐 2-3 个候选，再按需读具体模板的 `design.md`。节省 token，避免误选。
>
> **国内网络 / 公司内网 / 离线？** 生成前先读 `designs/font-stack-fallback.md`。默认
> `template.html` 已内置本地与官方 CDN 镜像链 (vendor → cdnjs → jsDelivr → unpkg)
> 全量配置 SRI 完整性校验与字体超时降级条，绝不引入未受信镜像，页面安全且不白屏。

## Mode Decision Tree (模式决策树)

```
用户意图
│
├─ "转换 / 转 / migrate .pptx" ──────> Mode B (Phase 4)
│
├─ "封面 / 公众号 / 小红书" ─────────> Mode C (Phase 5)
│
├─ "做 / 写 / 制作" + 已有主题 ────> Mode A (Phase 1)
│   │
│   └─ 有主题但无风格偏好 ─────────> 默认 Beautiful Modern,
│                                    主动提议 1-3 页风格预览
│
└─ "帮我 / help" + 模糊需求 ───────> 问 7 问清单
                                    (references/requirements-checklist.md)
```

# HTML PPT Generation Skill

When the user requests an HTML presentation or PPT, follow these instructions to create it.

## Overview

Presentations are generated using a **Design System Specification (`design.md`)** architecture combined with **Progressive Disclosure**. Rather than relying on rigid, hardcoded HTML templates, visual styles are authored as comprehensive design recipes specifying fonts, color palettes, elevation shadows, typography scales, layout rules, and animation patterns.

### Core Principles
1. **Design System Specification (`design.md`) Architecture**: Access over 35+ distinct aesthetic design recipes (e.g., Beautiful Modern, Swiss International, Cyberpunk Dark, 8-Bit Orbit, Emerald Editorial, Neo Grid, Monochrome, Retro Zine) defined in `designs/bold-template-pack/` and `designs/STYLE_PRESETS.md`.
2. **Progressive Disclosure**: High token efficiency. First read `designs/bold-template-pack/selection-index.json` to match styles based on text metadata. Only after the style is chosen, read that specific template's single `design.md` file to construct the presentation.
3. **Fixed 16:9 Stage (NON-NEGOTIABLE)**: Every slide canvas is authored inside a 1920×1080 stage scaled uniformly to the viewport using JavaScript (`updateScale()`). Content never reflows per device.
4. **Seamless Viewport Rule (视口无缝融合规范)**: All presentations must use CSS variables (`--viewport-bg`) on `body` / `.deck-viewport` and dynamic JavaScript (`updateViewportBg()`) to synchronize the outer screen background with the active slide's background.
5. **Text-First Workflow**: Preserves the signature 3-stage user workflow: **Text-based requirement alignment ➔ Design-guided wireframing (灰度骨架确认) ➔ Guided batch content filling ➔ Verification**.
6. **页眉三要素紧凑压缩与空间让渡规范 (Header Area Compression Rule · NON-NEGOTIABLE)**: 正文页（Content Slides）的 Badge/分类标签、主标题、副标题/金句引导语在纵向空间的占用必须保持扁平紧凑，**页眉总高度严格控制在画布的 18%~22% 以内（<= 200px~220px on 1080p）**，杜绝多层大外边距堆叠，将 78%~82% 黄金垂直空间完整让渡给核心内容区。**注意**：首页 PPT（Cover Slide / 封面页）作为整套演示门面与视觉焦点，豁免紧凑压缩，采用开阔舒展的专属宽纵向间距。
7. **每次生成必配底栏四件套与全景缩略图交互 (Mandatory 4-Button Toolbar & Overview Gallery · NON-NEGOTIABLE)**: 每次生成 HTML PPT 必须在底部居中配备毛玻璃控制栏，包含 **`◀ 上一页`**、**`页码/进度条`**、**`下一页 ▶`**、**`🗂 全览`** 与 **`⛶ 全屏`** 按钮，并内置基于 DOM/JS 的全景缩略图模态框与快捷键引擎（`←`/`→`/`Space` 翻页，`O` 打开全览，`F` 全屏，`Esc` 关闭全览/全屏）。
8. **主要内容大字号高可读性规范 (High-Legibility Large Font Standard · NON-NEGOTIABLE)**: 杜绝 12px~14px 细碎小字感。在 1920×1080 舞台下，卡片正文与段落不低于 `20px~22px`，副标题 `22px~26px`，卡片标题 `26px~28px`，分类徽章 `16px~18px`，数据大字 `56px~72px`，表格与代码 `19px~21px`，保证大屏演说与移动/笔记本视口缩放下的极佳易读性。
9. **图片/图标/序号徽章与文字单行同行并排规范 (Inline Icon, Badge & Title Standard · NON-NEGOTIABLE)**: 在卡片（`.card` / `.b-card` / `.feat-card`）、架构层级（`.stack-row` / `.tier-card`）、流水线步骤（`.pipeline-step` / `.step`）、功能列表等模块中，**图片、图标、Emoji 或序号徽章与对应的标题文字必须处于同一行展示（`display: flex; align-items: center; gap: 10px~14px;` 或在 `<h3>` 内前置 `<span class="badge">` / `<span class="icon-box">`），严禁无故上下拆成两行展示**。**唯一豁免例外**：仅当图片/图标与文字极长、在一行内确实无法完整容纳导致溢出或排版坍塌时，才可酌情拆为两行展示。
10. **全局色彩基调统一与防频闪规范 (Unified Global Color Palette & Anti-Flicker Standard · NON-NEGOTIABLE)**: 整套演示文稿必须保持全局色彩世界观的高度纯净与一致，**默认采用 100% 全套统一纯深色（Unified Dark Mode）或 100% 全套统一纯浅色（Unified Light Mode）**。**严禁逐页黑白无故交替闪烁（Anti-Pattern: 严禁一页深一页浅导致观众视觉眩光与频闪疲劳）**。唯一豁免结构：长篇大型演说中允许仅对封面/封底/章节过渡大幕页采用深色聚焦，而正文内容页（90%+）必须保持绝对统一的底色基调。

---

## Phase 0: Mode Detection

Determine what the user wants:
- **Mode A: New Presentation** — Create a presentation from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a PowerPoint (`.pptx`) file to HTML. Go to Phase 4.
- **Mode C: Cover Generation** — Generate multi-platform social media covers based on a PPT or article. Go to Phase 5.

Do not generate all slides in a single pass, and do not start building content before the wireframe is confirmed.

---

## Phase 1: Outline & Style Alignment (Text & Visual Preview Protocol)

1. **Requirements Alignment (7-Question Checklist)**
   Clarify requirements via text conversation:
    The full 7-question checklist is the canonical input for style matching. Read it from the standalone file `references/requirements-checklist.md` instead of inlining it here, so any agent can link to a stable anchor and re-read it without parsing this SKILL.md again. Quick recall: style preference, audience & scenario, presentation length, raw materials, visual assets, theme/density mode, hard constraints.
    *For first-time or undecided users*: Proactively offer to generate a quick **Visual Style Preview (风格视觉预览)** before building the full presentation to avoid wasting tokens if the aesthetic isn't right.

2. **Brand Asset Protocol (品牌嗅探)**
   **CRITICAL RULE**: If the user provides a specific company or brand, extract core brand colors (HEX/RGB) and typography via search or local files, injecting them into the selected `design.md` CSS variables (e.g. `--brand-accent`).

3. **Style Matching & Visual Preview Protocol (风格匹配与视觉预览协议)**
   Read `designs/bold-template-pack/selection-index.json` and consult `designs/STYLE_GALLERY.md`. Recommend 2-3 candidate style options tailored to the topic mood and presentation scenario.
   **Visual Gallery & Preview Coverage (视觉图鉴与预览覆盖)**: Use `designs/STYLE_GALLERY.md` and the selected template's design tokens as the canonical source for style comparison. The optional source-repository gallery under `demo/previews/` is not required by the installed skill.
   - Do not depend on a local `preview_png`. If a visual confirmation is useful, generate a small, topic-specific HTML preview or mockup image instead.
   - For interactive previews: offer **Option B (Visual Preview / Method 1 — `style-preview.html` comparison card)** so the user can see rendered cards with actual topic content before committing to the full deck.
   - If a preview PNG is mentioned in `selection-index.json`'s `orphan_previews` block, treat it as informational only (e.g. `cyberpunk-dark.png`, `swiss-international.png` core standalone styles).
   **CRITICAL REQUIREMENT (主动提示视觉预览与低成本确认)**:
   - **Proactive Prompting (主动提示)**: The AI MUST explicitly ask the user whether they want to view a visual style preview first or proceed directly. Present two clear paths:
     - **Option A (Direct Proceed / 直接生成)**: Directly proceed with the top recommended style (e.g., Beautiful Modern or Cyberpunk Dark).
     - **Option B (Visual Preview / 视觉预览对比 - Recommended for first-time users)**: Rapidly generate a 1 to 3 slide visual style comparison card (`style-preview.html` or mockup images) rendered with actual topic content for visual confirmation before constructing the full presentation.
   - **How to execute Option B (1-3 Slide Visual Style Comparison)**:
     - *Method 1 (Multi-Slide / Candidate Card HTML Preview - Recommended)*: Generate a lightweight `style-preview.html` containing 1 to 3 candidate slide preview cards (e.g., Slide 1 Cover, Slide 2 Key Concepts/Timeline, Slide 3 Architecture/Data) rendered with their exact CSS variables, Google Fonts, color tokens, and layout cards. Allow the user to specify how many slide preview cards (1-3) they wish to view.
     - *Method 2 (Style Preview Images)*: Use `generate_image` tool to render 16:9 visual mockup images for candidate styles.
   - Confirm the user's selected style choice after previewing before proceeding to Phase 2.

4. **Draft Narrative Arc Outline**
   Draft a slide-by-slide outline using a classic Narrative Arc:
   - **Hook** (1 slide)
   - **Context** (1-2 slides)
   - **Core** (3-5 slides)
   - **Shift** (1 slide)
   - **Takeaway** (1-2 slides)

---

## Phase 1.5: Image Generation & Screenshot Beautification

Prepare visual assets before building wireframes:
- **图片处理范式(必读)**: 选图片处理方式前先读 [`references/image-treatments.md`](references/image-treatments.md)。所有图片必须选 T1-T8 中的一档,并在 `<img>` 上写 `data-treatment="t-XXX"` 自检属性。**默认走 T2 (Float / 自由留白)**,不要默认套 `frame-img` 卡片 + `figcaption` "原始截图"那套旧范式。
- 用户原始截图/UI 截图: 走 T3 (Inset) 或 T4 (Browser),参考 `references/screenshot-framing.md` 适配比例/背景/留边。
- AI 生成图 / 信息图 / 流程图: 走 T1 (Bleed) / T2 (Float) / T7 (Backdrop),参考 `references/image-prompts.md` 写 prompt。
- 设备截图(手机/桌面): 用 T5 (Device) 而不是 T4 (Browser)。
- 多图分组: 用 T6 (Quiet Frame),单图不加 figcaption。

**图片处理硬规则(全范式通用)**:
- **默认支持鼠标双击图片放大 (Default Double-Click Image Zoom & Lightbox · NON-NEGOTIABLE)**: 生成的页面必须默认支持鼠标双击（dblclick）任意幻灯片图片全屏毛玻璃放大预览，再次双击/单击背景/按 Esc 退出；显式添加 `data-zoomable` 可支持单击放大。全屏放大仅聚焦纯净大图视觉，旁边及下方不展示文字、标题或描述（No caption text display）。
- 禁止 `<figcaption>` 写"原始截图 / 产品截图 / Screenshot / Untitled / Sample" 这类空标签。
- 禁止默认 `.frame-img` 带 `border-radius ≥ 12px` + 中-重 `box-shadow`;默认应为无圆角无阴影(已在 `template-beautiful.html` 重置)。
- 禁止 hover 时 `transform: scale(1.02)` (旧 Beautiful 模板行为)。
- 禁止 `object-fit: cover` 裁 UI 截图的左/右两侧(关键按钮和文字通常在两侧)。

---

## Phase 2: Design-System-Guided Wireframing (灰度骨架确认)

1. **Single-Point Reading of `design.md`**
   Read **ONLY** the single `design.md` specification corresponding to the selected style (e.g. `designs/bold-template-pack/templates/<slug>/design.md` or `designs/STYLE_PRESETS.md`). Extract:
   - Font family imports (Google Fonts / Fontshare)
   - Color tokens (`:root` CSS variables)
   - Typography scale & clamp values
   - Elevation shadows, borders, card styles
   - Animation classes & micro-interactions

2. **Build Stage Wireframe HTML File (骨架代码)**
   Generate the single-file HTML presentation structure:
   - Embed full contents of `designs/viewport-base.css` in the `<style>` block.
   - Include the extracted `design.md` CSS design system tokens and classes.
   - Set up the 1920×1080 `.deck-stage` canvas and scaling script (`updateScale()`, `updateViewportBg()`).
   - Create slide containers (`<div class="slide" id="s{N}">...</div>`).
   - Include slide titles, structural grid/card layout classes, and placeholder text/images.
   
   - **⭐ 硬规则一：页眉三要素紧凑压缩与空间让渡 (Header Compression & Space Yielding)**:
     - **适用场景与双轨规范 (Dual-Track Spacing Standard)**:
       - **🟢 场景 A：仅首页 PPT / 封面页（Cover Slide / Hero Slide）—— 豁免紧凑，采用开阔舒展宽纵向间距 (Spacious Hero Layout)**:
         - 封面页是整套 PPT 的门面与视觉焦点（Hero Impact），无需为下方多卡片让渡纵深。
         - **首页三要素专属宽间距阶梯**：
           - **Badge / 分类标签** (`.eyebrow-pill` / `.kicker` / `.cover-badge` 如 `DESIGN CANVAS`) 与主标题间距：`16px ~ 28px`（开阔舒展，坚决不局促挤压）
           - **主标题** (`h1` / `.slide-title` / `.cover-title` 如 `写 Skill 前先回答四个问题`) 与副标题/金句引导语间距：`20px ~ 32px`
           - **副标题 / 金句引导语** (`.slide-subtitle` / `.lead` / `.cover-sub` 如 `"想清楚问题，比直接写代码更重要" —— 四问设计画布`) 与下方元素（`.cover-stats` / `.cover-divider` / `.hero-middle-bridge` / 作者信息）间距：`36px ~ 56px`
         - **推荐排版**：使用 `.cover-frame` 或 `.slide.hero` 居中或左对齐开阔容器，充分释放纵向呼吸空间与高端大气的视觉门面质感。
       - **🔵 场景 B：正文内容页（Content Slides / 过程页 / 章节页）—— 严格执行页眉三要素紧凑压缩 (Compact Header)**:
         - **三要素界定**：Badge/分类徽章 (`.eyebrow-pill` / `.kicker` / `.slide-label`)、主标题 (`h1` / `h2` / `.slide-title`)、副标题/金句引导语 (`.slide-subtitle` / `.tagline` / `.lead`)。
         - **空间占比上限**：页眉三要素组合的总高度**严格控制在 <= 200px (约占 1080p 画布的 18%~22%)**，杜绝多层 20px+ 外边距堆叠。
         - **正文间距严格规范**：
           - Badge 与主标题间距：`6px ~ 8px`
           - 主标题与副标题间距：`8px ~ 12px`
           - 副标题与下方主内容区间距：`16px ~ 24px`
         - **紧凑布局推荐形式**：
           - *方案 A（垂直左对齐紧凑堆叠）*：使用 `.header-compact`，`Badge -> Title -> Subtitle` 统一在左侧自上而下垂直紧凑编排。
           - *方案 B（左右分栏 Header Split）*：使用 `.header-split`，左侧为 `Badge + 主标题`，右侧并排为 `副标题/金句`。
           - *方案 C（行内前缀 Badge Inline）*：直接在主标题内嵌入 `<span>` 徽章前缀。
         - **主内容空间保障**：确保下方 4 卡片网格、流程管线、多列对比表等核心内容区拥有 **78%~82% 的充分纵深展开空间**。

   - **⭐ 硬规则二：底部导航控制台四件套（上一页、下一页、全览、全屏）与全景模式 (Mandatory Toolbar & Overview Modal)**:
     - 每次生成的 HTML 文件必须在 `<body>` 末尾包含标准的悬浮控制台 HTML、全览模态框 HTML 以及完整自包含的 JS 运行引擎。
     
     ```html
     <!-- 标准底部悬浮控制台 (Controls Bar) -->
     <div class="controls-bar" id="controlsBar">
         <button class="ctrl-btn" onclick="prevSlide()" title="上一页 (← / PageUp)">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg> 上一页
         </button>
         <div class="slide-counter">
             <span id="counter">01 / 12</span>
             <div class="slide-progress-track"><div class="slide-progress-fill" id="progressFill" style="width: 8.3%;"></div></div>
         </div>
         <button class="ctrl-btn" onclick="nextSlide()" title="下一页 (→ / Space / PageDown)">
             下一页 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
         </button>
         <button class="ctrl-btn" onclick="toggleOverview()" title="全览缩略图 (O / Esc)">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> 全览
         </button>
         <button class="ctrl-btn" onclick="toggleFullScreen()" title="全屏演示 (F)">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg> 全屏
         </button>
     </div>

     <!-- 标准全览缩略图模态框 (Overview Modal) -->
     <div class="deck-overview" id="overviewModal">
         <div class="overview-header">
             <div class="overview-title">
                 <span>🗂 幻灯片全览导航</span>
                 <span class="overview-hint">按 ESC 或 O 键快速退出</span>
             </div>
             <button class="overview-close-btn" onclick="toggleOverview()">✕ 关闭全览</button>
         </div>
         <div class="overview-grid" id="overviewGrid"></div>
     </div>
     ```

     ```html
     <!-- 标准控制器与全景缩略引擎 JavaScript -->
     <script>
         let currentSlide = 1;
         const slides = document.querySelectorAll('.slide');
         const totalSlides = slides.length;

         function updateScale() {
             const stage = document.querySelector('.deck-stage') || document.getElementById('stage') || document.getElementById('deck');
             if (!stage) return;
             const scaleX = window.innerWidth / 1920;
             const scaleY = window.innerHeight / 1080;
             const scale = Math.min(scaleX, scaleY);
             const left = (window.innerWidth - 1920 * scale) / 2;
             const top = (window.innerHeight - 1080 * scale) / 2;
             stage.style.transform = `translate(${left}px, ${top}px) scale(${scale})`;
         }

         function updateViewportBg(slideIndex) {
             const slide = document.getElementById(`s${slideIndex}`) || slides[slideIndex - 1];
             if (slide) {
                 const bg = slide.getAttribute('data-bg') || (slide.classList.contains('dark') ? '#0f172a' : '#f8fafc');
                 document.documentElement.style.setProperty('--viewport-bg', bg);
             }
         }

         function showSlide(index) {
             if (index < 1) index = 1;
             if (index > totalSlides) index = totalSlides;
             currentSlide = index;
             slides.forEach((slide, i) => {
                 slide.classList.toggle('active', i + 1 === currentSlide);
             });
             const counter = document.getElementById('counter');
             if (counter) counter.innerText = `${String(currentSlide).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
             const progressFill = document.getElementById('progressFill');
             if (progressFill) progressFill.style.width = `${(currentSlide / totalSlides) * 100}%`;
             updateViewportBg(currentSlide);
         }

         function nextSlide() { if (currentSlide < totalSlides) showSlide(currentSlide + 1); }
         function prevSlide() { if (currentSlide > 1) showSlide(currentSlide - 1); }

         function toggleFullScreen() {
             if (!document.fullscreenElement) {
                 document.documentElement.requestFullscreen().catch(() => {});
             } else {
                 if (document.exitFullscreen) document.exitFullscreen();
             }
         }

         function buildOverview() {
             const grid = document.getElementById('overviewGrid');
             if (!grid) return;
             grid.innerHTML = '';
             slides.forEach((s, idx) => {
                 const card = document.createElement('div');
                 card.className = `overview-card ${idx + 1 === currentSlide ? 'current' : ''}`;
                 
                 // 注意：必须优先使用 textContent 而非 innerText，因为处于非激活状态的幻灯片带有 visibility:hidden，此时浏览器中 innerText 会返回空字符串 ""
                 const titleEl = s.querySelector('h1, h2, h3, .slide-title, .h-hero, .h-xl, .h-lg, .h-md, .display-hero, .display-chapter, .cover-title, .section-title, .chapter-title, [data-title]');
                 let title = titleEl ? (titleEl.textContent || titleEl.innerText || '').replace(/\s+/g, ' ').trim() : '';
                 if (!title) {
                     title = s.getAttribute('data-title') || s.getAttribute('data-label') || `第 ${idx + 1} 页`;
                 }
                 
                 const descEl = s.querySelector('.slide-subtitle, .tagline, .lead, .cover-sub, .body-desc, .desc-compact, p, .card-text, .feature-desc');
                 let desc = descEl ? (descEl.textContent || descEl.innerText || '').replace(/\s+/g, ' ').trim() : '';
                 if (desc.length > 90) desc = desc.slice(0, 88) + '...';

                 card.innerHTML = `
                     <span class="overview-card-badge">${String(idx + 1).padStart(2, '0')}</span>
                     <div class="overview-card-title">${title}</div>
                     <div class="overview-card-desc">${desc}</div>
                 `;
                 card.onclick = () => { showSlide(idx + 1); toggleOverview(); };
                 grid.appendChild(card);
             });
         }

         function toggleOverview() {
             const modal = document.getElementById('overviewModal');
             if (!modal) return;
             const isOpening = !modal.classList.contains('active');
             if (isOpening) {
                 buildOverview();
                 modal.classList.add('active');
             } else {
                 modal.classList.remove('active');
             }
         }

         document.addEventListener('keydown', (e) => {
             const modal = document.getElementById('overviewModal');
             const isOverviewActive = modal && modal.classList.contains('active');
             if (e.key === 'Escape') {
                 if (isOverviewActive) { toggleOverview(); return; }
             }
             if (e.key === 'o' || e.key === 'O') { toggleOverview(); return; }
             if (e.key === 'f' || e.key === 'F') { if (!e.metaKey && !e.ctrlKey) toggleFullScreen(); return; }
             if (isOverviewActive) return;
             if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); nextSlide(); }
             if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prevSlide(); }
             if (e.key === 'Home') { e.preventDefault(); showSlide(1); }
             if (e.key === 'End') { e.preventDefault(); showSlide(totalSlides); }
         });

         window.addEventListener('resize', updateScale);
         updateScale();
         updateViewportBg(1);
     </script>
     ```

   - **Apply Layout Density Strategy (防止中间尴尬中空与过度拉伸)**:
     - *space-between 滥用规避*: 严禁对内容高度较矮（<200px）的中间组件无脑使用 `.between` (`space-between`)，否则会导致元素被甩到最顶和最底，中间形成 200~400px 巨大尴尬空白。
     - *垂直集中分组 (Scheme 1 / center-group)*: 优先使用 `.slide-content.center-group` (`justify-content: center; gap: 40px;`) 或 `.slide-content` (`justify-content: flex-start; gap: 40px;`)，紧密分组标题、中间连通桥与卡片，四周留出自然呼吸 Margins。
     - *中间连通桥 (Middle Bridge Block)*: 
       - 封面/Hero Slide：在标题与底部 Stats 之间加入 `.hero-middle-bridge` 芯片标签行（如 `✦ Viewport 视口无缝同步` 等），消除中空断层。
       - 步骤/流程 Slide：三段式 Pipeline 卡片内务必填充充实的内容要点列表 (Bullet points)，充实卡片纵向高度。
    - **⭐ 硬规则三：主要内容大字号高可读性规范 (High-Legibility Large Font Standard · NON-NEGOTIABLE)**:
      - 杜绝 12px~14px 细碎小字感。在 1920×1080 舞台下，所有生成页面必须遵循大字号标准阶梯：
        - **分类徽章/Pill** (`.eyebrow-pill` / `.kicker` / `.slide-label`): `16px ~ 18px` (`font-weight: 800`)
        - **主标题** (`.slide-title` / `.h-xl`): `48px ~ 54px` (`font-weight: 800/900`)
        - **副标题/金句引导语** (`.slide-subtitle` / `.lead` / `.tagline`): `22px ~ 26px` (`font-weight: 600`)
        - **卡片/分栏标题** (`.b-card h3` / `.card-title`): `26px ~ 28px` (`font-weight: 800`)
        - **卡片正文/主要段落** (`.b-card p` / `.card-text` / `p`): `20px ~ 22px` (`line-height: 1.62`)
        - **列表项/Bullet Items** (`.b-card li` / `.feature-desc`): `19px ~ 21px` (`line-height: 1.6`)
        - **数据大数字** (`.stat-nb`): `56px ~ 72px`，**数据标签** (`.stat-label`): `16px ~ 18px` (`font-weight: 700`)
        - **流水线/Pipeline** (`.step-nb: 19px~20px`, `h3: 24px`, `p: 19px`)
        - **表格** (`.data-table`): `th: 21px (w:800)` / `td: 20px (line-height: 1.5)`
        - **代码块** (`.code-block`): `19px ~ 21px` (`line-height: 1.65`)
        - **金句/引用与 Callout** (`.quote-text: 34px`, `.callout: 23px`)
        - **底栏控制按钮** (`.ctrl-btn` / `.slide-counter`): `16px` (`font-weight: 700/800`)

    - **⭐ 硬规则四：图片/图标/序号徽章与标题单行同行并排规范 (Inline Icon, Badge & Title Standard · NON-NEGOTIABLE)**:
      - **排版核心原则**：在所有卡片（`.card` / `.b-card` / `.feat-card`）、架构层级（`.stack-row` / `.tier-card`）、流水线步骤（`.pipeline-step` / `.step`）等结构中，**图标、Emoji、图片或序号徽章必须与对应的标题文字位于同一行展示**（水平弹性盒 `display: flex; align-items: center; gap: 10px~14px;` 或直接在 `<h3>` 内前置 `<span class="badge">` / `<span class="icon-box">`），严禁无故分两行上下堆叠。
      - **豁免与折行例外 (Exemption Rule)**：除非在极限窄栏或极长文字场景下，图片/图标与文字同行并排确实放不下（导致严重文字溢出或卡片过宽挤压），才可酌情折行拆为两行展示。
      - **推荐与禁止写法对比 (Best Practice vs Anti-Pattern)**:
        ```html
        <!-- ❌ 错误反例：图标/序号与标题上下分两行（浪费纵向空间且排版松散） -->
        <div class="b-card">
          <div class="card-num-badge">01</div>
          <h3 class="card-title">触发条件 Trigger</h3>
          <p>用户说什么话或发生什么事件激活？提取高频关键词与意图模式。</p>
        </div>

        <!-- ✅ 正确写法 A：使用 .card-header / .card-title-row 水平弹性盒同行并排 -->
        <div class="b-card">
          <div class="card-header">
            <span class="card-num-badge">01</span>
            <h3 class="card-title">触发条件 Trigger</h3>
          </div>
          <p>用户说什么话或发生什么事件激活？提取高频关键词与意图模式。</p>
        </div>

        <!-- ✅ 正确写法 B：直接在 h3 内前置 badge / 图标 -->
        <div class="b-card">
          <h3 class="card-title"><span class="icon-box">💳</span> 第一层: 名片索引 ~100 词·永远常驻</h3>
          <p>充当 AI 的轻量索引路由表，仅负责判断"要不要激活此 Skill"。</p>
        </div>

        <!-- ✅ 正确写法 C：流水线 / Pipeline 步骤序号与标题同行并排 -->
        <div class="pipeline-step">
          <div class="step-header">
            <span class="step-nb">01</span>
            <h3>Draft 初稿起草</h3>
          </div>
          <p>AI 帮我起草初稿与核心架构</p>
        </div>
        ```
    - **⭐ 硬规则五：全局色彩基调统一与防频闪规范 (Unified Global Color Tone Standard · NON-NEGOTIABLE)**:
      - **排版色彩核心原则**：生成的整套 PPT 必须保持全局统一的色彩基调（**全套 100% 纯深色 Unified Dark 或全套 100% 纯浅色 Unified Light**），视觉基底与视口无缝同步，**严禁逐页黑白无故交替导致的频闪眩光（Anti-Pattern: 严禁一页深一页浅交替）**。
      - **结构化例外**：在 20P+ 大型长篇演说中，仅允许封面/封底/章节过渡大幕页采用深色反差，而正文内容页（90%+）必须保持绝对统一的底色基调。
    - **DO NOT fill detailed paragraphs yet.**

3. **Stop & Present Wireframe for Approval (骨架确认)**
   Show the wireframe HTML to the user and explain the layout structure. **STOP and wait for user approval** before proceeding to fill detailed content.

---

## Phase 2.5: Content Batch Filling

Once the wireframe is approved:
1. Batch-fill complete copy, data tables, code snippets, and visual assets into each slide structure.
2. Adhere to the selected density mode (Low density vs. High density).
3. Ensure no text or cards overflow their slide boundaries at 1920×1080 resolution.

---

## Phase 3: Verify and Open

1. **Verify Presentation Features**:
   - Fixed 16:9 stage scaling (`updateScale()` on window resize).
   - Seamless Viewport Background synchronization (`--viewport-bg`).
   - **Unified Global Color Theme**: Verify that all slides maintain a consistent global theme (100% unified dark or 100% unified light), with zero arbitrary slide-by-slide black/white flickering.
   - **Header Area Compactness**: Verify that Badge + Title + Subtitle height is <= 22% of slide canvas, leaving generous space for cards/diagrams.
   - **Inline Icon & Badge Standard**: Verify that all card badges, icons, numbers, and titles are aligned on the same horizontal row, with zero unwanted vertical two-line stacking.
   - **Bottom Controls Bar 4 Buttons**: Verify that `上一页`, `下一页`, `全览`, `全屏` buttons exist and are fully functional.
   - **Overview Gallery**: Test opening via `🗂 全览` button or `O` key, clicking a card jumps to that slide, and `Esc` closes overview.
   - **Fullscreen Mode**: Test toggle via `⛶ 全屏` button or `F` key.
   - All `.anim` elements trigger entry animations correctly.
   - Zero text clipping, zero vertical scrolling inside slides, zero panel overlap.
2. **Open in Browser**:
   - Ensure the completed HTML file is opened in the browser for user review.

---

## Reference Documents & Supporting Assets

All relative paths from skill root:

 - `designs/bold-template-pack/selection-index.json` — Compact metadata index of 35 bold design templates. `preview_png` and `orphan_previews` fields are optional source-gallery metadata; do not require their files to be installed.
- `designs/bold-template-pack/templates/*/design.md` — Detailed Design System recipes (read only the selected one).
- `designs/viewport-base.css` — Mandatory 16:9 stage scaling and seamless viewport CSS base.
- `designs/STYLE_PRESETS.md` — Core safe preset recipes (Beautiful Modern, Swiss Style, Cyberpunk Dark).
- `designs/animation-patterns.md` — Animation and micro-interaction guide.
- `references/checklist.md` — Presentation quality checklist.
 - `references/requirements-checklist.md` — Canonical 7-question style alignment checklist used by Phase 1.
- `references/screenshot-framing.md` — Screenshot framing and mockup guide.
- `references/image-prompts.md` — Prompt generation guide for presentation visuals.
- `references/image-treatments.md` — **必读**: 8 套图片处理范式(T1-T8)与 CSS 基座,所有图必须选一档并标 `data-treatment`。
- `scripts/extract-pptx.py` — PowerPoint content extraction script.

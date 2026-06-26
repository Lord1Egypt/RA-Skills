# Presentation Prompt Templates

Ready-to-use prompts for content generation and slide image creation. Loaded on-demand when creating presentations.

## 1. Content Generation Prompts

### Full Presentation Outline

```
Create a [X]-slide presentation about [topic].

Audience: [describe — e.g., busy managers, beginners, investors]
Duration: [minutes]
Goal: [inform / persuade / educate]
Tone: [professional / casual / academic]

Structure:
- Opening: [problem hook / story / data point]
- Body: [logical / chronological / priority order]
- Close: [call to action / summary / open discussion]

Per slide:
- Title = conclusion sentence (not a topic word)
- Max 4 bullet points
- Suggest visual type (chart, diagram, photo, icon)

Brand:
- Colors: [primary / secondary / accent]
- Font: [heading / body]
- Logo placement: [bottom-right / top-left]
```

### Business Report
```
Create a 10-slide pitch deck for [industry] prospects.
Structure: Problem (2 slides) → Impact (1) → Our Solution (3) →
Case Study (2) → Next Steps (1) → Appendix (1).
Audience: VP-level operations. Tone: pragmatic, data-driven.
```

### Educational / Training
```
Design AI-driven slides teaching [concept] to beginners.
Each concept includes one analogy and one real-world scenario.
Use simple language, one key insight per slide.
```

### Annual Review
```
Condense this PDF report into a visual presentation
highlighting three action items. Use KPI dashboard style.
Each slide has a chart or data visualization.
```

### Minimal Startup Pitch
```
Create a minimal-style startup pitch deck.
Use visual metaphors, avoid bullet point stacking.
Each slide: generous whitespace, one core number or short sentence.
```

### Research → Presentation
```
Analyze this research material, extract 3-4 most compelling findings.
Create a narrative flow: Problem → Insight → Implication.
Design slides that simplify complex data without sacrificing accuracy.
```

### Problem-Solution-Result
```
Generate a slide outline using the Problem → Solution → Result structure.
For each section, create 1-2 slides depending on depth.
```

### Long Document → Slides
```
Turn this document(s) into a 7-slide presentation.
Provide a clear and concise slide title for each slide.
Include 3-5 key bullet points per slide.
Focus on main ideas, avoid filler.
```

## 2. Path A HTML 生成规范（html2pptx 硬性约束）

> **必读！** html2pptx.js 将 HTML 逐元素解析为 PowerPoint 对象，不是截图。PPT 格式有固有约束，违反以下 4 条规则会直接报错。

### 4 条不可违反的规则

**规则 1：DIV 里不能直接写文字 — 必须用文字标签包裹**

```html
<!-- ❌ 错误：文字直接在 div 里 -->
<div class="title">Q3营收增长23%</div>

<!-- ✅ 正确：文字在 <p> 或 <h1>-<h6> 里 -->
<div class="title"><h1>Q3营收增长23%</h1></div>
<div class="body"><p>新用户是主要驱动力</p></div>
```

**规则 2：不支持 CSS 渐变 — 只能用纯色**

```css
/* ❌ 错误 */
background: linear-gradient(to right, #FF6B6B, #4ECDC4);

/* ✅ 正确：纯色 */
background: #FF6B6B;

/* ✅ 如果必须多色条纹，用 flex 子元素各自纯色 */
.stripe-bar { display: flex; }
.stripe-bar div { flex: 1; }
.red   { background: #FF6B6B; }
.teal  { background: #4ECDC4; }
```

**规则 3：背景/边框/阴影只能在 DIV 上，不能在文字标签上**

```html
<!-- ❌ 错误：<p> 有背景色 -->
<p style="background: #FFD700; border-radius: 4px;">重点内容</p>

<!-- ✅ 正确：用外层 div 承载背景/边框，<p> 只负责文字 -->
<div style="background: #FFD700; border-radius: 4px; padding: 8pt 12pt;">
  <p>重点内容</p>
</div>
```

**规则 4：DIV 不能有 background-image — 用 `<img>` 代替**

```html
<!-- ❌ 错误 -->
<div style="background-image: url('chart.png')"></div>

<!-- ✅ 正确 -->
<img src="chart.png" style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;" />
```

### Path A HTML 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 720pt; height: 405pt;
    font-family: system-ui, -apple-system, "PingFang SC", sans-serif;
    background: #FEFEF9;           /* 纯色，不能用渐变 */
    overflow: hidden;
  }
  /* DIV 负责布局/背景/边框 */
  .card {
    position: absolute;
    background: #1A4A8A;            /* 背景在 DIV 上 */
    border-radius: 4pt;
    padding: 12pt 16pt;
  }
  /* 文字标签只负责字体样式，不加背景/边框 */
  .card h2 { font-size: 18pt; color: #FFFFFF; font-weight: 700; }
  .card p  { font-size: 12pt; color: rgba(255,255,255,0.85); }
</style>
</head>
<body>

  <!-- 标题区：外层 div 定位，内层文字标签 -->
  <div style="position: absolute; top: 32pt; left: 48pt; right: 48pt;">
    <h1 style="font-size: 28pt; color: #1A1A1A; font-weight: 700;">标题用断言句，不是主题词</h1>
    <p style="font-size: 13pt; color: #555555; margin-top: 8pt;">副标题补充说明</p>
  </div>

  <!-- 内容卡片：div 负责背景，h2/p 负责文字 -->
  <div class="card" style="top: 100pt; left: 48pt; width: 180pt; height: 120pt;">
    <h2>要点一</h2>
    <p>简短说明文字</p>
  </div>

  <!-- 列表：使用 ul/li，不用手动 • 符号 -->
  <div style="position: absolute; top: 240pt; left: 48pt; width: 400pt;">
    <ul style="font-size: 13pt; color: #1A1A1A; padding-left: 20pt; list-style: disc;">
      <li>第一条要点</li>
      <li>第二条要点</li>
      <li>第三条要点</li>
    </ul>
  </div>

  <!-- 插图：用 <img> 标签，不用 background-image -->
  <img src="illustration.png" style="position: absolute; right: 48pt; top: 80pt; width: 240pt; height: 180pt;" />

</body>
</html>
```

### 常见错误速查

| 错误信息 | 原因 | 修复方法 |
|---------|------|---------|
| `DIV element contains unwrapped text "XXX"` | div 里有裸文字 | 把文字包进 `<p>` 或 `<h1>`-`<h6>` |
| `CSS gradients are not supported` | 用了 linear/radial-gradient | 改为纯色，或用 flex 子元素分段 |
| `Text element <p> has background` | `<p>` 标签加了背景色 | 外套 `<div>` 承载背景，`<p>` 只写文字 |
| `Background images on DIV elements are not supported` | div 用了 background-image | 改为 `<img>` 标签 |
| `HTML content overflows body by Xpt vertically` | 内容超出 405pt | 减少内容或缩小字号，或用 `overflow: hidden` 截断 |
| `HTML dimensions don't match presentation layout` | body 尺寸不是 720pt×405pt | 确认 `width: 720pt; height: 405pt` |

---

## 3. Slide Image Generation Prompts

### Base Style Prompt Pattern

Define once, append to every slide:
```
[Base Style Suffix]:
flat illustration style, [background description],
[text color] sans-serif typography, [accent detail],
clean professional aesthetic, 16:9 aspect ratio, 1920x1080
```

**Example base styles:**

**Dark Tech:**
```
flat vector illustration, deep navy gradient background (#0F0C29 to #302B63),
white sans-serif text, subtle teal neon accent lines (#4ECDC4),
minimal data-visualization aesthetic, 16:9, 1920x1080
```

**Clean Corporate:**
```
clean flat design, white background (#FFFFFF),
dark gray text (#2D3436), blue accent elements (#0984E3),
professional infographic style, 16:9, 1920x1080
```

**Warm Educational:**
```
soft watercolor illustration style, cream background (#FDF6EC),
dark text (#3D3D3D), coral accent highlights (#E17055),
friendly approachable aesthetic, 16:9, 1920x1080
```

### Per-Slide Prompt Structure

```
[Slide type]: [Content description].
[Visual elements]: [What to show — chart type, icons, diagrams].
[Layout]: [Title position, content arrangement].
[Base Style Suffix]
```

**Example:**
```
Title slide: "AI is Transforming Healthcare" centered in large bold text.
Subtitle: "3 Breakthrough Applications in 2026" below.
Visual: abstract neural network pattern as subtle background element.
[Dark Tech Base Style]
```

### Google's 6-Element Formula

```
[Subject] + [Composition] + [Action] + [Location] + [Style] + [Editing]
```

- Subject: what/who is the main focus
- Composition: camera angle, distance (wide, close-up, 85mm)
- Action: what the subject is doing
- Location: where the scene takes place
- Style: artistic style, color palette
- Editing: post-processing (soft focus, high contrast, film grain)

### Consistency Tips

1. **Describe, don't keyword** — narrative paragraphs work better than keyword lists
2. **Positive framing** — "empty quiet street" not "street without cars or people"
3. **Photography terms** — use specific lens lengths (85mm f/1.8), lighting (golden hour, studio rim lighting, three-point softbox)
4. **Specify hex colors** — exact color values prevent palette drift
5. **Character drift** — if characters change appearance, start a new conversation with full description

**Sources:**
- [Google Developers: Gemini Image Generation Prompting](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [Google Blog: Image Generation Prompting Tips](https://blog.google/products/gemini/image-generation-prompting-tips/)

## 3. Full AI Slide Generation Prompts (Path B)

Path B generates EVERY slide as a complete AI image. These prompts produce slides where layout, text, and visuals are all rendered by AI.

**⚠️ THE #1 MISTAKE: Writing prompts like CSS layout instructions.** "Title at top-left, two columns below" produces boring traditional PPTs. Instead, describe EXPERIENCE, REFERENCE, and INTENT.

### Base Style Templates (Design System → Prompt)

Each base style is derived from a Design System Preset (see SKILL.md Step 2). Define once, apply to every slide in the deck.

**Warm Narrative:**
```
A complete design system for this deck.

VISUAL REFERENCE: TED talk visual style meets Airbnb pitch deck — approachable storytelling.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: warm cream (#FDF6EC) 60%
- Text: dark charcoal (#3D3D3D) 25%
- Accent: coral (#E17055) 15%
- Color creates warmth, trust, human connection

TYPOGRAPHY AS DESIGN:
- Headlines: 36-44pt bold, warm and inviting
- Body: 18-20pt regular, short sentences not bullets
- Size ratio: 3:1 between title and body

COMPOSITION:
- Illustration occupies 40-50% of slide
- Text wraps around or sits beside visuals
- Rounded shapes, soft edges, no sharp corners

VISUAL LANGUAGE: Flat vector illustrations with warm palette, people-centric imagery,
storytelling flow, rounded shapes, hand-drawn feel optional
```

**Neo-Pop Magazine:**
```
A complete design system for this deck.

VISUAL REFERENCE: Supreme lookbook meets HYPEBEAST article — typography as graphic art.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: cream (#FFF8E7) 50%
- Color blocks: hot pink (#FF1493) + cyan (#00CED1) + yellow (#FFD700) 25%
- Text: black (#000000) 25%
- Color creates energy, youth, playful rebellion

TYPOGRAPHY AS DESIGN:
- Headlines: 40-50% of slide area — TYPOGRAPHY IS THE VISUAL
- Body: minimal, 12-14pt
- Size ratio: 10:1 between display and body
- Thick black borders around text blocks

COMPOSITION:
- Modular color blocks with "controlled chaos"
- Stacked asymmetric layouts
- Thick borders as design element
- Content fills 75%, structured chaos not whitespace

VISUAL LANGUAGE: Pixel-art 8-bit icons, cutout photography, speech bubbles,
bold graphic surfaces, sticker/patch aesthetic
```

**Ligne Claire Comics:**
```
A complete design system for this deck.

VISUAL REFERENCE: Hergé's Tintin tradition — maximum information clarity through
visual restraint. Every line serves a purpose.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: white/cream (#FFFDF7) 70%
- Illustration: flat saturated fills (3-5 solid colors, no gradients) 20%
- Text: black (#000000) outlines and lettering 10%
- Color is informational, not decorative — each color codes a concept

TYPOGRAPHY AS DESIGN:
- Titles: hand-lettered comic feel, bold and warm
- Body: clean sans-serif, in speech bubbles or caption boxes
- Size ratio: 2.5:1 between title and body
- Key quotes in speech bubbles with pointer tails

COMPOSITION:
- Panel-based layouts (2-4 panels per slide), sequential left-to-right reading
- Clear gutters (white space) between panels
- Each panel advances one idea — no panel is decorative

VISUAL LANGUAGE: Uniform-weight black outlines, flat colors without shading
or hatching, no gradients ever, precise details but zero visual noise,
clean backgrounds, characters with simple but expressive faces
```

**Whiteboard Sketch:**
```
A complete design system for this deck.

VISUAL REFERENCE: xkcd "What If?" meets a professor's whiteboard after an
exciting lecture — the beautiful mess of someone thinking out loud.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: pure white (#FFFFFF) 85%
- Ink: black (#000000) for all drawings and text
- Accent: ONE color only (red #FF4444 or blue #4488FF) for highlighting key insights
- The restraint IS the design — monochrome forces focus on the idea

TYPOGRAPHY AS DESIGN:
- Everything hand-drawn/handwritten feel, rough uneven baselines
- Key numbers rendered large (60-80pt) as visual anchors
- Annotations everywhere — arrows, circles, underlines
- Math-style notation where appropriate

COMPOSITION:
- Freeform whiteboard layout, no rigid grid
- Hand-drawn arrows connecting concepts
- Stick figures and simple diagrams
- Informal, alive, like someone just drew this

VISUAL LANGUAGE: Stick figures with expressive poses, hand-drawn wobbly charts
and graphs, annotation arrows, circled keywords, equation-style layouts,
crossed-out wrong answers, "aha!" moments marked with stars
```

**Manga Educational:**
```
A complete design system for this deck.

VISUAL REFERENCE: Japanese educational manga (学習漫画) like "Manga Guide to
Statistics" — a character GUIDES you through concepts with reactions and drama.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: white with selective color panels
- Characters: bright warm palette, skin tones + hair colors
- Emphasis: screen-tone gray for flashback/explanation areas
- Accent: manga-style color bursts for key moments

TYPOGRAPHY AS DESIGN:
- Bold manga-style impact titles (thick, slightly angled)
- Body text in speech bubbles and thought clouds
- Onomatopoeia (ドキドキ, !!!) as decorative design elements
- Size contrast 3:1, dramatic for emphasis moments

COMPOSITION:
- Dynamic manga panel layouts (3-5 panels per slide)
- Character reactions drive emphasis — big eyes for surprise, sweat drops for confusion
- Speed lines radiating from key insights
- Reading flow: right-to-left for authenticity, or left-to-right for international

VISUAL LANGUAGE: Expressive anime-style characters, big emotional reaction faces,
manga effects (sparkles ✨, speed lines, impact stars, sweat drops 💧),
panel borders with varied thickness, dramatic angles on key reveals
```

**Warm Comic Strip:**
```
VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
The world is simple (grass, sky, doghouse, trees) but the ideas are deep.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels,
warm ink lines (not harsh black). Everything feels like a Sunday morning comic page.
```
**NOTE:** Keep this base style SHORT. Do not add detailed color ratios, composition
rules, or typography specs — over-constraining kills diversity and character variety.
See `proven-styles-snoopy.md` for the full principle: describe mood, not layout.

### 🎨 Custom Character Style Reference

Users may reference specific cartoon/anime aesthetics (e.g., "Doraemon style", "Ghibli feel"). Extract the **visual DNA** and build a prompt around the style traits, not the character IP.

**Common references → prompt traits:**

| User says | Shape language | Line quality | Palette | Emotional tone |
|-----------|---------------|-------------|---------|----------------|
| "Doraemon" | Round, soft | Clean uniform | Bright primary blue + white + red | Warm, magical, educational |
| "Studio Ghibli" | Organic, natural | Detailed watercolor | Natural greens, sky blues, earth tones | Wonder, warmth, nostalgia |
| "Calvin and Hobbes" | Dynamic, varied | Expressive ink brush | Lush outdoor greens, sunset oranges | Philosophical, adventurous |
| "One Piece" | Exaggerated, bold | Thick dynamic | High-contrast, saturated | Energetic, dramatic |
| "Crayon Shin-chan" | Crude, chunky | Rough crayon-like | Flat bright primary | Absurd, everyday humor |
| "Adventure Time" | Geometric, simple | Thin uniform | Pastel candy colors | Whimsical, surreal |
| "Snoopy/Peanuts" | Simple, round | Clean thin (#333333 not #000) | Muted warm pastels (#FFF8E8 base) | Philosophical, gentle — ⭐ See `proven-styles-snoopy.md` for detailed proven guide |

**Template:**
```
CUSTOM STYLE: Inspired by [reference name] aesthetic.
Shape language: [round/angular/geometric/organic]
Line quality: [thin uniform / thick varied / sketchy / brushwork]
Color palette: [specific hex codes extracted from that aesthetic]
Character style: [proportions, expressiveness, detail level]
Background treatment: [detailed/minimal/abstract/none]
Emotional tone: [warm/energetic/philosophical/surreal/dramatic]
```

### Per-Slide Prompt Template

Replace [bracketed items] with your content. The key difference from boring prompts: every slide has a **Visual Reference**, **Design Intent**, and **Visual Narrative**.

```
Create a slide that feels like [visual reference — what specific publication/brand
does this slide evoke? e.g., "a WIRED feature page about breakthrough tech",
"a Bloomberg data visualization", "an Apple keynote product reveal moment"].

[Paste Base Style from above]

DESIGN INTENT: [What should the viewer FEEL? Not what they should read.
e.g., "the asymmetric risk-reward structure should be viscerally obvious",
"the viewer should feel the urgency of time decay",
"the scale of the number should provoke awe"]

TEXT TO RENDER (must be perfectly legible and accurately spelled):
- [Role]: "[exact text]" — rendered as [design instruction, e.g., "120pt hero metric",
  "oversized graphic headline occupying 30% of slide"]
- [Role]: "[exact text]" — rendered as [design instruction]

VISUAL NARRATIVE: [Describe what to SEE using metaphors, photography language,
and emotional atmosphere. NOT layout positions.
e.g., "A golden curve emerging from darkness, flat and gray in the loss zone,
then bending upward into brilliant warm light at the break-even point.
The chart has NO grid lines — just the pure dramatic curve and the giant number
floating at the inflection point like a spotlight."]
```

### Slide Type Examples (GOOD approach)

**Cover — WIRED Editorial style:**
```
Create a slide that feels like the opening spread of a WIRED magazine feature story.

[WIRED Editorial Base Style]

DESIGN INTENT: The viewer should feel they're about to read something important
and intellectually exciting — not another corporate deck.

TEXT TO RENDER:
- Title: "期权" — rendered as massive 80pt graphic headline, taking up 40% of
  slide width, white on charcoal, the characters themselves ARE the design
- Subtitle: "用有限的代价撬动无限的可能" — 18pt, teal accent, positioned as
  a magazine tagline below the title
- Tag: "STOCK OPTIONS GUIDE" — 10pt, spaced-out caps, subtle teal

VISUAL NARRATIVE: The left side is dominated by the oversized Chinese characters,
treated as graphic art — not just text. The right side features an abstract
geometric composition: interlocking angular shapes in charcoal and dark navy,
with thin teal neon lines tracing the edges like circuit paths. The overall
feeling is a tech magazine you'd pick up at an airport bookstore.
```

**Explanation — Manga Educational style:**
```
Create a slide that feels like a page from "Manga Guide to Economics" —
a cheerful character explaining a concept, with dramatic manga reactions
when the key insight lands.

[Manga Educational Base Style]

DESIGN INTENT: The viewer should feel GUIDED through the concept by a
friendly character. The "aha moment" should trigger a visible manga-style
reaction — surprise eyes, sparkles — making the abstract feel personal.

TEXT TO RENDER:
- Title: "什么是期权？" — bold manga impact title, slightly angled, top of slide
- Speech bubble 1: "期权就是花一小笔钱买一个权利" — character explaining
- Speech bubble 2: "但不是义务哦！" — character with index finger up, emphasis
- Reaction text: "原来如此！" — in a starburst speech bubble, eureka moment

VISUAL NARRATIVE: A 3-panel manga layout. Panel 1 (large, left half): a
friendly anime-style character (teacher/guide) with warm smile, pointing
at a simple diagram of "premium → right to buy". Panel 2 (top-right): the
same character holding up a finger with sparkle effect, emphasizing "right,
not obligation". Panel 3 (bottom-right): a second character (student) with
classic manga surprise face — big eyes, mouth open, lightbulb above head,
speed lines radiating outward. Clean white backgrounds in each panel,
thin black panel borders.
```

**Concept — Whiteboard Sketch style:**
```
Create a slide that feels like a brilliant professor just finished drawing
on a whiteboard — messy, alive, and suddenly everything clicks.

[Whiteboard Sketch Base Style]

DESIGN INTENT: The viewer should feel like they're sitting in the front
row of a great lecture. The hand-drawn quality makes complex finance feel
accessible and human, not intimidating.

TEXT TO RENDER:
- Title: "Call vs Put" — hand-drawn, underlined twice
- Left diagram label: "看涨 Call" with upward arrow
- Right diagram label: "看跌 Put" with downward arrow
- Annotation: "一个赌涨 一个赌跌 就这么简单" — circled in red

VISUAL NARRATIVE: A white canvas that looks like a freshly-used whiteboard.
On the left, a hand-drawn stick figure happily riding an upward arrow
(labeled "Call 看涨"), the arrow drawn with confident upward strokes.
On the right, another stick figure with an umbrella as a downward arrow
descends (labeled "Put 看跌"), suggesting protection. Between them,
a hand-drawn "VS" in a rough circle. At the bottom, a wobbly hand-drawn
underline beneath the annotation "就这么简单", circled in red marker —
the only color on the entire slide. Arrows, crossed-out attempts, and
small doodles in margins give it authentic whiteboard energy.
```

### Chinese Text Tips for Path B

1. **Keep titles ≤8 characters** — AI renders short Chinese text most reliably
2. **Body text ≤30 characters per line** — longer lines risk garbling
3. **Avoid rare characters** — stick to common vocabulary
4. **If text renders incorrectly** — simplify the text or split into shorter phrases
5. **Always verify** — check every slide image for text accuracy before assembly
6. **Separate text from visuals** — put text in clear areas, not overlapping complex visuals

### Parallel Generation Strategy

Generate slides in batches of 3-5 concurrently for speed:
```bash
# Run 3 in parallel using background processes
export $(grep GEMINI_API_KEY ~/.claude/.env)
uv run generate_image.py --prompt "slide 1 prompt..." --filename slide-01.png &
uv run generate_image.py --prompt "slide 2 prompt..." --filename slide-02.png &
uv run generate_image.py --prompt "slide 3 prompt..." --filename slide-03.png &
wait
```

### Prompt Quality Checklist (Quick Reference)

Before generating any slide, verify:
- [ ] **Visual Reference** — References a specific publication/brand/art style?
- [ ] **Design Intent** — Expresses what viewer should FEEL?
- [ ] **Color with Purpose** — Hex codes + ratios + emotional function?
- [ ] **Typography as Design** — Headline treated as graphic element with dramatic size ratio?
- [ ] **Visual Narrative** — Described with metaphors and atmosphere, not layout positions?
- [ ] **Negative Space** — Explicitly defined as design element?
- [ ] **NO Generic Adjectives** — Banned: "professional", "clean", "modern", "sleek", "elegant"?

---

## 5. NotebookLM Slide Prompts

### Style Templates (from awesome-notebookLM-prompts)

| Category | Templates |
|----------|-----------|
| Business Editorial | Modern Newspaper, Yellow×Black Editorial, Black×Orange Agency |
| Street/Trendy | Manga Style, Magazine Style, Pink Street-style, Digital Neo Pop |
| Typography-driven | Mincho × Handwritten Mix |
| Art/Avant-garde | Royal Blue×Red Watercolor, Sculpture×Vaporwave, Tech Art Neon |
| Product/Premium | Studio Mockup Premium |
| Athletic/Energy | Sports Athletic Energy |

Each template defines: Global Design Settings (palette, font hierarchy, grid, icon style) + Layout Variations.

### NotebookLM Best Practices

1. **Notes as source** — Write outline in NotebookLM notes, use as source for slide generation
2. **Brand book as source** — Upload brand guidelines, prompt: "Use the brandbook for branding and styling references"
3. **Refresh old decks** — Upload existing Google Slides, let AI redesign with new branding
4. **Multi-source synthesis** — Upload PDFs + videos + web links, AI synthesizes across all
5. **Specify audience** — "for busy managers" / "for beginners" / "for investors"
6. **Two-step method** — First generate a speech script, then use the script to generate slides
7. **Avoid topic titles** — Use narrative topic sentences instead of "Title: Subtitle" format
8. **Upload gold standard** — Upload your best past presentation as a style reference

**Sources:**
- [Google Blog: 8 ways to use Slide Decks in NotebookLM](https://blog.google/technology/google-labs/8-ways-to-make-the-most-out-of-slide-decks-in-notebooklm/)
- [GitHub: awesome-notebookLM-prompts](https://github.com/serenakeyitan/awesome-notebookLM-prompts)
- [XDA Developers: 3 NotebookLM prompts for slides](https://www.xda-developers.com/notebooklm-prompts-to-make-presentation-slides/)

## 6. Public Prompt Resources

| Resource | Link | Highlights |
|----------|------|-----------|
| Superside: 15+ AI Prompts for Presentations | [Link](https://www.superside.com/blog/ai-prompts-presentations) | Full-type templates: business, case study, webinar |
| Slidesgo Smart Guide | [Link](https://slidesgo.com/slidesgo-school/ai-presentations/best-ai-prompts-presentations-smart-guide) | 8 core templates + prompt methodology |
| SlidesAI: 75+ Presentation Prompts | [Link](https://www.slidesai.io/blog/prompts-to-make-presentations-with-ai) | 75+ ready-to-use prompts by scenario |
| awesome-notebookLM-prompts | [Link](https://github.com/serenakeyitan/awesome-notebookLM-prompts) | 20+ visual style YAML templates |
| Sabrina Ramonov: Viral PowerPoints | [Link](https://www.sabrina.dev/p/viral-powerpoints-slides-free-notebooklm) | 3-tier framework with 14 viral layouts |
| Google: Gemini Image Prompting | [Link](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/) | 6-element formula for image prompts |
| DataCamp: NotebookLM Guide | [Link](https://www.datacamp.com/tutorial/notebooklm) | Full NotebookLM tutorial with slides |

## 7. Style Selection Guide (实战验证)

**核心发现（2026-02-08实测）：插画/漫画类风格的AI生成效果远好于「专业极简」类风格。**

暗色底+发光文字+大量留白的风格（如WIRED、霓虹冲击、渐变高端、FT数据新闻）在Full AI Visual (Path B)中效果差，已从Base Style Templates中移除。

推荐优先使用的风格（效果最佳）：
1. **Warm Comic Strip** (Snoopy) — 详见 `proven-styles-snoopy.md`
2. **Manga Educational** (学習漫画)
3. **Ligne Claire Comics** (清线)
4. **Neo-Pop Magazine** (新波普)
5. **Whiteboard Sketch** (xkcd)

更多实测风格（含10种扩展风格的配色/prompt/适用场景）：
→ `proven-styles-gallery.md`

样例图片（17种风格的压缩版，每张<1MB）：
→ `../assets/style-samples/`

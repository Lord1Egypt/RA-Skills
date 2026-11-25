---
version: 0.29.0
name: aesthete-agent
description: Color palette generation, frontend aesthetics, UI color schemes — mechanically validated color output for UI/HTML, SVG slides, video covers, charts and posters. An 119-palette evidence library matched by register, OKLCH harmony generation, luminance ramps and image extraction; 60-30-10 role mapping with semantic colors; a 5-dimension scorecard plus WCAG contrast, color-blind simulation and AI-slop detection as four mechanical gates; card and six-scene visualizer previews; a preference-learning profile that evolves with every verdict. Named theme packs, full contrast matrices, CB-safe data-viz palettes, five-lens critique reports, and APCA (WCAG 3 draft) perceptual contrast included. Pure stdlib, offline. Skip when pure text layout, translation or polishing, copywriting, or any task unrelated to color and frontend aesthetics. Trigger words — color palette, color scheme, palette generation, frontend aesthetics, UI color, design aesthetics, hex, contrast, WCAG, color blind, visual taste, aesthete-agent.
---

# aesthete-agent — Frontend Aesthetics Engine

Why LLM color output is bad, with evidence: models treat hex codes as text, regress to the median of training data (the frontend-tutorial median is purple/indigo), and cannot actually see color. The fix is not a better model — it is **outsourcing taste to process**: manifesto first, role mapping, mechanical validation, in-context self-review.

⛔ Iron rules:
1. **No bare palette writing.** Every color task goes through the six-step method; step 6 (five-lens review) is not skippable.
2. **No runtime access to the source site** — no public API, direct connections hit Cloudflare 403; all data ships offline.
3. **The brief is law**: colors and aesthetics pinned by the user are binding constraints. Already-shipped brand systems are out of scope for re-paletteing.
4. **Bounded verification**: build fully → one batched review → one batched fix round → at most one more confirmation → **stop polishing**.
5. **Candidate discipline**: user verdicts require ≥2 full-page candidates (`make_variants.py` builds the comparison sheet); a single proposal is not sent for review.
6. **Verdict write-back**: every accept/reject lands in `profile.json` (machine-read) and `critique.md` necropsies (failure modes) — no write-back, no growth.

### Task → command (30 seconds)

| Task | Use |
|---|---|
| New palette for a brief | `match --brief` |
| Judge an existing page | `evidence page.html --palette` |
| Fix an existing page | `patch page.html --palette --apply` |
| Chart / data colors | `chartpal --kind` (supersedes `semantic`) |
| Full-page starting point | `scaffold --theme/--palette` (AUTO routes dark/light) |
| Single scene mockup | `scene --kind` |
| Cross-register exploration | `directions` |
| Side-by-side for review | `make_variants` |
| Token sheet | `tokens --palette/--theme` |
| Render review loop | `loop page.html --palette` |

### Golden defaults (3-second edition — defaults are the product, don't hand-tune)

| Dimension | Engine default | Basis |
|---|---|---|
| Fluid type scale | display steps in `clamp()`, rem endpoints, **max≤2.5×min** (always passes WCAG 1.4.4) | web.dev |
| Line height | display 1.15 / heading 1.3 / **body 1.7** (CJK band 1.5-2.0) / caption 1.5 | clreq + dual sources |
| CJK–Latin | `text-autospace` + progressive `text-spacing-trim`; spacing handled by the engine, **never hand-typed spaces** | W3C clreq |
| Font families | two tiers `--sans` (body) / `--sans-display` (display); display tracking `--track-display:-0.011em`, **zero body tracking** | Linear + clreq |
| 12-step scale | Radix role binding: 1/2 backgrounds · 3/4/5 states · 6/7/8 borders · 9/10 solids · **11/12 text (APCA Lc 60/90 guaranteed)** | Radix docs |
| Tokens | all CSS variables; alpha variants via `color-mix(in oklab,C 12%,transparent)`; OKLCH comments = perceptual coords | Tailwind v4 |
| Contrast dial | `tokens --contrast high` = WCAG 7.0 + Lc 75/90+ (AAA direction) | Linear 3-input |
| Motion | 150/300/600ms; entry stagger 60-120ms, end state = no-motion version | _motionlab |

Principle: **defaults are the product** — these ship as engine output, don't hand-tune; to deviate, change the inputs (`--palette/--contrast/--ratio`), not the artifact.

## Capability × Boundary Quick Reference

| Capability | Does | Does not | Deep dive |
|---|---|---|---|
| Library match/search | Rank an 119-palette evidence library by register + likes tiers + objective gates | Does not judge "subjective beauty" — final verdict is in-context | curation.md |
| Generate harmony / ramp / mutate | OKLCH harmony, luminance ramps, perceptual transforms with auto gamut fit | No illustration or gradient-image export | color-theory.md |
| Extract | Pull dominant colors + shares + readable-text hints from a reference image | No image redraw or matting | — |
| Roles | bg/text/accent/primary/surface + semantic colors, with contrast checks | Not a layout or type-selection system | craft-rules.md |
| Validate score/contrast/blind | 5-dim scorecard, exact WCAG boundaries, three color-blind simulations, fix suggestions on failure | Does not judge taste; contrast is necessary, not sufficient | color-theory.md |
| Anti-pattern slop + lint_page | Median-trap/purple-gradient/flat-lightness detection; HTML delivery audit — **any gradient (linear/radial/conic) is a P0 fail: flat color layering only** | Does not cover every aesthetic failure — five-lens screenshots fill the gap | anti-slop.md |
| Acceptance report | One-shot `report` aggregates contrast / color-blind / AI-slop / scorecard into a single PASS/FAIL JSON (exit code = verdict) for the verdict write-back loop | Not a taste judgment — five-lens screenshots still apply | critique.md |
| Preview card / showcase / make_variants | Palette cards + mockups; named showcase picks; ≥2-candidate comparison | Not a substitute for a real-environment smoke test | critique.md |
| Directions (cross-register) | `directions` renders whole-page candidates from different register families side by side — difference is enforced (distinct palettes, ≥2 style tags apart), each with metadata and a pick-back sentence | Not a taste verdict — the user still picks | curation.md |
| Showcase-grade scene | `scene --kind wallet/landing/dashboard… --theme` renders a showcase-craft single scene (device mockup + evidence badges) as a page starting point; AI-default purple guard built in | Scenes are starts, not finishes — extend, then gate | design-techniques.md |
| Design technique library | `references/design-techniques.md` — 10 composable expressive recipes (grain hero, ghost numerals, marquee, sticky acts, duotone, asymmetric grid, hover reveals) with complete code; pick 3-5 per page and compose | Composition is judged by the same mechanical gates | design-techniques.md |
| Page scaffold | `scaffold --theme` emits the full four-act expressive page skeleton (night hero / dawn works / voice / book) with auto-tuned contrast, grain, reveals — replace marked content, then gate | Content is yours to write; the skeleton is the craft | expressive-design.md |
| Expressive design (stunning) | Dark-act journey, oversized-vs-micro type, grain texture, scroll reveals, single signature — the formula that turns PASS into memorable | Still mechanically gated: contrast/color-blind/slop all apply | expressive-design.md |
| One-shot image check | `check-image` turns a cover/screenshot into palette + four-gate verdict in one command (digest-bound JSON) | Works on extracted colors — it does not judge composition | curation.md |
| Evidence dossier | `evidence` bundles the four mechanical gates + static lint (+ optional render probe) into one PASS/FAIL JSON and a human-readable record; exit code = verdict | Evidence, not taste — five-lens screenshots still apply | critique.md |
| Design tokens | `tokens --palette/--theme` emits a full semantic token sheet (CSS + JSON): color roles auto-tuned to contrast, accent split into graphic/text variants, space/radius/motion scales, measured ratios as comments | Tokens are derived, not decreed — wire them in, then deliver via `report` | curation.md |
| Page audit (existing pages) | `audit page.html --palette` mechanically inspects an existing page: drift with nearest-library replacements, gradient ban, purple-background guard, contrast pairs with tuned fix values, font floor, AI-default signatures | Static scope — external CSS and rendered truth need render probe / evidence | critique.md |
| Chart palettes | `chartpal --kind categorical/sequential/diverging` derives chart colors with three-CVD-simulation distinguishability bounds, monotonic ramps, neutral midpoints — annotated swatch HTML + JSON | Ordered data gets ramps, not categorical colors; group before exceeding 6 series | data-viz.md |
| Type scale | `typescale --base 16 --ratio 1.25` emits a CJK-aware modular ramp (12px floor, line-height pairing, tabular-nums token) as CSS + specimen | Clamped steps are reported, never hidden; scale serves hierarchy | cjk-typography.md |
| Render reconciliation | `qc shot.png --tokens tokens.json` reconciles the rendered pixels against declared tokens: background authenticity, off-palette intrusions with area shares, digest-bound verdict — the mechanical gate of the render feedback loop; `direct --render evidence.json` audits the *rendered* zone colors (probe v2) through the color director | Static checks cannot see rendering; declared ≠ rendered until proven | render-loop.md |
| Typography system | `references/typography-system.md` — display-grade CJK+Latin typesetting law: autospace base, tracking-by-size law, line-height contrast, eyebrow/display/deck recipes, variable-font loading discipline, numeric typography; `typescale --fluid` emits the ramp as fluid clamps plus the typesetting base CSS | Rules are paste-ready code, not prose; progressive-enhancement items degrade safely | cjk-typography.md |
| Layout composition | `references/layout-composition.md` — 12-col base, span vocabulary (no consecutive repeats, 4+4+4 once max), asymmetry ratios 7:5/8:4/5:8, spacing tiers 96/64/40, dark-light act alternation, decoration dosage caps; `scaffold --recipe` emits five parameterized full-page layouts (EDIT-SPLIT / BLUEPRINT / SWISS-POSTER / EDITORIAL-MAG / DARK-FOUR-ACT; default AUTO routes by palette temperament) | Recipes are starts — replace content, then gate | layout-composition.md |
| Motion grammar | `references/motion.md` - entry choreography (stagger 60-120ms, end state = no-motion, pixel-verified), hover feedback (translateY <= 4px + shadow, 150-220ms, scale/rotate banned), scroll-driven (inside @supports only, base state = full feature), dosage caps; audit checks motion_scale_hover / motion_lag | Static screenshots verify end states only; timing comes from rendered experiments | motion.md |
| Typography aesthetics | `references/typography-aesthetics.md` — font temperament spectrum, CJK x Latin pairing table (each pair rendered-verified), fake-bold ban (800/900 without @font-face = FAIL; degradation chain: subset Black > system VF > 700 cap), display-drama rules (ratio 1.414 sweet spot, giant-type trinity), and the --fonts asset pipeline spec | Health rules live in cjk-typography.md; this file decides what looks designed | cjk-typography.md |
| Quantified rationale | `narrate --palette/--theme` turns the measured report gates into a bilingual numbers-only rationale (contrast pair, blind sims, slop scan, score, fingerprint) ready to forward | Every number traces to the report; templates add no adjectives | critique.md |
| Exemplar injection | `exemplar --kind landing --register light` retrieves a render-reviewed, gate-passed exemplar page (five recipes x five boards, kind/register metadata in header) — code to imitate-adapt: swap colors to your declared tokens, replace content with real copy | Exemplars teach structure and dosage; zero-hit retrieval is an explicit error, never a guess | layout-composition.md |
| Targeted patches | `patch page.html --palette ... [--apply]` turns audit findings into literal search/replace pairs (muddy-background tint, font floor, CJK tracking, contrast pairs); `--apply` makes a byte-identical .bak, applies, re-audits | Literal patches apply only where the string truly exists — everything else degrades to manual guidance | render-loop.md |
| Render loop checklist | `loop page.html --palette ...` emits the executable review loop: pre-render gates, full-viewport per-screen screenshot rules, qc reconciliation line, five lenses, stop conditions (max 5 rounds) | Gate-green is not done; the loop is the unit of work, not a single render | render-loop.md |
| Visualizer scenes + SVG recolor | 10 realistic scenes (mobile / landing / dashboard / branding / typography / pattern / chart / product card / email / editorial) with derived roles, legibility gates and a text ladder; SVG recolor via slot inventory (design's own colors mapped by rank, pure black/white kept), `--shuffle N` renders N permutations with a comparison grid | Scene mockups are decision aids, not production UI | critique.md |
| Color-blind safe sets | `matrix` cross-checks every palette pair under three CVD simulations; `semantic --count` emits a CVD-safe categorical set; `themes`/`theme` list and emit the 11 theme packs (palette + voice + signature) | These are palette-level checks — page-level gates are separate | curation.md |
| Learn house + profile.json | Accepted designs join the corpus; preferences (theme/bans/registers) apply mechanically | The learning file IS the config file — see "Verdict write-back" section | curation.md |

**Non-goals**: layout systems, image asset generation, print CMYK gamut, typeface selection — this skill only decides and validates color.

## Six-Step Method

Command variables (set once): `SDIR="<absolute path to this skill dir>"`, `S="$SDIR/scripts/palette_forge.py"`.

### Step 1: Name the aesthetic manifesto

Pick a **1-2 word movement name** + a one-line manifesto: "Herb garden ledger — pot brown, dried-herb green, mulberry-paper cream, all low saturation, sun-bleached". The manifesto includes:
- **Register check** (lens 0): who reads it / in what setting / what they take away in 3 seconds; visual register must match the content domain. **The user's existing aesthetic profile (e.g. light/understated/whitespace/ghost numerals) is the highest-priority constraint — check before writing; a fitting metaphor cannot rescue a register mismatch**;
- **Reference aesthetics**: "1970s ski lodge: burnt orange, avocado green, warm brown";
- **Lightness architecture**: light or dark ground; text is always the extreme;
- **Color dosage**: accent ≤10% of the page — "scarcity is force";
- **Negation list**: pick applicable items from `references/anti-slop.md` into the prompt (inference-time negation works);
- 60-30-10 is a **default scaffold, not law** — proportions follow the brief.

### Step 2: Source (four routes)

```bash
python "$S" match --brief "pediatric clinical teaching page" --limit 6   # A' brief match: auto register + profile down-rank (preferred)
python "$S" search --style warm,pastel --no-flags --limit 6   # A manual filter
python "$S" harmony --base 780000 --mode complementary --theme light  # B OKLCH harmony
python "$S" extract reference.png --n 6                  # C image extraction (needs Pillow)
python "$S" ramp --base 2A9D8F --steps 7                 # D luminance ramp (charts/heatmaps)
```

A' = natural-language brief → register detection + profile down-rank + tier ranking, **the preferred entry for new tasks**. **The spacebar-iteration equivalent**: re-roll seeds/modes/style words; generate ≥2 candidates before moving on. Many candidates → `showcase` renders named picks.

### Step 3: Roles, not a bag of swatches

```bash
python "$S" roles --palette 606C38,283618,FEFAE0,DDA15E,BC6C25 --semantic --css
```

Outputs bg/text/accent/primary/surface + derived semantic colors (success/warning/error/info), with three contrast checks — non-zero exit on failure. Key point: the strongest color **owns one deliberate region**, not scattered accents.

### Step 4: Mechanical validation (measurement vs taste, separated)

```bash
python "$S" score --palette ...     # 5-dim scorecard /20, P0-P3 findings, <10 exits non-zero
python "$S" contrast --fg ... --bg ... [--large]   # single-pair check with fix suggestions
python "$S" blind --palette ...     # three color-blind simulations; mandatory for charts/status colors
python "$S" slop --palette ...      # AI-slop signatures; non-zero exit on hit
```

Charts additionally: distinguish data by luminance ramps only (ramp), redundant encoding via shape/labels, never red+green as the sole distinction.

### Step 5: Export tokens

```bash
python "$S" export --palette ... --format css|tailwind|json|svg|w3c|context   # w3c=设计令牌标准;context=LLM 上下文块
python "$S" mutate --palette ... --shade -20 --sat +5 --hue 15 --temp +30
```

### Step 6: Five-lens self-review (mandatory gate)

```bash
python "$S" card --palette ... --name "Project" --out card.html   # palette card + mockup
python "$S" visualize --palette ... --name "Project" --out viz.html   # 10-scene visualizer; --variants N = same scenes under N palette orders
python "$S" visualize --palette ... --svg design.svg --shuffle 3      # slot-inventory recolor: 3 permutations + comparison grid
python "$S" critique --palette ... [--evidence evidence.json] --out report.md   # 五镜报告生成器(机械发现预填)
python "$S" report --palette ...   # 一键验收: 四闸聚合 PASS/FAIL JSON, 退出码=裁决
python "$S" export --palette ... --format prompt   # 色板→图像生成提示词块(封面/插画管线)
python "$S" doctor                                 # 环境体检
python "$SDIR/scripts/lint_page.py" page.html --palette <declared palette> --floor 12   # delivery audit
```

**Always** screenshot into the conversation and adjudicate with the **five lenses** from `references/critique.md` (intent/register → composition → information → color → type): every PASS/FAIL points at a concrete element + cites a principle + evidence; FAIL unfixed = not delivered; fixes are bounded. Before HTML delivery run lint_page.

Gate chain:

| Step | Tool | Guards |
|---|---|---|
| 1 palette | `score` | 5 dims + profile violations |
| 2 build | any | — |
| 3 HTML discipline | `lint_page` | drift/bans/font floor/dosage |
| 4 render evidence | `render_probe.js` + `lint_page --render` | measured theme/dosage/contrast/font |
| 5 candidates | `make_variants` | ≥2-candidate comparison sheet |
| 6 five-lens screenshots | human + agent | eye order/density/composition |

Render-probe fallback: without browser tooling skip step 4, keep five-lens screenshots as the floor, and note "render evidence not run" in the delivery.

On user rejection, run a **necropsy** first (write the transferable failure mode back to critique.md), then redesign. Formal deliverables follow the host environment's acceptance flow.

## Verdict write-back & customization

- **Accepted-design intake**: `python "$S" house --name "Project final" --hexes ... --from-proj project` — joins the library and gets match-boosted.
- **Register vocabulary**: the built-in register table ships with the engine (medical + frontend families). `profile.json` `registers` stores per-user accent caps and theme overrides that `match` reads; adding a brand-new domain's keywords is a code-level extension, not a config edit — `--register` accepts only built-in names.
- **Self-test**: `python "$S" selftest` — WCAG boundaries/OKLCH round-trip/slop signatures; non-zero exit = engine untrustworthy.

## Reference docs (30-second routing)

| Task | Go to |
|---|---|
| Write negation lists / spot AI-slop | anti-slop.md (ban table + template) |
| Review a rendered page | critique.md (five lenses + verdict format) |
| Harmony rules / contrast formulas / color semantics | color-theory.md |
| Find a named rule fast | craft-rules.md (rule cards) |
| Grow the library / selection methodology | curation.md |
| Harvest more source data | harvest-playbook.md (5 field-tested traps) |

| File | Content |
|---|---|
| `references/critique.md` | Five-lens review + named failure modes + necropsy archive |
| `references/craft-rules.md` | Palette rule cards (five-lens quick reference) |
| `references/color-theory.md` | Harmony rules/OKLCH/lightness architecture/60-30-10/WCAG formulas/semantics |
| `references/anti-slop.md` | AI-slop bans and evidence chain |
| `references/curation.md` | Selection methodology + library-growth pipeline |
| `references/harvest-playbook.md` | source harvesting recipe (5 field-tested traps) |
| `references/responsive.md` | Mobile pass for showcase/landing pages: nav never display:none, auto-height bar, fixed-canvas horizontal gallery, grid min(100%), overflow locating snippet |
| `references/cjk-typography.md` | CJK pages: full font stacks, serif headline rules (no orphan lines, synthesized/real weight), text-autospace/spacing-trim, subset webfont via `scripts/make_cjk_subset.py` |

## Selection methodology

Three filters: ① crowd signal (source-site official charts + likes tiers + cross-page recurrence) ② objective gates (reject only objectively broken: flat lightness / no readable pair; flag CB collisions / slop / narrow lightness) ③ in-context self-review (the final verdict). **Nobody can know "beautiful" a priori** — the library sets the starting line, the context decides. Details in `references/curation.md`.

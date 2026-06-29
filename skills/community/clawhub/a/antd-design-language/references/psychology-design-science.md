# The Design-Science & Psychology Behind the Rules

The "why" toolbox. Ant Design's specs are surface expressions of deeper, well-studied principles.
Use this file to **explain** any antd rule, or to reason about a situation antd doesn't explicitly
cover. Organized: Gestalt → CRAP → UX laws → Norman/Nielsen → cognitive load → color/contrast →
hierarchy & reading → typography. Each entry: **definition → why it works → how antd uses it.**

---

## 1. Gestalt principles (how the brain groups what it sees)

The visual system organizes raw input into wholes *pre-attentively* (before conscious thought). Good
layout offloads work onto this free processing.

| Principle | Definition | Antd expression |
| --- | --- | --- |
| **Proximity** | Near elements are perceived as a group. | Form label↔field grouping; 8px spacing; card padding. |
| **Similarity** | Elements sharing color/shape/size are seen as related. | Repeated component styling; same button shape = same role. |
| **Common Region** | Items inside a shared boundary group together. | `Card`, `Panel`, table row backgrounds, list containers. |
| **Continuity** | The eye follows lines/edges; aligned items read as connected. | The 24-column grid, aligned form fields, baseline alignment. |
| **Closure** | The mind completes incomplete shapes. | Icon glyphs, minimal borders, skeleton screens. |
| **Common Fate** | Things moving together are perceived as one unit. | Coordinated transitions (`Use Transition`), object constancy. |
| **Figure–Ground** | We separate foreground objects from background. | Modals/overlays + shadow; dimmed mask; elevation. |
| **Prägnanz (Simplicity)** | We perceive the simplest possible interpretation. | Restraint: few sizes/weights, clean alignment → "calm." |

**Master idea:** grouping by *space and similarity* is free; grouping by *reading labels* is
expensive. Antd's spacing/grid/repetition push work onto Gestalt perception.

## 2. C.R.A.P. (Robin Williams — applied Gestalt for layout)

Antd's first four design principles **are** C.R.A.P.:

- **Contrast** — if two things differ, make them *clearly* differ (size/weight/color/space). Creates
  hierarchy; avoids "muddy" sameness. → type scale, primary vs default button.
- **Repetition** — repeat visual motifs to unify and teach. → the token system.
- **Alignment** — nothing arbitrary; everything lines up. → 24-col grid.
- **Proximity** — group related, separate unrelated. → 8px rhythm.

## 3. UX laws (heuristics with predictive power)

| Law | What it says | Antd application |
| --- | --- | --- |
| **Hick's Law** | Decision time ↑ with number/complexity of choices. | Progressive disclosure, smart defaults, *one* primary action (`Keep it Lightweight`). |
| **Fitts's Law** | Time to a target ↓ with size, ↑ with distance. | Adequate `controlHeight`/hit areas; actions near their context (`Make it Direct`). |
| **Miller's Law** | Working memory ≈ **7 ± 2** chunks. | Chunked nav, grouped form sections, stepwise wizards. |
| **Jakob's Law** | Users expect your site to work like the others they know. | Conventional patterns; consistency = the **Certainty** value. |
| **Tesler's Law** | Complexity is **conserved** — someone must bear it. | The *system* absorbs complexity (tokens, components) so each product/user doesn't. |
| **Doherty Threshold** | Productivity stays high when response < **400 ms**. | Fast motion (0.1–0.3s), loading/skeleton states (`React Immediately`). |
| **Aesthetic–Usability Effect** | Beautiful UIs are *perceived* as more usable (and tolerate minor flaws). | Polished defaults, consistent spacing/motion build trust. |
| **Von Restorff (Isolation)** | The distinctive item is noticed/remembered. | Brand color reserved for the single primary action; badges/alerts. |
| **Serial Position** | First & last items are best remembered. | Put key nav/actions at the start/end of lists & menus. |
| **Peak–End Rule** | Experiences are judged by their peak & their end. | Strong success/result pages, graceful empty/error states (`Meaningful`). |
| **Zeigarnik Effect** | Unfinished tasks occupy memory. | Progress indicators, step counters, draft/resume, badges. |
| **Goal-Gradient** | Motivation rises closer to the goal. | Steppers/progress that show nearness to completion. |
| **Postel's Law** | Be liberal in what you accept, conservative in what you do. | Forgiving inputs (parse many formats), strict, clear output/validation. |
| **Law of Prägnanz** | We read the simplest form. | Visual restraint; flat, ordered layouts. |

## 4. Norman's principles + Nielsen's heuristics (interaction)

**Don Norman — *The Design of Everyday Things*:**

- **Affordances** — what an object *lets* you do. **Signifiers** — the perceivable cues that
  *advertise* it (antd's hover/focus styles, button shapes = signifiers → `Provide an Invitation`).
- **Mapping** — controls spatially relate to their effects (natural mapping → the **Natural** value).
- **Feedback** — every action gets a visible, timely response (→ `React Immediately`, `Meaningful`).
- **Constraints** — limit possible actions to prevent error (disabled states, masked inputs).
- **Conceptual model** — a coherent story of how the system works; consistency keeps it intact.
- **Gulf of Execution / Evaluation** — the gaps between *intent → action* and *result → understanding*.
  Good design narrows both: clear affordances (execution) + clear feedback (evaluation).

**Nielsen's 10 usability heuristics** (antd touches all): visibility of system status · match between
system & real world · user control & freedom (undo/cancel) · **consistency & standards** · error
prevention · **recognition rather than recall** · flexibility & efficiency (shortcuts) · aesthetic &
minimalist design · help users recover from errors · help & documentation.

## 5. Cognitive load theory (Sweller)

Working memory is tiny and fragile; design should spend it wisely. Three loads:

- **Intrinsic** — inherent task difficulty (can't remove; can *sequence*: wizards, chunking).
- **Extraneous** — load from the *interface itself* (inconsistency, clutter, poor labels). **This is
  what antd attacks** — consistency, tokens, and convention convert extraneous load into automaticity.
- **Germane** — productive load that builds the user's mental model (good onboarding, consistent
  patterns that transfer).

Corollaries antd relies on: **Recognition over recall** (show options, don't make users remember);
**Chunking** (group into ≤7 units); **Progressive disclosure** (reveal complexity on demand —
`Keep it Lightweight`); **Selective attention** (one focal point per screen).

## 6. Color & contrast science

- **Color models:** antd's palette algorithm works in **HSV/HSB** (hue, saturation, value) because
  it matches how we *perceive* brightness/vividness, giving even steps where naive RGB math wouldn't.
- **60-30-10** — a balance ratio: ~60% dominant/neutral, 30% secondary, 10% accent. Antd: lots of
  neutral surface, brand color used *sparingly* (the 10% accent) → the primary action pops
  (**Von Restorff**, **Contrast**).
- **WCAG contrast:** normal text needs **≥ 4.5:1** (AA), large text/UI **≥ 3:1**; **AAA = 7:1**. Antd's
  layered-opacity text + algorithmic palettes are tuned to clear these. Always verify custom brand
  colors.
- **Semantics & culture:** green=success, red=error/danger, gold=warning are learned mappings (and
  partly cultural — note red is positive/festive in Chinese contexts; antd uses red for *error* in
  product UI regardless). Don't encode meaning by **hue alone** — ~8% of men have color-vision
  deficiency; pair color with icon/text/position.

## 7. Visual hierarchy & reading patterns

- **Visual hierarchy** — deliberate ordering of attention via size, weight, color, contrast,
  position, and whitespace. Every screen should answer "where do I look first?" in < 1 second.
- **Reading patterns** — **F-pattern** (text-heavy pages/lists), **Z-pattern** (sparse/landing
  layouts), **layer-cake** (headings + content scanning). Place primary info along these paths;
  put key actions at the start/end (**Serial Position**).
- **Scanning, not reading** — users skim. Front-load labels, use clear headings, keep line lengths
  moderate, and let whitespace chunk content.

## 8. Typography psychology

- **Legibility** (can I distinguish characters) vs **Readability** (can I read comfortably). Base
  14/22 and the system stack optimize both at screen distance.
- **Measure (line length):** ~45–75 characters is comfortable; too long loses the return sweep, too
  short breaks rhythm.
- **Vertical rhythm:** consistent line-heights/spacing (multiples of the 8px base) create a calm,
  scannable cadence (**Repetition** + Gestalt continuity).
- **Tabular numerals:** equal-width digits so figures align in columns — critical for data tables
  (an enterprise/B-side need).

---

## How to use this when explaining or critiquing

State **rule → principle → consequence**:

> "These form fields should share one alignment edge (antd **Alignment**) — it leverages Gestalt
> **continuity** so the eye sweeps the column in one motion, cutting **saccades** and extraneous
> **cognitive load**. Misaligned, each field becomes a separate fixation and the form *feels* harder
> even if it isn't (**Aesthetic–Usability Effect** in reverse)."

That rule→reason→cost chain is the assistant's signature. See `assets/review-checklist.md` to apply
it systematically.

# Ant Design UI Review Checklist

A structured audit for critiquing a screen against Ant Design's language. For each item: the **check**,
the **principle** it enforces, and the **cost** of failing it (cite this when giving feedback). Work
top-down; stop-the-line items are marked ⛔.

> Output format for a review: for every issue, write `Issue → antd principle → psychological cost →
> fix`. Example: *"Two primary buttons in the toolbar → violates Contrast / Von Restorff → user can't
> tell the main action, decision slows (Hick's Law) → demote one to default."*

## 1. Layout & alignment (CRAP · Gestalt)

- [ ] Everything aligns to the **24-col grid** / a shared edge; no arbitrary offsets. — *Alignment /
  continuity; misalignment adds saccades + "messy" feel.*
- [ ] Related controls are **grouped by proximity**; unrelated ones separated. — *Proximity / common
  region; wrong spacing implies wrong relationships.*
- [ ] Spacing uses the **8px rhythm** (4/8/12/16/24/32/48), not random px. — *Repetition; ad-hoc
  spacing = collaboration entropy.*
- [ ] One clear **focal point**; obvious "look here first." — *Visual hierarchy; no hierarchy = read
  everything.*
- [ ] Adequate **whitespace**; screen not cramped despite density. — *Prägnanz; clutter raises load.*

## 2. Color

- [ ] Brand color (`#1677FF`) used **sparingly**, mainly for the **one** primary action per view. ⛔ —
  *Von Restorff / Contrast; overuse destroys the accent.*
- [ ] Status colors are **semantic only** (success/warning/error), not decorative. — *Consistency;
  semantic noise misleads.*
- [ ] Text/background contrast meets **WCAG AA (≥4.5:1)**, UI elements **≥3:1**. ⛔ — *Legibility/
  accessibility.*
- [ ] Meaning never conveyed by **hue alone** (pair with icon/text). — *~8% color-vision deficiency.*
- [ ] Custom colors derived via the **palette algorithm / tokens**, not hand-picked one-offs. —
  *Repetition / Certainty.*

## 3. Typography

- [ ] Body **14/22**; only **3–5 sizes** total on the screen. — *Contrast/hierarchy; too many sizes =
  no scale.*
- [ ] Weights limited to **400/500** (600 rare). — *Restraint; bold overuse flattens hierarchy.*
- [ ] Numbers in tables use **tabular-nums** and align. — *Readability of data (B-side need).*
- [ ] Line length comfortable (~45–75 chars); headings clearly distinct. — *Readability; F-pattern
  scanning.*

## 4. Components & consistency

- [ ] **One component per job**; same pattern used the same way everywhere. — *Certainty / Jakob's
  Law; recognition over recall.*
- [ ] Values come from **tokens** (`useToken`/`ConfigProvider`), not hardcoded hex/px. — *Growing /
  Repetition; hardcoding breaks dark/compact themes.*
- [ ] Radius (6), shadows (subtle, transient surfaces only) consistent with the system. — *Figure–
  ground; loud shadows add noise.*

## 5. Interaction (ease-of-use principles)

- [ ] Main task is **direct** (edit in place where possible). — *Make it Direct / Fitts's Law.*
- [ ] Flows **stay on the page** (modal/drawer/inline vs full reload). — *Stay on the Page; protects
  working memory (Miller).*
- [ ] Primary path is **lightweight**; advanced options progressively disclosed. — *Keep it
  Lightweight / Hick's Law.*
- [ ] Interactive elements **invite** action (hover/focus states, helpful placeholders/empty states).
  — *Provide an Invitation / signifiers.*
- [ ] Targets are large enough and not too far from context. — *Fitts's Law.*

## 6. Feedback & state

- [ ] Every action gets **immediate feedback** (loading/skeleton/optimistic), response < **400 ms**
  perceived. ⛔ — *React Immediately / Doherty Threshold.*
- [ ] State changes **transition** (don't pop) to preserve continuity. — *Use Transition / object
  constancy.*
- [ ] **Empty, loading, and error** states are all designed (not just the happy path). ⛔ —
  *Meaningful; Peak–End; error recovery (Nielsen).*
- [ ] Validation is clear, specific, and forgiving of input format. — *Postel's Law; error
  prevention/recovery.*
- [ ] Long/complete flows show **progress** and resolve open loops. — *Goal-Gradient / Zeigarnik.*

## 7. Accessibility & internationalization

- [ ] Keyboard navigable; visible focus; semantic roles/labels. ⛔ — *Inclusive; control & freedom.*
- [ ] Respects `prefers-reduced-motion`. — *Inclusive motion.*
- [ ] Layout tolerates **text expansion** (i18n) and **CJK** line-breaking. — *Natural; antd's CJK
  strength.*
- [ ] Dark mode handled via `darkAlgorithm`, not ad-hoc colors. — *Certainty / Growing.*

## 8. Density & theme fit

- [ ] If data-dense, consider **compactAlgorithm** rather than shrinking ad hoc. — *Tesler's Law;
  system absorbs density.*
- [ ] The screen's restraint matches enterprise context (not consumer flash). — *Right tool for the
  cognitive/business context.*

---

### Quick triage (if short on time, check these five ⛔)

1. Exactly **one** primary action, in brand color.
2. Text contrast **≥ 4.5:1**.
3. Every action has **immediate feedback**.
4. **Empty/loading/error** states exist.
5. **Keyboard + focus** accessibility works.

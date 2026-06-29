# Ant Design — Values & Principles (with their roots)

Source: Ant Design design spec (ant.design/docs/spec). This file pairs every value/principle with
the **design-science or psychology law** it expresses — that pairing is how you apply them with
judgment instead of by rote. (Deeper definitions of each cited law live in
`psychology-design-science.md`.)

---

## The four design values

Ant Design serves **enterprise / B-side products**. Its meta-goal: maximize **certainty** and
minimize **"collaboration entropy" (协作熵)** — the disorder that accrues when many designers and
engineers make inconsistent micro-decisions. The four values operationalize that goal.

### 1. Natural · 自然

> Interfaces should follow the natural laws of the physical world and human intuition, so users act
> without conscious effort.

- **Means:** sensible defaults, familiar patterns, physically plausible motion, plain language.
- **Why (roots):** **Mental models** & **Jakob's Law** (users expect your product to work like the
  others they know); **affordances/signifiers** (Norman — controls should *look* like what they do);
  **natural mapping** (control layout mirrors real-world relationships). Natural = *don't make the
  user translate.*

### 2. Certain · 确定性

> Consistent, modular rules so designers make fewer arbitrary choices and users never relearn.

- **Means:** one component for one job; tokens over magic numbers; identical patterns across pages,
  terminals, and products.
- **Why (roots):** **Consistency & standards** (Nielsen heuristic); **Jakob's Law**; **cognitive-load
  theory** — consistency converts *extraneous* load into automaticity. This is antd's central value:
  it explicitly frames design as *reducing entropy*, which is an information-theory framing of
  predictability.

### 3. Meaningful · 意义感

> Every screen has a clear purpose and gives the user meaningful, well-timed feedback.

- **Means:** state the goal of each page; acknowledge every action; show progress; end flows on a
  positive, resolved note.
- **Why (roots):** **Feedback** & **visibility of system status** (Norman / Nielsen); **Goal-Gradient
  Effect** (motivation rises near completion → show progress); **Peak–End Rule** (people judge an
  experience by its peak and end → design strong endings); **Zeigarnik Effect** (open loops nag →
  resolve them).

### 4. Growing · 生长性

> Design and product grow together; the system is alive, not a frozen spec.

- **Means:** design tokens & modular components so the system scales; patterns that extend cleanly;
  a feedback loop between product needs and the system.
- **Why (roots):** **Systems thinking / design-tokens** (single source of truth that propagates);
  **Tesler's Law** (complexity is conserved — a growing system absorbs it so each product doesn't
  re-solve it). Growth is why v5 is **token-based**: change a seed, the system re-derives itself.

---

## The ten design principles

The first four are the classic **C.R.A.P.** visual principles (Robin Williams) — which are
themselves applied **Gestalt** psychology. The last six are **interaction** principles (antd's
"易用模式", influenced by *Designing Interfaces* / *Designing Web Interfaces* by Bill Scott & Theresa
Neil). For each: the rule, how antd applies it, and its psychological root.

### Visual (CRAP / Gestalt)

#### 1. Proximity · 亲密性
- **Rule:** items related in meaning should be close; unrelated items spaced apart. Closeness creates
  a single visual unit and reveals page structure.
- **Antd:** form label↔field grouping, card padding, 8px spacing rhythm, list item grouping.
- **Root:** **Gestalt law of Proximity** (+ *Common Region*). The brain groups near things
  pre-attentively → grouping by space costs *zero* conscious effort, unlike reading.

#### 2. Alignment · 对齐
- **Rule:** every element should align to something; invisible alignment lines create order and a
  calm scan path.
- **Antd:** the 24-column grid, left-aligned labels/fields, baseline alignment of text+icons.
- **Root:** **Gestalt Continuity** + **Law of Prägnanz** (the mind prefers simple, ordered
  arrangements). Misalignment forces extra **saccades** (eye jumps) → higher load, "messy" feeling.

#### 3. Contrast · 对比
- **Rule:** make different things *clearly* different — by size, weight, color, space. Contrast
  builds hierarchy and guides the eye to what matters first.
- **Antd:** primary vs default buttons; title vs body type scale; brand color reserved for the one
  primary action per view.
- **Root:** **Visual hierarchy** + **Von Restorff Effect** (the distinct item is remembered/noticed)
  + **figure–ground**. Weak contrast = no hierarchy = the user must read everything to decide.

#### 4. Repetition · 重复
- **Rule:** repeat visual styles (color, type, spacing, component shapes) across the product to unify
  it and aid learning.
- **Antd:** the token system *is* institutionalized repetition; consistent component look everywhere.
- **Root:** **Repetition/Similarity (Gestalt)** + **Jakob's Law** internalized — once learned, a
  repeated pattern is recognized, not re-decoded (**recognition over recall**).

### Interaction (ease-of-use)

#### 5. Make it Direct · 直截了当
- **Rule:** put the control where the work is; edit in place rather than navigating away.
- **Antd:** inline edit, editable tables/cells, in-context actions on hover.
- **Root:** **Direct manipulation** (Shneiderman) + **Fitts's Law** (short travel to the target) +
  reduced **Gulf of Execution** (Norman). Less indirection = less load + fewer errors.

#### 6. Stay on the Page · 足不出户
- **Rule:** avoid jarring full-page reloads/jumps; keep the user's context.
- **Antd:** modals, drawers, inline expand, `Popconfirm`, async updates without navigation.
- **Root:** **Doherty Threshold** & preserving **working memory** — context switches dump the user's
  mental stack (**Miller's Law**, 7±2). Staying put protects that fragile state.

#### 7. Keep it Lightweight · 简化交互
- **Rule:** minimize the steps and the visible options for the *main* path; reveal the rest on demand.
- **Antd:** progressive disclosure (collapse, "more"), smart defaults, one primary action per screen.
- **Root:** **Hick's Law** (decision time grows with the number of options) + **cognitive-load
  theory** + **Tesler's Law** (don't push irreducible complexity onto the user — absorb it).

#### 8. Provide an Invitation · 提供邀请
- **Rule:** *signal* what's possible before and during an action (hover hints, affordant styling,
  empty-state guidance).
- **Antd:** hover/focus states, placeholder & helper text, empty states that say what to do next.
- **Root:** **Signifiers** (Norman) + closing the **Gulf of Execution** + **discoverability**.
  Invitations turn "what can I do here?" into an obvious answer.

#### 9. Use Transition · 巧用过渡
- **Rule:** animate state changes so the user can follow *what changed and where it went*. Motion is
  explanatory, not decorative.
- **Antd:** enter/leave transitions, motion that respects spatial origin, ~natural easing.
- **Root:** **Object constancy** & **Gestalt Common Fate**; transitions preserve continuity so the
  brain tracks one object instead of perceiving a jarring replace. Ties to the **Aesthetic–Usability
  Effect**.

#### 10. React Immediately · 即时反应
- **Rule:** respond to input instantly — even an optimistic/loading state — so the system feels alive.
- **Antd:** button loading states, skeletons, instant validation, optimistic UI.
- **Root:** **Doherty Threshold** (keep response < **400 ms** to maintain flow & productivity) +
  **feedback/visibility of status**. Latency without acknowledgment breaks the sense of agency.

---

## Applying this in practice

When you design or review with antd, run two passes:

1. **Visual pass (CRAP):** Is everything *aligned*? Are related things *close* and unrelated things
   *apart*? Is there real *contrast* for hierarchy? Are styles *repeated* consistently (use tokens)?
2. **Interaction pass (ease-of-use):** Is the main task *direct* and *lightweight*? Does it keep the
   user *on the page*, *invite* the next action, *transition* state changes, and *react immediately*?

For each finding, name the principle **and** its root law — see `assets/review-checklist.md` for a
structured audit, and `psychology-design-science.md` for the law definitions.

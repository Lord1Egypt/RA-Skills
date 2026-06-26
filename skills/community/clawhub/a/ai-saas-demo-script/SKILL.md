---
name: ai-saas-demo-script
description: Create concise, conversion-oriented demo video scripts and shot-by-shot storyboards for AI SaaS products. Use when the user asks for a product demo video script, SaaS launch video, AI feature walkthrough, Remotion timeline, motion storyboard, product explainer based on UI/workflows, or wants to generalize/analyze a demo video into a reusable AI SaaS script structure.
---

# AI SaaS Demo Script

## Purpose

Use this skill to turn an AI SaaS product, feature, or workflow into a short product demo video script. Favor proof through workflow over abstract claims: show the user's input, the AI transformation, the human review/control step, and the completed outcome.

Default to a 45-60 second hero/demo video unless the user asks for another length.

## Core Narrative

Build around this transformation:

```text
manual/friction-heavy workflow
-> product appears
-> user provides input
-> AI extracts/generates/prepares output
-> user reviews or approves
-> final result happens
-> value props and brand close
```

The demo should feel like a complete workflow, not a feature inventory.

## Script Formula

Use this generic structure and replace bracketed parts with product-specific details:

```text
Still manually [doing painful task]?

Meet [Product]
[AI-powered / automated / secure] [category]

Send / upload / connect [input]
to [simple destination or workspace]

It extracts / analyzes / creates / prepares [key output]
And seconds later...

Time for a quick check
Review [AI-generated draft/result]
Approve / confirm / send / publish

[Success state]

Save time.
Avoid errors.
Stay in control.

[Brand]
```

Keep on-screen text short. Prefer 2-7 words per beat. Avoid paragraphs unless the deliverable is a voiceover script.

## Timing Template

For a 48-60 second video:

| Time | Section | Goal |
|---|---|---|
| 0-5s | Pain hook | Name the manual workflow or urgent friction. |
| 5-8s | Product reveal | Introduce product name and one-line category. |
| 8-15s | Input | Show the simplest user action: send, upload, connect, ask, or import. |
| 15-22s | AI transformation | Visualize extraction, generation, scoring, matching, or drafting. |
| 22-27s | Time bridge | Use a short beat like "Seconds later..." or "Ready to review." |
| 27-35s | Review | Show the AI-prepared result inside product UI. |
| 35-41s | Approval/action | Show human control: approve, send, publish, invite, confirm. |
| 41-48s | Success | Show final state, status change, or completed task. |
| 48-60s | Value + brand | Summarize 2-3 value props and close with brand/CTA. |

For 30 seconds, remove the separate time bridge and compress review + approval into one beat.

## Reference Selection

Load only the reference needed for the task:

- For shot language, camera movement, pacing, and user-flow movement, read [references/motion-and-camera.md](references/motion-and-camera.md).
- For scene transition types and storyboard transition wording, read [references/scene-transitions.md](references/scene-transitions.md).
- For Remotion parameters, easing, Smart Zoom, cursor/pointer behavior, and frame timing, read [references/remotion-parameters.md](references/remotion-parameters.md).
- For dashboards, KPIs, charts, data animation, and before/after proof, read [references/data-and-comparison.md](references/data-and-comparison.md).
- For frame-by-frame study of a fintech SaaS reference video and translating that motion language into a new product demo, read [references/fintech-shot-study.md](references/fintech-shot-study.md).
- For implementing or reviewing Remotion code-layered product UI, focus precision, overlay safety, and key-frame QA, read [references/remotion-layered-ui-checklist.md](references/remotion-layered-ui-checklist.md).
- For real-product Remotion demos where UI fidelity matters, use screenshot/backplate overlays, native coordinates, pointer/focus lifecycles, and QA frames from [references/real-ui-backplate-remotion.md](references/real-ui-backplate-remotion.md).
- For turning a real website, product URL, or local HTML app into a video pipeline with capture, product analysis, storyboard, composition, snapshot QA, and render steps, read [references/website-to-video-pipeline.md](references/website-to-video-pipeline.md).
- For lessons learned from the different. fintech demo project, including HyperFrames-style motion, real UI fidelity, logo/assets, Insights charts, and render-performance fixes, read [references/real-project-different-lessons.md](references/real-project-different-lessons.md).

If the user asks for a complete motion storyboard or Remotion-ready plan, read all references.

## Copy Rules

Write copy as outcome-led UI captions:

- Start with a concrete manual pain, not a generic "AI is changing everything" claim.
- Say what the user does in plain verbs: send, upload, connect, ask, review, approve.
- Say what the AI creates in product terms: draft, summary, payment, report, insight, ticket, forecast, recommendation.
- Include a control beat for B2B trust: review, approve, edit, or confirm.
- End with 2-3 benefits maximum. Strong defaults: "Save time", "Avoid errors", "Stay in control".
- Prefer visible result text over broad claims: "Report ready" beats "Boost productivity".

## Layout Design: Five Principles

Use these rules when turning a SaaS workflow into a storyboard or Remotion UI:

1. Hierarchy first: one primary focal element per shot. Size, color, brightness, and motion should make the active step obvious before the viewer reads details.
2. Alignment and grid: place product screens, captions, KPI cards, and callouts on a consistent grid. Avoid drifting focus boxes; when possible, wrap real UI layers instead of drawing rectangles over screenshots.
3. Proximity and grouping: keep related controls, labels, metrics, and explanations visually close. Put supporting callouts outside the product screen when they are not part of the product UI.
4. Contrast and emphasis: use high contrast only for the current action or result. De-emphasize background UI with opacity, scale, or blur instead of adding competing highlights.
5. Spacing and breathing room: leave enough empty space around captions, cards, and focus states. Do not stack overlay cards on top of readable product content; if the UI is dense, zoom, pan, or split the layer.

For product demos, prefer code-layered UI mockups when focus precision matters. Screenshots are acceptable for broad context, but buttons, cards, charts, cursors, and focus states should be separate layers whenever they need animation or exact highlighting.

## UI Motion Polish Rules

Use these rules when turning storyboard beats into product UI motion. Treat animation as product feedback, not decoration.

Before adding motion, ask whether it clarifies state, guides attention, confirms an action, explains AI processing, or prevents a jarring change. If none apply, remove it. Avoid animation on high-frequency keyboard actions and repeated navigation; use motion for occasional product moments such as modals, drawers, generated cards, review panels, approvals, and success states.

Use responsive timing and purposeful easing:

| Motion type | Timing | Easing |
|---|---:|---|
| Micro feedback | 80-150ms | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Button/toggle response | 120-180ms | ease-out |
| Tooltip/popover/dropdown | 125-250ms | ease-out from trigger |
| Card/review panel enter | 200-350ms | ease-out or premium ease |
| Page/state transition | 400-600ms | ease-in-out |
| Data reveal | 600-1200ms | linear or ease-in-out by data type |

Avoid `ease-in` for UI entrances because it delays the exact moment viewers expect feedback. Keep most functional UI animation under 300ms unless the shot is explanatory, data-driven, or a deliberate product reveal.

Preserve product-native interaction details:

- Buttons, tabs, approval controls, send controls, and toggles should show immediate press feedback, such as `scale(0.97)`, before the result state appears.
- Popovers, dropdowns, menus, and tooltips should animate from their trigger. Centered modals are the exception and can keep a centered transform origin.
- Product cards, generated drafts, approval panels, and popovers should not enter from `scale(0)`. Use `scale(0.95)` or higher plus opacity.
- Prefer animating `transform` and `opacity`. Avoid `transition: all` and layout-heavy animation unless the workflow state requires it.
- Prefer transitions for dynamic UI that can be interrupted or retargeted, such as toasts, selected rows, filters, drawers, and review panels. Use keyframes for predetermined explanatory sequences.
- Freeze dense background UI when animating the workflow artifact. Avoid heavy blur, stacked translucent overlays, and decorative motion over readable product content.
- Respect reduced motion by removing large transform-based movement while preserving helpful opacity, color, and status transitions.

## Real UI Fidelity Ladder

Use this ladder before implementing a demo from a real product:

1. Real UI proof first: capture or load real product screens for every key page before rebuilding anything. Use screenshots, DOM captures, exported assets, or local HTML renders as the visual truth.
2. Backplate when fidelity is risky: if a code recreation does not match spacing, typography, table density, sidebar state, chart layout, or product cards closely enough, use the real UI screenshot as a backplate and animate only the functional overlays.
3. Layer only the moving parts: rebuild or overlay only the elements that need motion, such as cursor, focus ring, typed input, selected row, carried card, data ribbon, animated chart line, toast, approval check, or generated artifact.
4. Full code recreation only after matching: rebuild a whole screen in code only when it already matches the real product's layout and hierarchy, or when the real product UI is unavailable.
5. Never trade fidelity for polish: a smooth but inaccurate UI is worse than a simpler animation on top of the real product screen.

For real product demos, default to a hybrid approach:

```text
real product screenshot/backplate
+ code cursor/focus/action overlays
+ code-generated data or carry artifacts only where they show state change
+ minimal caption lane outside the active UI
```

Use code recreation for reusable future systems, but verify it against the real screen before using it in a finished demo.

## Real Project Lessons

Apply these rules when turning a real product UI into a finished demo:

- Prefer layered UI reconstruction over screenshot-only animation when the demo needs precise focus boxes, cursor actions, data animation, or UI state changes.
- Bind highlights to the same layout constants/components as the UI element. Do not draw approximate rectangles over screenshots unless the shot is only broad context.
- Use foreground cards only when they represent a real product action: selected row, generated document, extracted result, approval step, or completed status. Do not let them cover the next piece of readable product content.
- Camera motion must have a target. A perspective tilt, angled screen, or push-in is useful only when the camera is moving toward a meaningful UI area.
- Avoid decorative light sweeps as generic transitions. A scan/glow is allowed only when it explains AI processing, extraction, or status progress.
- Every product shot should include either an operation, a data change, a generated artifact, a review/control moment, or a visible result state.
- Treat brand assets as product proof. Use the real logo mark, typography, colors, and product vocabulary when available; do not substitute generic gradient placeholders for recognizable assets.
- Make important analytics a main product scene, not a small decorative badge. If a real product has a dedicated dashboard or Insights page, let the data occupy the primary frame and animate it in a readable order.
- Reserve a caption lane before animating the product UI. Captions should sit in side whitespace or an intentional text zone, not over the primary operation, chart, or table.
- Use HyperFrames-style foreground carry for workflow artifacts: selected rows, result cards, generated files, matched segments, and approval cards can lift forward, travel, and hand the viewer into the next state.
- Keep foreground carry cards opaque and readable. Translucent cards over dense UI often create text bleed and should be avoided unless the background is intentionally blurred/dimmed.
- Real UI fidelity beats decorative polish. Rebuild journey bars, tables, charts, sidebars, and cards to match the product's actual hierarchy, spacing, labels, and active states before adding extra motion.
- For line charts, reserve a left axis gutter and a right terminal gutter. Start the plotted line after the Y-axis labels and keep the final point near, not past, the last month label to avoid both collisions and empty space.
- Cursor, pointer, and focus states must share the same target coordinates. If the cursor clicks one element and the highlight surrounds another, remove the highlight or bind both to the same component constants.
- In Remotion, store pointer coordinates as the intended click target, not the cursor asset's top-left corner. Let the pointer component subtract the arrow-tip offset internally.
- Pipeline and close scenes should still carry workflow proof. A recommendation row can lift into a foreground approval card, then resolve into an approved/completed status card before the brand close.
- Motion-design personality for B2B AI SaaS demos should usually be Corporate with Premium accents: clean, professional, mostly `cubic-bezier(0.2,0,0,1)` or `cubic-bezier(0.4,0,0.2,1)`, with only 0-5% overshoot on tactile cards or success feedback.
- For UI entrances, prefer a stronger ease-out such as `cubic-bezier(0.23, 1, 0.32, 1)`. For on-screen movement or morphing, prefer an ease-in-out such as `cubic-bezier(0.77, 0, 0.175, 1)`. Avoid `ease-in` for UI entrances.
- Use a duration palette: micro feedback 80-150ms, button/toggle response 120-180ms, card enter 200-350ms, page/state transition 400-600ms, data reveal 600-1200ms.
- Build motion as setup -> action -> resolution. Example: cursor hover/press -> row lifts or card carries -> check/status resolves.
- Show tactile input before showing outcome: cursor hover/click or touch press -> button compresses -> action resolves -> success/status appears.
- Use three layers only when each serves the story: primary workflow object, secondary shadow/icon/content follow-through 50-150ms later, and ambient background motion kept subtle.
- For multi-element scenes, stagger in reading order. Use 40-60ms for list/table rows, 50-80ms for cards, and keep total stagger under 500ms.
- Never animate more than roughly one third of visible elements at the same time. If the scene feels busy, freeze background UI and animate only the workflow artifact.
- Success states should not just appear. Use container scale 0.9 -> 1.0 with a light 3-5% overshoot, then draw/pop the checkmark 100-150ms later, total 300-500ms.
- Popovers, dropdowns, menus, and tooltips should reveal from their trigger point. Centered modals can animate from center.
- Avoid product elements entering from `scale(0)`. Use `scale(0.95)` plus opacity for generated cards, menus, panels, and popovers.
- Avoid `transition: all`; specify properties. Prefer `transform` and `opacity` for motion, especially over dense tables and dashboards.
- Gate hover-only effects for pointer devices and account for reduced-motion preferences when implementing real UI or Remotion-adjacent web demos.
- When a real product project exposes UI labels in source HTML or app code, mirror the product vocabulary exactly before polishing motion. In the different. demo, journey labels had to match `Prospecting`, `Onboarding`, `Needs Matching`, `Proposal Push`, and `Post-invest`.
- For precision scenes, define a target as a rectangle and derive the pointer target and focus outline from that same rectangle. Avoid maintaining separate cursor and selection-box coordinates.
- For analytics scenes, use a primary full-size data surface. Reserve chart gutters for axis labels and the terminal point, then resolve the animation into an integrated result strip/ribbon instead of a small detached popover.
- After any UI fidelity or motion-system pass, render stills for at least Search, Data, Segment, and Pipeline. Check cursor/box alignment, title collisions, chart whitespace, logo fidelity, and whether the active element is fully framed.
- If a code-recreated UI still visibly differs from the real product after one correction pass, switch to a real screenshot/backplate plus code overlays instead of continuing to approximate the full interface.
- Pointer visibility needs a lifecycle. Show the cursor before the action, click, then fade it out within roughly 0.4-0.7s unless it is deliberately moving to the next target. A stale cursor near an old target is perceived as a focus error.
- Focus visibility also needs a lifecycle. A focus box should enter with the action, hold only while that target is being discussed, then fade before the next target appears. Avoid two unrelated focus cues on screen at the same time.
- For screenshots/backplates, store overlay coordinates in the native screenshot coordinate system. Avoid mixing native screenshot coordinates with transformed container coordinates unless the transform is centralized and tested.
- Captions must never sit on top of the clicked UI, selected row, chart line, table labels, or active card. If the real UI is dense, use a small bottom or side caption lane with a semi-opaque background and short text.
- A QA still that looks correct while paused is not enough for pointer scenes. Also check a mid-action frame after the click to ensure the cursor has faded or is moving toward the next target.

Use this self-check after rendering key frames:

```text
Is the focus box attached to the real target?
Does any overlay cover required UI text or data?
Does the camera move toward the active action?
Does the caption have its own lane away from the product operation?
Does any foreground carry card come from a real workflow artifact?
Are foreground cards opaque enough to prevent underlying text bleed?
Do chart gutters prevent axis-label collisions and terminal empty space?
Do cursor, pointer, and focus states land on the same UI target?
Is the pointer coordinate a target point rather than an SVG top-left guess?
Does the Pipeline/Close sequence show an approved or completed workflow artifact before benefits?
Is the project motion personality consistent: Corporate/Premium, not playful unless explicitly intended?
Does each major motion beat have setup, action, and resolution?
Does the visible press feedback happen before the result state appears?
Do popovers, dropdowns, and tooltips animate from their trigger rather than from the center?
Do generated cards and panels avoid `scale(0)` entrances?
Are motion properties limited mostly to transform and opacity?
Are high-frequency keyboard or repeated navigation actions left instant or nearly instant?
Are card/icon follow-through elements delayed 50-150ms instead of moving all at once?
Does every stagger finish within 500ms?
Are success checks animated as feedback rather than static decorations?
Would the shot still make sense if the decorative effects were removed?
Is the product value proven by a state change, not just a caption?
Are real brand/product assets used where available?
If this is a data scene, is it a main readable product state rather than a small floating widget?
Are real product labels copied from source UI where available?
Do focus boxes and pointer positions come from one shared target definition?
Does the chart reserve enough gutter for axis labels and terminal points?
Did you render representative stills after the pass, not only rely on code inspection?
If the code UI differs from the real product, did you switch to a real screenshot/backplate?
Does the pointer fade out after click, or is it stale near a previous target?
Does each focus box fade before the next unrelated target appears?
Are overlay coordinates in the same coordinate system as the screenshot/backplate?
Does the caption avoid the active UI, selected row, and chart labels?
Did you check a mid-action frame, not only the settled frame?
```

## Output Formats

When asked for a script, return:

1. **Concept**: one sentence.
2. **On-screen script**: exact text by section.
3. **Shot-by-shot storyboard**: time, visual, text, motion, purpose.
4. **Voiceover** if requested; otherwise omit it.
5. **Motion parameters** when the output will become animation or Remotion code.
6. **Remotion timeline** if relevant.
7. **UI polish review** when reviewing an existing storyboard, Remotion implementation, or UI motion.

Use this storyboard table:

| Time | Visual | On-screen text | Motion/transition | Purpose |
|---|---|---|---|---|

Use this Remotion section format:

```text
PainPointIntro        0.0-5.0s
ProductReveal         5.0-8.0s
InputScene            8.0-15.0s
AITransformScene      15.0-22.0s
ReviewScene           22.0-34.0s
ApprovalScene         34.0-41.0s
SuccessScene          41.0-48.0s
ValueOutro            48.0-56.0s
BrandEndCard          56.0-60.0s
```

When reviewing UI motion or storyboard polish, use this table:

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 180ms ease-out, opacity 180ms ease-out` | Exact properties improve performance and make the motion predictable |
| Popover scales from center | Popover reveals from the trigger point | Anchored UI should preserve spatial continuity |
| Approval result appears instantly | Cursor click -> button compresses -> success appears | Setup, action, and resolution make the workflow believable |

## Quality Checklist

Before finalizing, check:

- The viewer can understand the workflow without reading dense UI text.
- The camera moves through a coherent user path instead of jumping between disconnected screens.
- Every shot has a clear attention target.
- Smart Zoom keeps the active element centered and usually stays within `1.2x-1.8x`.
- Cursor movement establishes intent before UI state changes and does not cover key readable content.
- Pressable controls show immediate feedback before success or completion states appear.
- The AI capability is shown through a before/after transformation.
- Data animation reveals change progressively and highlights one main insight at a time.
- Before/after scenes prove a specific improvement with a visible delta, not just a prettier after state.
- The script includes a human control moment.
- Every scene advances the workflow or reinforces the final value.
- Each transition maps to a product state change or narrative beat.
- Functional UI motion uses responsive easing and avoids `ease-in` entrances.
- Popovers, dropdowns, menus, and tooltips reveal from their trigger; centered modals remain centered.
- The pacing has contrast: key features and results hold longer than setup or navigation.
- The result state is specific and visible.
- The ending has no more than three benefits.
- The video can be executed with product UI mockups, not only abstract animation.
- Highlights, overlays, and cursor positions are checked on rendered frames, not just trusted from code.
- Decorative sweeps, static perspective, and generic glow effects are removed unless they explain a product state.
- Real logos and key product assets are used when provided, instead of approximated with code.
- Real product UI fidelity is checked against captured screens, not just labels or approximate layout.
- If code-layered UI cannot match the real product quickly, the demo uses real screenshots/backplates with code overlays for motion.
- Data dashboards have chart gutters, axis spacing, terminal-point spacing, and tooltips checked in rendered frames.
- Cursor and focus overlays have lifecycle timing: enter, click/hold, fade out before the next target.
- Captions sit in a deliberate lane and do not cover the active UI operation.
- Product UI animation uses `transform` and `opacity` where possible, avoids `transition: all`, and does not animate dense layout unnecessarily.
- Generated cards, panels, popovers, and menus avoid `scale(0)` entrances.
- Reduced-motion behavior is considered when implementing web or Remotion-adjacent interactive demos.
- Heavy filters, stacked translucent layers, and oversized SVG effects are removed if playback flashes, stutters, or renders slowly.
- If implemented in Remotion, the layered UI passes the component, motion, and rendered-frame checks in `remotion-layered-ui-checklist.md`.

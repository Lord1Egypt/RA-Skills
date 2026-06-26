# Motion and Camera Rules

Use these rules when creating shot-by-shot storyboards, camera direction, user-flow movement, and motion descriptions for AI SaaS product demos.

## Shot Language

Use clean, high-contrast shots with one dominant idea per scene:

- **Pain hook**: Abstract UI fragments, floating cards, or blurred workflow states. Keep brand subtle.
- **Product reveal**: Logo centered, small category descriptor, restrained glow or simple scale-in.
- **Input scene**: Realistic product-adjacent UI: inbox, dashboard, chat, file upload, CRM, docs, table, or API event.
- **AI transformation**: Animate data leaving the input and becoming structured cards, highlighted fields, suggestions, drafts, or ranked options.
- **Review scene**: Show a credible UI screen with prefilled fields or generated output. Use cursor movement to guide attention.
- **Approval scene**: Use a button click, toggle, status badge, or approver list to prove human control.
- **Success scene**: Use an unmistakable status: "Sent", "Published", "Approved", "Resolved", "Ready", or "Completed".
- **Outro**: Use short value props, then logo. Do not add new feature claims in the outro.

## Camera Transformation Workflow

Design the demo as guided camera movement through a user flow. Prefer zoom, pan, morph, focus, or masked movement over abrupt hard cuts unless a hard cut clearly improves pacing.

| Step | Goal | Common camera/transition language |
|---|---|---|
| Establish | Build global understanding: what product/context is this? | Full dashboard or home view, slight zoom-in, logo/product name fade-in. |
| Focus | Pull attention to the key feature or entry point. | Zoom into element, dim or blur background, glow/outline/spotlight on the target. |
| Dive-in | Enter the function from its visible entry point. | Card-to-page morph, click-to-expand, scale + fade, zoom-through. Keep element positions continuous. |
| Flow | Show how the feature is used. | Follow cursor, pan across steps, stagger UI states, step-by-step pacing. |
| Feedback | Show what changed or completed. | Checkmark, toast, status badge, number change, chart growth, generated result appearing. |
| Highlight / Loop | Reinforce the core value and return to a bigger picture. | Zoom out to full workflow, quick feature carousel with motion continuity, slogan/CTA/logo. |

Default attention rule: every shot should answer "where should the viewer look now?"

## Motion Rules

- Pair each text beat with a product action within 0.5-1.5 seconds.
- Use cards, panels, and cursor movements as continuity anchors across transitions.
- Move the viewer through the interface rather than cutting randomly between disconnected screens.
- Use dark backgrounds for complexity/AI processing and light backgrounds for clarity/review/outcome when appropriate.
- Let the result state hold longer than setup beats so the viewer can read the payoff.
- Use glow, scan lines, outlines, and progress rings sparingly; they should point to the AI action, not decorate every scene.
- Keep most transitions simple: opacity, blur, scale, slide, card morph, or match cut.
- Avoid showing too many UI fields at once. Highlight only the field or action the viewer must understand.
- Do not use static perspective or an angled product screen unless the camera is actively pushing, panning, or orbiting toward a focal UI action.
- A camera move must have a destination: active row, input, CTA, generated card, KPI, approval status, or success state.
- If a shot is mostly reading, keep the camera calm: slow push or no movement, no rotation, no decorative sweep.
- Use foreground lift-outs for real workflow objects only, such as a selected table row becoming a card or a generated document preview leaving the UI.

Use this rhythm formula:

```text
browse fast -> focus slow -> operate medium -> result slow -> switch fast
```

Practical timing at 30fps:

- Page or section switch: 9-12 frames.
- Click microinteraction: 6-8 frames.
- Feature comprehension hold: 45-60 frames.
- Result feedback hold: 30-45 frames.
- Key value statement: 45-75 frames.

## Fintech SaaS Product-Film Pattern

When matching polished fintech SaaS reference videos, favor this pattern:

| Beat | Visual treatment | Why it works |
|---|---|---|
| Wide product context | Full UI, subtle push, active area already visible | Establishes credibility without overexplaining. |
| Cursor-led action | Pointer arrives before the UI changes; button/card reacts | Makes the workflow feel real and causal. |
| Foreground object | Row, file, or result card lifts out while background softens | Converts a dense UI into one readable story object. |
| Processing proof | Fields highlight, numbers count, status steps complete | Shows what the AI did instead of claiming it. |
| Human control | Approval, review, edit, or send action gets a slower beat | Builds trust for B2B/finance demos. |
| Result hold | Final status or KPI stays still long enough to read | Lets the value land. |

Avoid these anti-patterns:

- Static angled UI with no camera progression.
- Sweeps or glows that do not reveal data, extraction, or status.
- Focus boxes floating independently from the UI layout.
- Overlay cards stacked over dense product text.
- Captions explaining features while the product screen shows no matching operation.

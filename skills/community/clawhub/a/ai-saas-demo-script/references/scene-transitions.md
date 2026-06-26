# Scene Transitions

Use this reference when designing shot transitions, storyboard transition language, or motion logic between product demo scenes.

Make transitions explain progress through the workflow. Choose the transition based on what changes in the product story:

| Transition | Use when | How to describe it in a storyboard |
|---|---|---|
| Text-to-UI reveal | A claim needs immediate product proof. | "Caption fades as the product UI slides in behind it." |
| Match cut | The same object continues across scenes, such as file -> card -> draft. | "Invoice card keeps its screen position while the background swaps to the product dashboard." |
| Card morph | Unstructured input becomes structured output. | "Uploaded file expands and morphs into structured field cards." |
| Cursor-led cut | A user action triggers the next state. | "Cursor clicks primary button; cut on click to the generated result." |
| Status-change cut | The product moves from draft/pending to approved/sent/resolved. | "Status badge flips from Draft to Approved, then cuts to final success state." |
| Light/dark contrast cut | The story moves from complexity/processing to clarity/outcome. | "Dark processing scene wipes to a bright review screen." |
| Processing scan | AI extraction or status progress needs to be visible but brief. | "A restrained scan line passes over the card, revealing extracted fields." |
| Camera push/pull | Move from overview to detail or detail back to value. | "Slow push into the relevant field, then pull back to show the whole completed workflow." |
| Zoom transition | Move from global UI to one function or from a page to a specific button/card. | "Camera pushes from the full dashboard into the highlighted automation card." |
| Pan transition | Show multiple steps or modules in the same product space. | "Camera pans horizontally across the workflow columns as each step completes." |
| Focus transition | Direct attention to a critical feature without leaving the current screen. | "Background dims and blurs while the recommendation panel receives a soft outline." |
| Masked transition | Hide a cut behind a moving panel, cursor, modal, or foreground card. | "The expanding modal briefly fills frame and reveals the detailed page underneath." |
| Foreground carry | A selected row, file, or generated result should connect two screens. | "The selected client card lifts forward, then lands as the header object in the analysis screen." |
| Hold/fade | The result or brand needs time to register. | "Success state holds for one beat, then gently fades to brand end card." |

## Transition Rules

- Attach every transition to a product logic step: input, extraction, draft, review, approval, or success.
- Cut on action when possible: click, upload, send, approve, status flip, or field highlight.
- Use 6-12 frame micro-transitions for UI actions and 12-24 frame transitions for scene changes at 30fps.
- Preserve a visual anchor across cuts when the workflow might feel abstract, such as the same card, file, cursor, or status badge.
- Use a quiet transition before important reading moments. Do not animate the camera aggressively while the viewer must read text.
- Avoid stacking more than two transition effects at once. For example, do not combine heavy blur, scale, rotation, glow, and wipe on the same cut.
- Treat the success transition as the emotional peak: make it clearer and slightly longer than earlier UI transitions.
- Give each transition a reason. If the viewer cannot explain why the camera moved, simplify it.
- Do not use glow, sweep, or flash as a generic scene transition. Use processing scans only when something is being extracted, generated, verified, or completed.
- Do not use perspective/tilt as a transition by itself. Pair any angled view with an actual camera push/pan toward a UI target, or keep the interface flat.
- Check focus transitions on rendered frames. If the box is not precisely attached to the target component, rebuild the target as a layer or remove the box.

## Default Transition Map

```text
Pain hook -> Product reveal: dark text fade + logo scale-in
Product reveal -> Input scene: text fades as UI slides/pushes in
Input scene -> AI transformation: file/card lifts from UI and morphs into structured output
AI transformation -> Review scene: foreground carry or match cut from output card into product dashboard
Review scene -> Approval/action: cursor-led cut on button click
Approval/action -> Success: status-change cut or progress ring to checkmark
Success -> Value outro: hold, then bright fade or clean wipe
Value outro -> Brand end card: logo assemble or simple fade
```

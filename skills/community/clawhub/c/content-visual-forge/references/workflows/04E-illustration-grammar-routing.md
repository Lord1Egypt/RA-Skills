# Workflow 04E · Illustration Grammar Routing

Run this optional workflow after Content Analysis and before page script or image prompt generation.

## Trigger

Enable illustration grammar when:

- The user asks for illustration-style output, article illustrations, inline images, visual metaphors, or high-quality generated pictures.
- `wechat-inline-image` needs atmosphere, section breaks, or essay visuals.
- `social-card` or `knowledge-carousel` needs a stronger visual narrative than icon cards.
- The user provides external samples to borrow image quality or illustration consistency.

Do not enable it just because the user says "make it beautiful" if the task is mostly exact text, screenshots, tables, or engineering rendering.

## Required Inputs

- Source Lock
- output_mode
- execution_mode
- content analysis or content compression ladder
- platform specs when the output is platform-bound

## Decisions

### 1. Choose illustration intensity

- `none`: no illustration layer; use normal layout or render data.
- `accent`: small supporting illustration, icons, or margin visual.
- `scene`: one dominant scene per page with low text.
- `sequence`: several pages share recurring visual subjects and scene rhythm.

### 2. Build the grammar

Declare a compact grammar:

- scene family
- recurring subject or object family
- composition rules
- line and texture rules
- palette and contrast rules
- text-load ceiling
- blocked mimicry

### 3. Attach per-page shot list

Each image or page gets:

- scene_role
- subject_focus
- camera_distance
- composition_axis
- motion_state
- environment_density
- text_load
- source_anchor
- prompt_style_phrase

## Output

Return:

- illustration_grammar.enabled
- illustration_grammar.intensity
- illustration_grammar.scene_family
- illustration_grammar.recurring_subjects
- illustration_grammar.visual_tokens
- illustration_grammar.blocked_mimicry
- illustration_shot_list[]

## Boundaries

- This workflow does not replace Source Lock.
- This workflow does not authorize copying external style, characters, prompts, templates, assets, or visual signature.
- If exact Chinese text is important, route text to engineering rendering or post-layout.

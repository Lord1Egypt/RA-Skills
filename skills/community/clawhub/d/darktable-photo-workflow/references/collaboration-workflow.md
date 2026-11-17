# Darktable collaboration workflow

Use this loop for photo analysis and editing advice. The user prefers restrained post-processing and a complete executable Round 02 rather than a drip-fed tutorial.

## Round 00 — input audit

Inspect automatically before asking questions:

- file type, dimensions, embedded profile, and available EXIF;
- whether the image appears to be a RAW, exported rendering, screenshot, or already processed derivative;
- what can be observed directly and what needs RAW data, scopes, history, or a screenshot;
- the installed Darktable version, UI language, active tone mapper, and current history when visible.

Ask only when a missing fact would materially change the analysis or instructions. Otherwise state a labeled assumption.

## Round 01 — diagnosis and direction

Present these sections in this order.

### 1. Evidence note

Separate:

- `可见事实 / Visible facts`: metadata and directly visible properties;
- `分析判断 / Judgments`: technical, compositional, color, commercial, and artistic evaluation;
- `未知或推测 / Unknowns or inferences`: capture intent, recoverability, clipping, focus cause, or processing history.

### 2. Technical analysis

Cover only relevant items:

- aperture, shutter, ISO, focal length, focus, and camera/lens when metadata exists;
- sharpness, motion, depth of field, noise, dynamic-range appearance, and artifacts;
- composition, subject hierarchy, viewpoint, spatial organization, color relationships, light, and lens language.

Do not infer capture settings from appearance when metadata is absent. Describe the visual effect instead.

### 3. Commercial and internet suitability

Judge possible use cases and limitations using:

- semantic clarity and speed of recognition;
- thumbnail performance and crop flexibility;
- usable negative space for copy;
- technical adequacy for the intended size;
- series consistency and likely audience;
- visible trademark, property, privacy, model-release, or other rights risks.

Identify visible risks without giving a legal conclusion.

### 4. Art and photographic-history linkage

This section is optional. Use `analysis-framework.md` only when formal evidence supports a useful comparison. Load `movement-map.md` or `photographer-cards.md` only as routed by the main `SKILL.md`. Explain the shared visual mechanism and at least one difference. Do not imply that the photographer was influenced by, copied, or intended to resemble a named artist.

If evidence is weak, say that the image is better described in formal terms than attached to a movement or photographer.

### 5. Inferred intent

Give one primary hypothesis and optional alternatives. For each, include:

- visible supporting evidence;
- confidence: high, medium, or low;
- any sign that argues against it.

Call this an inference, not the user's actual intention.

### 6. Editing directions

Offer 2–4 materially different choices. For each state:

- visible goal;
- tone and color direction;
- what is preserved and what is sacrificed;
- suitable uses;
- intensity: low, medium, or high.

Do not disguise small slider variations as different styles. Default to low-intensity, reversible changes.

### 7. Confirmation gate

Ask the user to confirm or correct:

- inferred intent;
- chosen editing direction and intensity;
- output use;
- any must-preserve or must-avoid constraint.

Do not issue the detailed Darktable recipe before this gate unless the user explicitly asks to skip it.

## Revision loop

When the user rejects part of Round 01:

1. update the challenged subsection;
2. update only dependent intent or style conclusions;
3. show what changed and why;
4. request confirmation again.

Do not rerun unrelated analysis merely for formal completeness.

## Round 02 — one complete limited-edit plan

First restate known context: input type, Darktable version/UI language when known, active principal tone mapper, current edit/history, output, chosen direction, and intensity.

Recommend a duplicate or snapshot if the treatment diverges materially. Then provide one complete plan:

- normally 3–8 useful adjustments;
- 2–4 when the image is already strong;
- global corrections before local masks;
- one principal tone mapper unless a concrete exception is explained;
- no module-order change, AI tool, complex mask, or heavy grading by default.

For every step include:

1. priority: `必要 / Necessary`, `条件性 / Conditional`, or `可选 / Optional`;
2. module and key control in Chinese and English, with the exact English UI name in backticks;
3. where to find it, preferring right-panel search over a fixed module group;
4. direction and a conservative starting range when defensible;
5. a visual or scope-based stopping criterion;
6. the main side effect to watch;
7. when to skip the step.

Recommended order:

1. protect the current version;
2. necessary optical or technical correction;
3. exposure and principal display transform;
4. overall color relationship;
5. local correction only when the global result cannot solve the issue;
6. detail and texture only to the output's needs;
7. output checks.

After feedback, amend only the relevant steps. Return to Round 01 if the intended meaning or selected direction changes.

## Image-state card

Maintain this compact state across the conversation:

- file name/type and evidence limitations;
- confirmed intent;
- chosen direction, intensity, and output;
- Darktable version and principal tone mapper;
- completed or accepted steps;
- unresolved issues;
- rejected assumptions or directions.

## Completion

Close the loop when the user confirms:

- the result matches the intended meaning;
- no obvious halos, mask edges, color contamination, retouch joins, or excessive texture loss remain;
- fit view, 100%, clipping/scopes, and output-specific checks pass.

Record the final modules and the reason each was retained. Only then consider extracting a reusable style or preset.

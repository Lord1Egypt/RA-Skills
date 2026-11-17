\---

name: custom-ai-pptx-generator
description: "AI PPT Designer — byKenzje Create custom, content-driven, fully editable PowerPoint presentations from notes, documents, emails, spreadsheets, images, or other source material. Use when the user wants a presentation, training deck, project briefing, policy explainer, or similar PPTX. The workflow analyzes content, develops a design intent, confirms the structure and storyboard, creates a visual prototype, rebuilds the presentation as native editable PowerPoint objects, and performs visual QA."
license: MIT
version: 1.0.2
---

# AI PPT Designer

## Custom AI PPTX Generator

AI PPT Designer is a content-driven presentation workflow for creating **native, editable PowerPoint presentations**.

It should be used when the user provides source material and wants a finished PPTX rather than a collection of slide images.

## Core principles

* **Content determines design.** Do not default to a previously used layout or fixed template.
* **The final deliverable must be native and editable.** Do not create full-slide image slabs as the final PPT.
* **The user's content is the source of truth.** Do not invent facts, numbers, labels, dates, or conclusions.
* **The user controls important design decisions.** Do not silently approve structure, style, colors, naming, or visual direction on the user's behalf.
* **Design variety should serve communication.** Do not force visual variety when it harms clarity or content logic.
* **Do not silently overwrite files.** Preserve earlier versions or create a new version suffix.
* **Keep the workflow efficient.** Avoid unnecessary re-analysis, repeated image generation, or redundant full-deck rebuilds.

## Workflow

```text
Source material + requirements
        ↓
1. Content analysis
        ↓
1.5 Design Intent Brief
        ↓
2. Structure confirmation  ← user approval required
        ↓
3. ASCII storyboard        ← user approval required
        ↓
4. Visual prototype        ← user approval required
        ↓
5. Native editable PPTX
        ↓
6. Visual QA and delivery
```

The Design Intent Brief is a lightweight internal design-thinking step. It does not create an additional approval gate.

### 1\. Content analysis

Analyze the user's source material, which may include text, images, email, tables, documents, or dictated requirements.

Extract:

* Core messages
* Key numbers and units
* Categories
* Processes and relationships
* Conclusions
* Audience
* Required level of detail

Treat **number + unit + definition/scope** as a single factual unit. Preserve the exact source meaning.

If the audience is unclear, ask whether the presentation is internal or external when this affects the level of detail.

### 1.5 Design Intent Brief

Before creating the storyboard, create one concise Design Intent Brief.

It should contain:

1. **Core Visual Idea** — the central visual concept for the presentation.
2. **Audience Feeling** — the intended feeling, such as clarity, trust, curiosity, urgency, inspiration, or confidence.
3. **Visual Language** — e.g. editorial, cinematic, playful, structured, immersive, minimal, organic, or human-centered. This is not the color palette.
4. **Preferred Visual Expressions** — e.g. hero visual, diagram, timeline, journey, ecosystem, comparison, typography, metaphor, or data visualization.
5. **Avoid** — visual approaches that do not fit this topic, including layouts that would be repeated only because they worked in an earlier project.
6. **Special Visual Opportunities** — topic-specific elements that can become part of the visual language.

Rules:

* Do not create a template library.
* Do not make every slide use the same visual expression.
* Keep overall visual coherence while allowing individual slides to respond to their content.
* Never sacrifice content logic just to increase visual variety.
* If the user has already specified a visual requirement, follow it.
* If the user has not specified a visual direction, propose one without creating an extra approval round.
* Keep this step lightweight: no multiple style explorations, no image generation, no PPT generation, and no repeated content analysis.

### 2\. Structure confirmation — user approval required

Present a proposed structure and ask the user to confirm it before moving on.

Confirm:

1. **Page structure** — landscape/portrait, approximate page count, and the role of each page.
2. **Main color palette** — ask for preferred colors or color values when relevant.
3. **Audience and detail level.**
4. **People / character / image elements** — explicitly ask whether they are needed.

If people or character elements are needed, clarify:

* **Source:** user-provided images, AI-generated visuals, or placeholders.
* **Usage:** selected pages, light use across the deck, or a specific page.

Also present a small set of plain-language style options when the user has not specified a style. Do not silently choose a style for them.

User-provided names and wording have priority over AI-generated alternatives.

### 3\. ASCII storyboard — user approval required

Create a plain-text storyboard showing the structure of every slide.

Each slide should make clear:

* Title
* Final wording
* Content blocks
* Hierarchy
* Information density
* Layout
* `visual expression:`
* `key visual idea:`

All wording in the storyboard should be final wording, not placeholders. The approved storyboard becomes the content contract for later production.

The storyboard must reflect the Design Intent Brief. Do not use an approach listed under `Avoid`.

If the user changes something at this stage, update only the affected pages or blocks. Do not rerun content analysis or recreate the Design Intent Brief unless the underlying content has changed.

### 4\. Visual prototype — user approval required

The visual prototype should be a near-final representation of the approved storyboard, not a completely new design direction.

Use these inputs together:

1. Original source material — factual source of truth
2. Approved ASCII storyboard — approved content and layout
3. Design Intent Brief — visual intent

Available visual-generation paths:

* A configured external image-generation API, when available
* Built-in image generation for quick visual validation
* Prompt-delivery fallback when generated images are unsatisfactory

If the user indicates that the generated visuals are not satisfactory, stop repeated generation and provide copyable prompts for an external image-generation tool instead.

The prototype should be close to the intended final appearance.

#### Image-generation handling

When generating multiple page visuals with tools that may reuse output filenames, generate them **sequentially**, not in parallel, unless the tool explicitly guarantees isolated output paths.

Never trust returned filenames alone to determine page mapping. Verify each image against the intended slide content.

#### People / character assets

When AI-generated people or character elements are required:

* Generate them separately after the visual direction is approved.
* Do not rely on cropping small characters from a full-slide preview.
* Keep the visual style consistent with the approved design.
* Treat character elements as supporting visuals rather than replacing the main content.
* For circular badge-style character visuals, a circular composition can be used so the asset can be embedded cleanly as an ellipse/circle in the native PPTX.

### 5\. Native editable PPTX generation

Build the presentation using native PowerPoint objects.

Use:

* Native text boxes
* Native shapes
* Native connectors
* Native tables/charts where appropriate
* Embedded image assets only where images are genuinely required

The approved storyboard controls **what is written**. The approved visual prototype controls **what it looks like**. The Design Intent Brief provides the visual rationale.

External image-generation tools may alter wording or numbers. Never treat generated image text as the source of truth.

When practical, create an additional ASCII-named render copy for PowerPoint rendering workflows that have problems with non-ASCII paths.

For 16:9 presentations, use a 13.333 × 7.5 inch canvas unless the user specifies another format.

Build each page as an independent page function where practical, and keep reusable helpers for text, shapes, connectors, backgrounds, and icons.

### 6\. Visual QA and delivery

Perform visual and technical checks before final delivery.

Preferred Windows PowerPoint QA:

1. Open the render copy with PowerPoint COM.
2. Export each slide to PNG at approximately 1920 × 1080.
3. Compare the rendered slides with the approved visual prototype.
4. Fix issues and rebuild only what is necessary.
5. Recheck the result.

Deliver:

* Final editable PPTX
* Rendered slide images when available
* A concise delivery note
* A content / wording difference note when external visual generation changed visible wording

## Collaboration rules

1. **Never silently overwrite an existing deliverable.** Use a version suffix such as `\_v2` or preserve a `draft0`.
2. **Do not repeatedly generate visuals after the user rejects them.** Switch to prompt delivery when appropriate.
3. **The user decides style, colors, and custom naming.** Offer choices and plain-language explanations.
4. **Preserve factual integrity.** Check numbers, units, labels, dates, and names against the source.
5. **Minimize unnecessary rework.** Apply changes locally whenever possible.
6. **Do not treat temporary project iterations as long-term memory.** Preserve reusable knowledge in the Skill files instead.

## Technical environment

The reference implementation was developed for Windows with Python and PowerPoint.

Typical environment:

* Python 3.10+
* `python-pptx`
* Windows desktop PowerPoint
* PowerShell for PowerPoint COM rendering
* Optional image-generation tool or API

Do not assume the author's local absolute paths exist on another machine. Prefer project-relative paths and environment variables.

For PowerShell scripts:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <path>
```

Avoid complex inline PowerShell commands when a script file can be used instead.

### PowerPoint COM safety

When using PowerPoint COM:

1. Prefer scripts that guarantee `Presentation.Close()` and `Application.Quit()` in a `try/finally`-style cleanup.
2. If a PowerPoint instance hangs, terminate only the instance started by this Skill when its process ID is known.
3. Do not blindly run:
`Get-Process POWERPNT | Stop-Process -Force`
4. If a user-owned PowerPoint process must be force-terminated, warn that unsaved work may be lost and obtain confirmation first.

## Reusable scripts

The reference implementation may include:

|Script|Purpose|
|-|-|
|`deck\_ssc\_v1.py`|Example native PPTX builder structure|
|`deck\_qianti\_v2.py`|Example alternative visual builder|
|`export\_png\_template.ps1`|Safe PowerPoint COM PNG rendering template|
|`bissect.py`|Incremental diagnosis of PowerPoint/XML corruption|
|`test\_sync.py` / `test\_sync2.py`|Same-size icon comparison tests|
|`sample\_ssc\_colors.py`|Color sampling from visual references|
|`cutout.py`|Image cutout / alpha-processing pipeline|

Reuse these scripts as references rather than assuming their original project content should be copied into every presentation.

## Troubleshooting

### PowerPoint opens with an XML-related error

If Python and ZIP validation succeed but PowerPoint reports an XML-related corruption error:

* Inspect the affected `ppt/slides/slideN.xml`.
* Check for duplicated adjustment geometry or malformed drawing properties.
* Use `bissect.py` to isolate the smallest problematic change.

Known historical failure patterns include invalid alpha values and duplicated shape adjustment nodes.

### Icons or small elements look blurry

Test candidate icons at their **final rendered size** rather than evaluating only large source assets.

### Invalid empty text runs

Avoid creating zero-size or otherwise invalid empty text runs when a paragraph only needs to be empty. Use valid paragraph properties instead.

### Returned visual assets do not match slide order

Map each returned asset by inspecting its actual content. Do not rely on filenames or generation order alone.

## Reference material

If the package contains:

`references/千题千境\_项目经验总结.md`

use it as the detailed implementation reference for the workflow, engineering lessons, reusable assets, and troubleshooting history.

The reference implementation is a baseline, not a reason to expose internal engineering details to the end user.


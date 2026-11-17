# Historical examples and validation scope

Historical examples keep their original versions and evidence limits; they are not relabelled as 5.3.0 runs. See the current [README](../../README.en.md).

## Gallery: 22-slide Xiaomi business review

**2026-10-18 · Decorative business design.** The user-supplied Xiaomi Q2/H1 2025 report and data sheet became a 22-slide presentation through real rendering, revisions, and independent agent review. Click the image for the full preview.

[![Xiaomi Q2/H1 2025 business review: actual rendered overview of 22 slides](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png)](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png)

<details>
<summary>Version and validation scope</summary>

The experiment used development commit `af23320`, whose version file still read `5.1.1`. Those changes are now included in `5.2.0`; the historical run has not been relabelled as a test of the final release. The PPTX contains 370 text objects, 139 shapes/paths, 6 native charts and 4 native tables: 519 native objects and no images.

On Linux + LibreOffice, sampled text and table edits persisted after saving and reopening. In-application chart-data editing was not successfully validated, and PowerPoint/WPS was not tested. Alibaba PuHuiTi fonts are not embedded. Only the overview image is distributed here; raw inputs, full logs and evidence packages remain outside the public repository.

</details>

## v5.1 example: six Chinese slides, no image generation

An independent author used the current Skill and a seven-page user-provided PDF, *AI SME Entrepreneurship Support Plan (2026–2028)*, to create a six-slide Chinese overview without image-generation calls. Every slide includes speaker notes and source references. The 90-day action sequence is explicitly labeled as an author recommendation.

Download the same [editable PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-native.pptx), or inspect the [object counts and acceptance evidence](../../assets/samples/v5.1-no-image-policy-evidence.json). These images are unmodified previews rendered from that PPTX.

### Cover: 13 text objects and 6 native shapes

![v5.1 original cover rendered without image generation](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png)

### Targets: 16 text objects and 3 native shapes

![v5.1 policy targets with original numeric qualifiers preserved](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-02.png)

### Actions: 18 text objects and 5 native shapes

![v5.1 native timeline labeled as author advice, not an official application process](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-06.png)

Counts come directly from the delivered PPTX. Each text box or shape is counted once:

| Slide | Native text | Native shapes | Editable objects |
| --- | ---: | ---: | ---: |
| 1 · Policy overview | 13 | 6 | 19 |
| 2 · Three-year targets | 16 | 3 | 19 |
| 3 · Resource supply | 15 | 4 | 19 |
| 4 · Enterprise development | 12 | 3 | 15 |
| 5 · Open source and support | 20 | 5 | 25 |
| 6 · Author recommendations | 18 | 5 | 23 |
| **Total** | **94** | **26** | **120** |

This example contains **0 images, 0 native charts, 0 native tables, and 0 groups**, with notes on all six slides. Numbers are editable text; they are not counted as charts. Decorative lines and dots count as shapes. Characters and notes placeholders are not counted again. Object count describes editability, not design quality.

The candidate passed independent review of all pages and source content, reaching `final_delivery_ready`. On **macOS with LibreOffice 26.2.4.2**, Basic/UNO changed text, numeric text, and a shape fill on a disposable copy. Saving, closing, and reopening preserved the edits and all six notes; the original candidate stayed unchanged. This is an actual application-object edit test, not GUI clicking, and does not establish Windows/Linux or PowerPoint/WPS compatibility. The sample uses Arial Unicode MS without font embedding; verify fonts and layout on another device.

## Retained v5.0 example: a 20-slide Chinese research overview

A 67-page report, *Agents, robots, and us: How AI reshapes work and skills in Latin America*, became a 20-slide Chinese overview covering automation potential, economic value, jobs and skills, country comparisons, and business cases. All 20 slides have sources and speaker notes. This is the original v5.0-era output, counted separately from the v5.1 example above.

The workflow was source document → complete slide design images → multimodal interpretation and declarative reconstruction → native PPTX → real rendering and acceptance. The original contact sheet is preserved below. [Download the original editable PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-native.pptx) or inspect [per-slide object data](../../assets/samples/v5.0-latin-america-ai-zh-evidence.json).

![v5.0 Agents, robots, and us: actual rendered overview of 20 Chinese slides](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-overview.png)

| Object type | Count | Editing scope |
| --- | ---: | --- |
| Native text boxes | 274 | Text, font, size and colour |
| Native shapes and paths | 164 | Position, size and colour |
| Native charts | 7 | Editable data series with 7 embedded workbooks |
| Native tables | 2 | Cells, rows, columns and styling |
| **Native editable objects** | **447** | **274 + 164 + 7 + 2** |
| Separate cover image | 1 | Replace as a whole; illustration elements are not individually editable |
| **Total slide objects** | **448** | **447 native objects + 1 image** |

Counts are read directly from the original PPTX. Each object is counted once; chart points, table cells, embedded workbooks and notes are not counted again.

<details>
<summary>Show all 20 slides' object counts</summary>

| Slide | Text | Shapes/paths | Charts | Tables | Native editable | Replaceable images |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 2 | 0 | 0 | 9 | 1 |
| 2 | 15 | 18 | 0 | 0 | 33 | 0 |
| 3 | 19 | 6 | 0 | 0 | 25 | 0 |
| 4 | 13 | 5 | 1 | 0 | 19 | 0 |
| 5 | 14 | 7 | 1 | 0 | 22 | 0 |
| 6 | 9 | 3 | 1 | 0 | 13 | 0 |
| 7 | 9 | 3 | 1 | 0 | 13 | 0 |
| 8 | 16 | 10 | 0 | 0 | 26 | 0 |
| 9 | 11 | 5 | 0 | 1 | 17 | 0 |
| 10 | 13 | 8 | 1 | 0 | 22 | 0 |
| 11 | 9 | 3 | 1 | 0 | 13 | 0 |
| 12 | 12 | 5 | 1 | 0 | 18 | 0 |
| 13 | 15 | 9 | 0 | 0 | 24 | 0 |
| 14 | 7 | 3 | 0 | 1 | 11 | 0 |
| 15 | 20 | 9 | 0 | 0 | 29 | 0 |
| 16 | 15 | 6 | 0 | 0 | 21 | 0 |
| 17 | 16 | 13 | 0 | 0 | 29 | 0 |
| 18 | 20 | 9 | 0 | 0 | 29 | 0 |
| 19 | 17 | 28 | 0 | 0 | 45 | 0 |
| 20 | 17 | 12 | 0 | 0 | 29 | 0 |
| **Total** | **274** | **164** | **7** | **2** | **447** | **1** |

</details>

Historical acceptance used macOS + LibreOffice 26.2.4.2 through Basic/UNO to edit text, chart data, table data and the cover image on a copy. Changes persisted after saving, closing and reopening. Reconstruction retains differences in fonts, icons, gradients and chart styling; pixel-perfect 1:1 fidelity is not claimed. PowerPoint/WPS was not tested. Hiragino Sans GB and Arial are not embedded; recheck fonts and layout on another device.

## Historical examples

These are real renders from earlier versions and are not part of the v5.1 object counts above.

<details>
<summary>Show V4 Template and Bespoke examples</summary>

**Template: a 31-slide research presentation**, with notes on 29 body slides, using a source report and native template components.

![V4 Template 31-slide rendered contact sheet](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/mgi-template-v4-31-page-contact-sheet.png)

**Bespoke: a 23-slide independent presentation**, with 12 native charts and notes on all 23 slides. These examples use different reports and are not a controlled quality comparison. They do not imply partnership, authorization, or endorsement by report publishers or template brands.

![V4 Bespoke 23-slide rendered contact sheet](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/state-ai-2025-independent-bespoke-23-page-contact-sheet.png)

More historical assets are in the [sample directory](../../assets/samples/).

</details>


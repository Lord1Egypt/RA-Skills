# Export Pipelines Reference

Use this reference when choosing between direct PPTX, native dynamic PPTX, Feishu Slides, static HTML, and web dynamic exports.

## Direct PPTX

Preferred route: PptxGenJS or an existing local helper.

Use when the deck must be editable in PowerPoint, Keynote, LibreOffice Impress, or Google Slides import.

Verification levels:

- `created`: file exists, non-trivial size.
- `inspected`: slide count or internal zip/XML shape inspected.
- `rendered`: converted/opened/screenshot successfully.
- `final`: rendered/read back plus content checks passed.

## Native Dynamic PPTX

This is the stable answer for “dynamic PPT” unless the user explicitly asks for web presentation or same-slide object animation.

Method: progressive build slides.

- Logical slide 1 with 3 bullets becomes 3 visually similar PPTX slides.
- Step 1 shows bullet 1.
- Step 2 shows bullets 1-2.
- Step 3 shows bullets 1-3.
- In slide show mode, each click appears like a reveal.
- Add fade transitions where possible.

Pros:

- Works in PPTX players without fragile animation XML.
- Easy to generate with PptxGenJS.
- Easy to inspect by slide count.
- More robust across PowerPoint and Keynote.

Cons:

- Increases physical slide count.
- Timeline is slide-level, not object-level.
- Editing later requires awareness of build-step duplicates.

Verification:

- expected physical slide count equals sum of reveal steps
- notes count matches physical slides when notes are generated
- transition XML exists if transitions are added
- QuickLook/PowerPoint/Keynote can render at least representative slides

## Dynamic HTML Companion

Use reveal.js or custom HTML when the user asks for a web deck, interactive deck, browser presentation, or when a richer motion prototype is needed.

Do not substitute it for native dynamic PPTX when the user asks for PPT.

## Object-Level Animated PPTX Experimental

Native object animation inside one slide is not the default. It requires OOXML timing/animation structures or target-player automation and is fragile across apps.

Only attempt if:

- the user explicitly requires same-slide object animation
- a helper or OOXML patcher exists
- a 1-2 slide prototype can be inspected in PowerPoint/Keynote

Fallback: native dynamic PPTX via progressive build slides.

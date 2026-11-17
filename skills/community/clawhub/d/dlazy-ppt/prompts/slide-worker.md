# Slide Worker Prompt

Use this template when dispatching a slide subagent after the sample slide is approved and full-deck generation is authorized.

```text
Generate slide <N> for this dlazy-ppt deck.

Deck dir: <absolute deck dir>
Slide job file: <absolute deck dir>/prompts/slide_<NN>.json
Output target owned by parent: <absolute deck dir>/origin_image/slide_<NN>.png
Image tool: `scripts/image_gen.py` (dLazy)
Sample generation method copied from the approved sample:
- backend_used: <exact label recorded by parent>
- tool_name: <image_gen OR image_generate OR scripts/image_gen.py>
- mode: <generate OR edit>
- model/config: <model, size, quality>
- prompt_source: <approved sample prompt source>
- input_context_preparation: <how local images were made visible or attached>
- approved_sample_path: <absolute path to approved origin_image/slide_XX.png>
- handoff_rule: use this same command shape; return a blocker if unavailable
Input images already prepared by the parent:
- <absolute path> - approved sample slide style reference; match style only, do not copy layout
- <absolute path> - strict input asset; preserve labels/data/arrows/content

Read the JSON job file, then follow its `prompt` field exactly. Use the dLazy image tool and the recorded sample generation method only.
You must produce the final slide candidate with `scripts/image_gen.py`, using the saved job prompt and every required image input.

Forbidden for final slide image creation:
- local drawing or rendering scripts
- Pillow-generated slides
- SVG, HTML/CSS, or canvas screenshots
- python-pptx/PptxGenJS/native PPT layout screenshots
- manually composited text, card, chart, or image overlays

If you cannot use the dLazy image tool, stop and return `blocker=<reason>` instead of creating a lower-quality replacement.
If you cannot follow the recorded sample generation method, stop and return `blocker=<reason>` instead of switching tools.
Do not edit slide job files, origin_image, speech.md, or assemble the PPT.

Before returning, visually check:
- Chinese text is readable and not garbled
- style matches the approved sample slide
- required source images are visibly included and not replaced by a similar redraw
- no overlapping or truncated important content

Return only:
backend_used=scripts/image_gen.py
selected_source=/absolute/path/to/the/--out/path/passed/to/image_gen.py
qa_note=<one sentence>
```

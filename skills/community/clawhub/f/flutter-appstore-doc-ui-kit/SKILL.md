---
name: flutter-appstore-doc-ui-kit
description: Generate a launch-ready app package for App Store submission: a complete Markdown feature document plus AI-generated Apple-style UI design images for each page and a square-corner app icon. Use when the user wants a Flutter app concept/spec constrained to FVM Flutter 3.35.1, offline-first (no backend), camera + photo library permissions, anti-saturation positioning, and no TODO/temp placeholders.
---

# Flutter AppStore Doc + UI Kit

Generate an App Store-ready pack in gated stages with mandatory user review between stages:

- `docs/app-feature-spec.zh-CN.md` + `docs/app-feature-spec.en-US.md`
- `ui/*.png` (AI-generated Apple-style page design images)
- `icon/app_icon_1024.png` + `icon/app_icon_1024.svg` (square-corner icon)

## Workflow (Approval-Gated)

1. Generate APP feature docs in Chinese + English and output them.
2. Ask user to download/review docs; wait for: **continue** or **revise docs**.
3. Proceed only after user explicitly approves docs.
4. Confirm image-generation capability:
   - If API/model access exists, generate page-level UI images from approved docs.
   - If no API/model access, output one unified style prompt package for user-side generation.
5. Ask user to download/review UI images.
6. Proceed only after user explicitly approves UI images.
7. Confirm icon-generation capability:
   - If API/model access exists, generate icon via model.
   - If no API/model access, generate icon with programmatic SVG->PNG pipeline.
8. Ask user to review icon.
9. Finish only after user explicitly approves icon.

Do not auto-skip any gate. If user asks for changes, revise only that stage and re-submit for approval.

## 1) Required Inputs

Collect/confirm:

- App name
- Target language(s)
- Preferred app direction (if none, pick a low-saturation utility direction)
- Optional color style

Hard constraints to enforce:

- Tech stack: Flutter via **FVM Flutter 3.35.1**
- Includes **camera** + **photo library** permissions
- Avoid over-saturated app categories and avoid risky claim patterns
- No backend server required
- No TODO placeholders or temporary/fake data sections
- Document scope must be **version 1.0.0 only**
- Do **not** include roadmap/future updates/backlog/post-v1 plans
- Can include general capabilities: i18n, dark mode, accessibility, privacy-first local storage
- App icon must be **square-corner** (not rounded)

## 2) Stage 1 — Generate and Deliver Feature Docs (ZH + EN)

Run once:

```bash
python3 scripts/generate_appstore_pack.py \
  --app-name "SnapSort" \
  --out ./out/snapsort \
  --locales "en,zh-Hans" \
  --primary-color "#0A84FF"
```

Then prepare doc outputs first and deliver only docs for review:

- `docs/app-feature-spec.zh-CN.md` (if missing, derive from base spec and provide Chinese version)
- `docs/app-feature-spec.en-US.md` (if missing, derive from base spec and provide English version)

If the generator only creates one base spec file, split/translate into two locale files before sending to user.

## 3) Stage 2 — Generate and Deliver UI Design Images

After user approves both docs, check capability first.

### Option A: API/model access available
Use `scripts/generate_ui_ai.py`.

Required auth:
- `OPENAI_API_KEY` in environment (or another confirmed image model backend configured by user).

Example:

```bash
python3 scripts/generate_ui_ai.py \
  --doc ./out/snapsort/docs/app-feature-spec.en-US.md \
  --out ./out/snapsort/ui \
  --primary-color "#0A84FF"
```

Outputs:
- `ui/page-01-*.png` ... `ui/page-08-*.png`

### Option B: no API/model access
Output a single unified prompt package (global style + 8 page prompts + naming rules) for the user to generate images manually in external tools.
Then collect user-generated images and continue to UI review gate.

Do not deliver icon in this stage.

## 4) Stage 3 — Generate and Deliver App Icon

After user approves UI images, check capability first.

### Option A: API/model access available
Generate icon with image model and export PNG.

### Option B: no API/model access
Generate icon with deterministic programmatic pipeline (SVG source + PNG output).

Deliver icon artifacts:

- `icon/app_icon_1024.png`
- `icon/app_icon_1024.svg`

## 5) Quality Validation

Before each approval gate, validate that stage artifacts are complete:

Doc stage:
- Both `zh-CN` and `en-US` docs exist and are semantically aligned.
- Feature doc explicitly states FVM Flutter 3.35.1.
- Feature doc version is explicitly marked `1.0.0`.
- Camera + photo permissions appear in feature/privacy sections.
- No backend dependency appears in architecture/data flow.
- No TODO/TBD/temp/placeholder language.
- No roadmap / future update sections are present.

UI stage:
- UI images are PNG outputs (AI-generated or user-generated from provided prompt package).
- UI images cover all listed key pages in approved spec.
- Labels and flows match approved doc wording.

Icon stage:
- Icon is visually square (no rounded corner mask baked into source).
- Icon style matches approved product direction.

## 6) App Store Safety Guidance

Use `references/review-safety-checklist.md` and keep copy conservative:

- No medical/financial/legal guarantee claims
- No “instant earnings” or manipulative wording
- Permission usage tied to clear user-triggered actions
- Privacy text explicitly local-first and user-controllable

## Notes

- This skill creates design/spec artifacts, not Flutter code.
- If user also needs implementation scaffolding, create a separate Flutter build skill.

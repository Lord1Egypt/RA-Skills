# Article HTML To PPT

Convert articles, Markdown drafts, HTML pages, WeChat drafts, and review-approved manuscripts into formal, brand-consistent slide decks.

This skill supports:

- direct PPTX export
- native dynamic PPTX via progressive build slides
- HTML preview or dynamic HTML companion decks
- Feishu Slides routing
- MeowClawLab visual systems
- evidence-backed storyboards
- content lock, slide manifest, and lightweight visual QA gates

## Quality Contract

- Important claims, numbers, examples, diagrams, and recommendations must trace back to source material or be labeled as reconstruction or assumption.
- Storyline comes before slide production.
- Slide content is locked before visual previews or PPTX export.
- Non-trivial decks should maintain `slide_manifest.json`.
- Core text should remain editable where the export format supports it.
- Visual structure should not be downgraded into a flat screenshot unless the user explicitly accepts that tradeoff.

## Templates

- `templates/storyboard-template.md`
- `templates/content-lock-template.md`
- `templates/slide-manifest-template.json`
- `templates/visual-qa-gate-template.json`

## Version

1.0.3

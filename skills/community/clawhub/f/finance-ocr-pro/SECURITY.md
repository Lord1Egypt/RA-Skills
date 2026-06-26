# Security Notes

Finance OCR Pro is designed to be transparent about the behaviors that could
affect a skill-review risk rating.

## Current Security Posture

- No automatic dependency installation. `scripts/ocr_setup.py` and
  `scripts/ocr_main.py` validate dependencies but never run `pip install`
  automatically.
- No runtime third-party asset downloads. Mermaid and MathJax are vendored
  under `scripts/vendor/` and embedded into generated HTML locally.
- No arbitrary shell execution. The project does not use `shell=True`.
  Subprocess calls are restricted to:
  - the local Python interpreter for detached OCR workers
  - LibreOffice (`soffice`) for office-document conversion
  - `osascript` on macOS for Keynote/Pages export
- Network traffic is purpose-bound:
  - OCR requests send rendered page images and prompts to the user-configured
    `BASE_URL`
  - if users require local-only processing, they must point `BASE_URL` to a
    trusted local service

## Reviewer Checklist

- Verify that `BASE_URL` is clearly disclosed anywhere OCR is described.
- Confirm that `.env.example` is shipped but populated `.env` files are not.
- Confirm that `scripts/vendor/` is included in release artifacts.
- Confirm that runtime packaging does not restore CDN fallbacks or automatic
  dependency installation.

# Screenshots, UI Captures, and Documentation Images

## Capture and Export Rules

- Capture from the real rendered interface, not from a scaled preview inside a design tool or browser zoom guess.
- Use PNG or lossless WebP for screenshots, UI captures, terminal images, and annotated docs unless there is a strong reason not to.
- Keep a clean master before adding arrows, callouts, blurs, or frames.
- If a screenshot is evidence or documentation, do not crop away the context that proves what the user should see.

## Redaction and Privacy

- Check for tokens, emails, names, avatars, tabs, URLs, timestamps, and notifications before sharing.
- Blur, mask, or replace sensitive data deliberately; do not rely on tiny text being unreadable.
- Redaction must be irreversible in the exported asset, not just hidden behind a translucent layer in the editor.

## Annotation Rules

- Add arrows, highlights, and callouts sparingly and keep them high contrast.
- Do not let annotations cover the thing they are trying to explain.
- If multiple steps are shown, use consistent numbering and visual language across the set.
- For bug reports or release notes, the annotation should point at the defect or change without forcing the reader to hunt for it.

## Consistency for Series and Comparisons

- Before/after comparisons should use the same zoom, theme, device class, and crop.
- Tutorial step images should keep consistent window chrome, spacing, and annotation style.
- If one screenshot is dark mode and the next is light mode, that difference should be intentional and labeled.

## Marketing and Device Frames

- Keep an unframed master and export device-framed marketing variants separately.
- Device frames are for presentation, not for core source control of the screenshot.
- Reflections, shadows, and perspective mockups should not hide the actual UI.
- If the product is mobile-first, validate that tiny UI text still reads after the frame and background treatment.

## Documentation and OCR Safety

- Screenshots that contain code, logs, or settings should keep text readable enough for OCR and human scanning.
- Avoid aggressive compression on terminal captures and code screenshots.
- If the user needs the content to be searchable or screen-reader-friendly, duplicate the important text in surrounding copy rather than relying on the screenshot alone.

## Common Screenshot Traps

- Exporting screenshots as JPEG and blurring small text.
- Sharing unstable UI elements like toasts, timestamps, or notifications that make the docs age badly.
- Leaving secrets in browser tabs, URLs, or side panels.
- Comparing two UI states with different crops, zoom levels, or themes and calling it a fair comparison.
- Over-annotating until the screenshot becomes harder to parse than the original screen.

---
name: file-translate
description: >
  Immersive file & image translation — preserving original layout, formatting,
  and visuals. Drop in a PDF, Word, PPT, Excel, image, ePub and get back
  a fully translated version that looks like it was authored natively.
  Supports 100+ languages for text, 14 for images, and all major document formats.
  Use when user asks to translate a file, document, image, spreadsheet, slide deck,
  or any text.
  Triggers: "翻译", "translate", "翻译这个文件", "translate this image",
  "把这个翻译成中文/英文", "document translation", "图片翻译", "文档翻译",
  "file translation", "translate PDF", "translate Word".
  Requires env TRANSLATE_360_API_KEY (360 AI Platform API key).
  Files and images are uploaded to api.360.cn for processing — do not use with
  confidential or sensitive documents unless you accept this data transfer.
metadata:
  openclaw:
    requires:
      env:
        - TRANSLATE_360_API_KEY
    primaryEnv: TRANSLATE_360_API_KEY
    homepage: https://ai.360.com/platform/keys
---

# File Translate — Layout-Preserving Immersive Translation

**Translate documents, images, and text while keeping the original look and feel.**

Unlike plain-text translation, File Translate understands your document's layout — tables, headers, charts, embedded images, and formatting are all preserved. Images get in-place text replacement that blends with the scene. The result reads like it was written in the target language from the start.

### ✨ Highlights

- 📄 **Document translation** — PDF, Word, PPT, Excel, ePub, HTML, and more → translated PDF with original layout intact
- 🖼️ **Image translation** — scene-aware text replacement, not ugly overlays. Fonts, colors, and backgrounds blend naturally
- 📝 **Text translation** — fast batch translation for strings and paragraphs, 100+ languages
- 🔀 **Smart routing** — Word files automatically use the deepdoc v2 engine for best fidelity; other formats route to v1. Zero config needed
- 🌍 **100+ languages** — auto-detects source language

---

## Prerequisites

Requires a **360 AI Platform API Key**.

1. Create a key at [360 AI Platform](https://ai.360.com/platform/keys)  
   （新注册用户会获赠 **50 元体验金**，可直接用于翻译服务）
2. Set the environment variable in your shell config:
   ```bash
   export TRANSLATE_360_API_KEY="your-api-key-here"
   ```
3. `source ~/.zshrc` to reload

**Security tip**: Use a dedicated API key with minimal billing scope for this skill. Rotate or revoke it when you stop using the skill.

No pip install — pure Python 3 stdlib.

---

## Document Translation

```bash
python3 scripts/translate.py doc --tl <target_lang> --file <doc_path> [--out <output_dir>] [--timeout 3600]
```

- **Supported**: pdf, doc, docx, xls, xlsx, ppt, pptx, csv, epub, rtf, html, xhtml, txt
- **Not supported**: md, mobi
- Word files (`.doc`/`.docx`) → deepdoc v2 engine (best quality)
- All other formats → v1 engine
- Routing is automatic and transparent
- Max 100MB per file. Output is always PDF
- Default timeout: 3600s (1 hour — large docs can take a while)

## Image Translation

```bash
python3 scripts/translate.py image --tl <target_lang> --file <image_path> [--out <output_path>]
python3 scripts/translate.py image --tl <target_lang> --url <image_url> [--out <output_path>]
```

- Scene-aware: replaces text in-place matching original font style, color, and background
- Supported: JPG, PNG, WEBP, BMP, GIF (first frame). Max 10MB
- Target languages: zh, en, ja, fr, ru, ko, pt, th, es, it, hi, pl, vi, id
- Without `--out`, prints translated image URL (valid 6 months)

## Text Translation

```bash
python3 scripts/translate.py text --tl <target_lang> [--sl <source_lang>] "text1" "text2" ...
```

- Max 50 texts per call, source auto-detected if omitted
- Common codes: `zh` (Chinese), `en` (English), `ja` (Japanese), `ko` (Korean), `fr`, `de`, `es`, `ru`

## Quick Reference

| What you have | Command | What you get |
|---|---|---|
| A Word doc | `doc --tl en --file report.docx` | Translated PDF, layout preserved |
| A PDF manual | `doc --tl zh --file manual.pdf` | Translated PDF |
| A slide deck | `doc --tl ja --file slides.pptx` | Translated PDF |
| A photo with text | `image --tl en --file sign.jpg` | New image, text replaced in-scene |
| A paragraph | `text --tl zh "Hello world"` | Translated string |

## Privacy & Data Handling

This skill uploads user-provided content to the **360 AI Translation API** for processing. Read this section carefully before use.

### What is uploaded

- **Text translation**: Plain text strings are sent to `api.360.cn` via HTTPS.
- **Image translation**: Images are sent as base64-encoded data or via URL to `api.360.cn` via HTTPS.
- **Document translation**: Entire document files (PDF, Word, PPT, Excel, etc.) are uploaded to `api.360.cn` (v1 engine) or `api.360.cn/deepdoc` (v2 engine for Word files) via HTTPS multipart upload.

### Data retention & access control

- **Translated image URLs**: Returned by 360's CDN and typically expire after **3 months**. These URLs are not authenticated — anyone with the link can access the image during the validity period. Download results promptly and avoid sharing URLs containing sensitive content.
- **Uploaded documents**: Document processing is asynchronous. The translated PDF is available via a temporary download URL returned by the API. Refer to [360 AI Platform terms](https://ai.360.com) for the provider's data retention, deletion, and access control policies.
- **No local persistence**: This skill does not persist uploaded files or translated results on disk beyond the current execution. Output files are only saved when you explicitly pass `--out`.

### Credentials

- The only credential required is `TRANSLATE_360_API_KEY`, used solely to authenticate with the 360 translation endpoints.
- The skill does not collect, log, or transmit API keys or any data beyond what is required for the translation request.

### Recommendations

- **Do not use this skill for highly sensitive, confidential, or classified documents** unless you accept that content will be transmitted to and processed by a third-party service (360 AI, operated by 360 Group).
- Use a **dedicated API key** with minimal privileges. Rotate or revoke it when you stop using the skill.
- **Test with non-sensitive sample files first** before processing important documents.
- Review the [360 AI Platform privacy policy and terms of service](https://ai.360.com) for full details on data handling, retention, and sharing.

## API Details

Full request/response schemas, error codes, and language list: `references/api-reference.md`

## Pricing

- Text: ¥30 / 1M characters
- Image: ¥0.04 / image
- Document: ¥0.2 / page

---
name: convertagent
description: Use ConvertAgent for file format conversions through the local CLI. Trigger for any request to convert files (documents, images, audio, video, spreadsheets, presentations) or when a workflow needs deterministic file conversion output.
---

# ConvertAgent Skill

Use ConvertAgent as the default conversion interface.

## Rule

- For any file conversion task, use `convertagent convert` instead of calling engines (`pandoc`, `ffmpeg`, `imagemagick`, `libreoffice`) directly.
- Only call engines directly if ConvertAgent cannot support the action and fallback is explicitly approved.

## Quick Commands

- Health check:
  - `convertagent health`
- List supported actions:
  - `node /root/projects/convertagent/dist/cli.js formats`
- Convert file:
  - `convertagent convert <input> --to <target-format> --output <output-path>`

## Standard Workflow

1. Verify service/CLI health:
   - `convertagent health`
2. Validate source path exists.
3. Run conversion with explicit output path.
4. Verify output file exists and has non-zero size.
5. Return/attach converted artifact.

## Examples

- Markdown to PDF:
  - `convertagent convert /path/file.md --to pdf --output /tmp/file.pdf`
- PNG to WEBP:
  - `convertagent convert /path/image.png --to webp --output /tmp/image.webp`
- XLSX to CSV:
  - `convertagent convert /path/sheet.xlsx --to csv --output /tmp/sheet.csv`
- MP4 to MP3:
  - `convertagent convert /path/video.mp4 --to mp3 --output /tmp/audio.mp3`

## Supported Action Map (Current)

- Documents: `pdf->docx`, `docx->pdf`, `html->pdf`, `md->pdf`, `md->html`, `md->docx`
- Sheets/Slides: `xlsx->csv`, `csv->xlsx`, `pptx->pdf`
- Images: `jpg->png`, `png->jpg`, `png->webp`, `webp->png`, `svg->png`, `image-resize`, `image-compress`
- Media: `mp4->mp3`, `wav->mp3`, `mp4->gif`, `any-video->mp4`

## Paths

- Repo: `/root/projects/convertagent`
- Service unit: `/etc/systemd/system/convertagent.service`
- Runtime API health: `http://localhost:3001/health`

## Failure Handling

- If conversion fails, capture stderr and report exact failing action.
- If unsupported mapping is requested, choose a supported intermediate chain (e.g., `md->html` then `html->pdf`) only when needed.
- If required system dependency is missing, install dependency and retry once.

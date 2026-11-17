---
name: dsh-paddleocr-skills-setup
description: >-
  Install and configure the native PaddleOCR plugin for DeepSeek Harness (DSH) from the Settings → PaddleOCR GUI. Use for OCR and image-to-text from screenshots, scans, and PDFs; Chinese/CJK text; PDF-to-Markdown; structured document parsing with tables, formulas, layout, and reading order; or DSH endpoint, credential, GUI setup, verification, and troubleshooting.
license: MIT-0
metadata:
  author: Aidenwu0209
  repository: https://github.com/Aidenwu0209/dsh-PaddleOCR-Skills
  version: "1.0.1"
  openclaw:
    emoji: "🛠️"
    homepage: https://github.com/Aidenwu0209/dsh-PaddleOCR-Skills
---

# Set up DSH PaddleOCR Skills

Install the native DeepSeek Harness bundle. Do not present it as an OpenClaw
code plugin; this setup skill guides installation into DSH.

Use this setup skill when the request mentions **DeepSeek Harness**, **DSH**,
the **Settings → PaddleOCR** GUI, or tasks such as **图片转文字 / 截图识字 /
扫描件 OCR / PDF 转 Markdown / 表格提取 / 公式识别 / 版面分析**. The bundle
provides native tools for plain OCR and structured document parsing, plus GUI
fields for service endpoints, credentials, timeouts, `uv`, and result storage.

## Install and launch

1. Check Node.js 22.19+, Python 3.9+, `npx`, and `uv`. Explain any missing
   prerequisite before using its official installer. Do not use `sudo` or
   change unrelated settings without permission.
2. Run:

   ```bash
   npx @deepseek-ai/dsh plugin --profile web add "github:Aidenwu0209/dsh-PaddleOCR-Skills#main"
   npx @deepseek-ai/dsh web
   ```

3. Wait for the real local Web URL, open it, and confirm that **Settings →
   PaddleOCR** is visible.
4. Confirm the settings panel links to https://www.paddleocr.com, the API-token
   page, and official API documentation.

## Configure safely

- Ask the user for the HTTPS `/ocr` and `/layout-parsing` endpoints they need.
- Store the token through the DSH Credential field; never echo, log, or place it
  in ordinary settings or source files.
- Confirm `uv`, the selected endpoint, and credential status in the GUI.
- Do not claim success unless the plugin install succeeded, the Web URL
  responded, and the Settings panel was actually visible.

Report prerequisite versions, commands, the Web URL, visible configuration
status, and any values still required from the user.

---
name: dsh-unlimited-ocr-skill-setup
description: >-
  Install and configure the native Unlimited-OCR plugin for DeepSeek Harness (DSH) from its Settings GUI, using Baidu Cloud or a local SGLang/OpenAI-compatible service. Use for long-document OCR; PDF, OFD, Office, text, and scanned-image to Markdown; tables, formulas, and reading order; or DSH provider, credential, local inference, GUI setup, verification, and troubleshooting.
license: MIT-0
metadata:
  author: Aidenwu0209
  repository: https://github.com/Aidenwu0209/dsh-Unlimited-OCR-Skill
  version: "1.0.1"
  openclaw:
    emoji: "🛠️"
    homepage: https://github.com/Aidenwu0209/dsh-Unlimited-OCR-Skill
---

# Set up DSH Unlimited-OCR Skill

Install the native DeepSeek Harness bundle. Do not present it as an OpenClaw
code plugin; this setup skill guides installation into DSH.

Use this setup skill when the request mentions **DeepSeek Harness**, **DSH**,
the **Settings → Unlimited-OCR** GUI, **Baidu Cloud**, **SGLang**, or tasks such
as **长文档 OCR / PDF、OFD、Office 转 Markdown / 多页扫描件 / 表格提取 /
公式识别 / 阅读顺序**. The bundle adds a native parsing tool and GUI fields for
provider selection, credentials, endpoints, timeouts, local inference, and
result storage.

## Install and launch

1. Check Node.js 22.19+, Python 3.9+, `npx`, and `uv`. Explain any missing
   prerequisite before using its official installer. Do not use `sudo` or
   change unrelated settings without permission.
2. Run:

   ```bash
   npx @deepseek-ai/dsh plugin --profile web add "github:Aidenwu0209/dsh-Unlimited-OCR-Skill#main"
   npx @deepseek-ai/dsh web
   ```

3. Wait for the real local Web URL, open it, and confirm that **Settings →
   Unlimited-OCR** is visible.
4. Confirm that the official model repository, cloud API, authentication, and
   local-deployment links are visible and clickable.

## Configure safely

- Ask the user to choose Baidu Cloud or a local/OpenAI-compatible service.
- Store API keys through DSH Credentials; never echo, log, or place them in
  ordinary settings or source files.
- For local mode, allow loopback HTTP or remote HTTPS only.
- Do not claim success unless the plugin install succeeded, the Web URL
  responded, and the Settings panel was actually visible.

Report prerequisite versions, commands, the Web URL, provider status, and any
values still required from the user.

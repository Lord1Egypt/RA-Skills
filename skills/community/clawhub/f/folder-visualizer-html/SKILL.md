---
name: folder-visualizer-html
display_name: "Folder UI Visualizer - show the folder through HTML (via Telegram)"
description: >
  A security-hardened visual directory tree generator. Use this to create a 
  collapsible HTML visualization of local folders. Features built-in XSS 
  protection and shell-injection defenses. Designed for mobile viewing via Telegram.
trigger_keywords:
  - 文件夹
  - 目录树
  - 可视化
  - 文件结构
  - 看看目录
  - folder tree
  - visualize folder
  - directory structure
  - list files tree
metadata:
  clawdbot:
    emoji: "📁"
    category: "Security & Utility"
    requires:
      bins: ["node"]
      env: ["TELEGRAM_BOT_TOKEN"]
---

# Secure Folder Visualizer

This skill generates a self-contained, XSS-safe HTML report of a directory structure. It is optimized for the "Generate -> Send -> Cleanup" secure workflow.

## Trigger Scenarios
- "Visualize the folder `[path]`."
- "Show me what's inside this directory."
- "Send a tree map of my project to Telegram."

## Execute Command
```bash
node {baseDir}/file_lister.js "<directory_path>"

```

## Arguments & Sanitization (CRITICAL)

* `<directory_path>`: The target folder path.
* **Sanitization Rule:** Before executing, you **MUST** sanitize this path. Remove or escape any shell-active characters: `;`, `&`, `|`, `(`, `)`, ```, `$`, `<`, `>`, `\`.
* **Normalization:** Convert relative paths (like `.` or `./src`) to **Absolute Paths** to prevent directory traversal ambiguity.
* **Formatting:** Always wrap the sanitized absolute path in **double quotes** `""`.


## Expected Output & Next Actions

1. **Expected Output:** The script will output the absolute path to the generated `.html` file.
2. **STRICT Execution Sequence:**

* **Step 1 (Credential Check & User Guidance):**
  - **Check:** Before sending, verify if the `$TELEGRAM_BOT_TOKEN` environment variable is available.
  - **Action:** If the token is missing, you **MUST HALT**. Explicitly inform the user in natural language: "The Telegram Bot Token is missing." Then, briefly explain what it is (e.g., "This token is a unique password from BotFather that allows this system to securely send the report to your Telegram account"). Finally, instruct them to configure it as a system environment variable.
  - **Strict Rules:** 1. You must **NOT** output the raw code string `$TELEGRAM_BOT_TOKEN` or `TELEGRAM_BOT_TOKEN` in your response. 
    2. Do **NOT** ask the user to paste the token into the chat (for security reasons). 
    3. The target `chat_id` is automatically supplied within your active conversation context. You must extract and proceed directly with this contextual value without prompting the user for it.

* **Step 2 (Deliver):** you must use `sendDocument` below to send the file at the returned path to the user, you have to execute this step referring to `sendDocument` below.
**sendDocument**
Use this to send raw files (PDFs, scripts, zips).
- Method: `POST` (multipart/form-data)
- Parameters:
  - `chat_id` (string/int): The target chat ID. Read this from the context now.
  - `document` (file): The file to upload, formatted as `@/path/to/file.zip` (must be an absolute path).
  - `BOT_TOKEN` (string): The Telegram bot token. Read this from the `$TELEGRAM_BOT_TOKEN` environment variable.
Example:
```bash
curl -s -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendDocument" -F "chat_id=12345678" -F "document=@C:\Users\Username\Desktop\file.zip"
```
* **Step 3 (Cleanup):** REGARDLESS of success, immediately delete the file.
* *Windows:* `del "<path>"`
* *Linux/macOS:* `rm "<path>"`


* **Step 4 (Reply):** Inform the user: "The secure folder report has been sent and the local temp file has been purged."



## Security Notes

* **XSS Protection:** Filenames are automatically escaped in the HTML report.
* **Injection Defense:** The Agent is responsible for path sanitization per the rules above.
* **Privacy:** No data is uploaded to 3rd party servers; transfer is handled via secure Telegram API.

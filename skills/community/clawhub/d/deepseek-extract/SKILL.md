---
name: deepseek-extract
description: >
  Extract full conversation content from DeepSeek shared chat links.
  Use when: user provides a DeepSeek share URL (chat.deepseek.com/share/...),
  wants to extract or export a DeepSeek conversation, says "deepseek link",
  "deepseek share", "extract deepseek", "导出deepseek对话", or mentions
  saving/exporting a DeepSeek chat.
  NOT for: extracting from ChatGPT, Claude, or other AI platforms; general
  web scraping; or URLs not from chat.deepseek.com/share/.
version: 1.0.0
context: fork
metadata:
  openclaw:
    emoji: "📋"
    homepage: https://github.com/zz0116/deepseek-extract
    requires:
      bins:
        - python3
---

# DeepSeek Extract

Extract full conversation content from DeepSeek shared chat links.

## Prerequisites

Before using this skill, ensure the following are installed:

```bash
pip install playwright
playwright install chromium
```

If `playwright` is not installed when the skill runs, inform the user and offer to run the install commands above.

## Workflow

### Step 1: Validate the URL

1. Check if the provided URL matches `https://chat.deepseek.com/share/...`
2. If the URL does not match this pattern, inform the user:
   - "This skill only supports DeepSeek share links (chat.deepseek.com/share/...)."
   - If the URL is from another AI platform (ChatGPT, Claude, etc.), suggest the appropriate skill or manual copy.
3. If valid, proceed to Step 2.

### Step 2: Run the extraction script

Execute the extraction script from the skill's `scripts/` directory:

```bash
python3 "<skill_dir>/scripts/extract_deepseek.py" "<share_url>" --output "<output_path>"
```

**Parameters:**
- `<share_url>`: The DeepSeek share URL (required)
- `--output`: Output file path (optional, defaults to `./deepseek_conversation.md`)
- `--format`: Output format — `markdown` (default) or `json`
- `--headed`: Run browser in headed mode for debugging (optional flag)
- `--timeout`: Page load timeout in milliseconds (optional, defaults to 30000)

Replace `<skill_dir>` with the actual skill base directory path.

**Error handling:**
- If `playwright` is not installed: inform the user and offer to run `pip install playwright && playwright install chromium`
- If `python3` is not found: try `python` instead
- If the script exits with a timeout error: retry with `--timeout 60000`
- If the script exits with an empty extraction: try with `--headed` flag to debug visually

### Step 3: Verify and deliver

1. Read the output file to verify content was extracted successfully.
2. If the output is empty or contains fewer than 2 messages:
   - Try again with `--headed` flag for debugging
   - The DeepSeek page may have anti-bot protection — inform the user
   - Suggest: "DeepSeek may be blocking automated access. You can try manually copying the conversation."
3. If content was extracted successfully, present it to the user.
4. If the user wants a different format (Word, PDF, etc.), use other skills (docx, pdf) to convert.

### Step 4: Cleanup

Remove any temporary files created during extraction. Keep the output file unless the user specifies otherwise.

## How It Works

The extraction script uses Playwright (headless Chromium) to:
1. Navigate to the DeepSeek share URL
2. Wait for the SPA to fully render (JavaScript execution)
3. Try multiple CSS selector strategies to find message elements
4. Classify messages as user or assistant based on class names and data attributes
5. If primary selectors fail, use aggressive text-parsing fallback
6. Output the result as Markdown or JSON

## Output Format

### Markdown (default)
```markdown
# DeepSeek 对话记录

> 来源: <share_url>

---

## 用户
<message content>

## DeepSeek
<response content>

---
(repeat for each turn)
```

### JSON
```json
{
  "url": "<share_url>",
  "title": "<page title>",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No messages extracted | Anti-bot / CAPTCHA | Try `--headed` flag; copy manually |
| Timeout error | Slow network | Retry with `--timeout 60000` |
| Incomplete content | Lazy loading | Script auto-scrolls; try `--headed` to verify |
| `playwright` not found | Not installed | Run `pip install playwright && playwright install chromium` |
| `python3` not found | Windows environment | Try `python` instead of `python3` |

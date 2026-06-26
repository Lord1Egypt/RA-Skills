---
name: generate-qrcode
description: "MANDATORY: Call the existing Python script. DO NOT write your own code."
metadata: { "openclaw": { "emoji": "📱", "always": true } }
---

# QR Code Generator - STRICT INSTRUCTIONS

**CRITICAL RULE**: You MUST use the pre-written script at `~/.openclaw/skills/generate-qrcode/agent.py`

**NEVER** write inline Python code. **ALWAYS** call the existing script.

## MANDATORY Command

```bash
python3 ~/.openclaw/skills/generate-qrcode/agent.py "<URL or text>" <output_path>
```

## Examples

Generate QR for www.baidu.com:
```bash
python3 ~/.openclaw/skills/generate-qrcode/agent.py "www.baidu.com" ~/Desktop/baidu_qr.png
```

## What NOT to do

❌ WRONG: `python -c "import qrcode; ..."`
❌ WRONG: Installing libraries yourself
❌ WRONG: Writing your own QR code generation code

✅ CORRECT: `python3 ~/.openclaw/skills/generate-qrcode/agent.py "..." output.png`

# Installation Guide

## OpenClaw

```bash
# Install via ClawHub
clawhub install html-ppt-to-pdf

# Or install manually
cp -r html-ppt-to-pdf ~/.agents/skills/
```

The skill is auto-discovered on next session start. No restart needed.

---

## Claude Code (claude.ai/code)

1. Download or clone the skill folder
2. Place it in your skills directory:
   ```bash
   cp -r html-ppt-to-pdf ~/.claude/skills/
   ```
3. Reference it in your project's `CLAUDE.md` or system prompt:
   ```
   Skills path: ~/.claude/skills/html-ppt-to-pdf/SKILL.md
   ```

---

## Codex (OpenAI)

1. Place the skill folder in your workspace:
   ```bash
   cp -r html-ppt-to-pdf ~/your-project/skills/
   ```
2. Add to your `AGENTS.md` or system prompt:
   ```
   Available skill: skills/html-ppt-to-pdf/SKILL.md
   ```

---

## Any Agent (Manual)

Paste the contents of `SKILL.md` into your agent's system prompt or context window. The agent will follow the workflow instructions automatically.

---

## System Dependencies

Install these once before first use:

```bash
# Node.js (v18+) — required for Puppeteer PDF export
node --version   # check if installed
# Install: https://nodejs.org

# Puppeteer (headless Chrome)
npm install puppeteer

# python-pptx (required for .pptx template parsing)
pip install python-pptx
```

### macOS (recommended)
All dependencies available via Homebrew:
```bash
brew install node
npm install puppeteer
pip3 install python-pptx
```

### Linux
```bash
# Puppeteer may need extra Chrome deps
sudo apt-get install -y libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
  libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libatk1.0-0 \
  libgtk-3-0
npm install puppeteer
pip install python-pptx
```

---

## Puppeteer Installation Troubleshooting

If `npm install puppeteer` fails (network/permission issues):

```bash
# Option 1: skip download, install Chrome separately
npm install puppeteer --ignore-scripts
npx puppeteer browsers install chrome

# Option 2: use puppeteer-core with system Chrome
npm install puppeteer-core
# Then in export_pdf.js, change launch() to:
# puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' })

# Option 3: check if Chrome/Chromium is already installed
which google-chrome chromium chromium-browser 2>/dev/null
```

> ⚠️ If Puppeteer cannot be installed, **stop and tell the user** — do not fall back to wkhtmltopdf, pdfkit, weasyprint, or any other PDF tool. These tools do not support modern CSS and will produce broken layouts.

## Verify Installation

Run a quick test:
```bash
node -e "const p = require('puppeteer'); console.log('puppeteer ok:', p.executablePath ? 'bundled' : 'system')"
python3 -c "import pptx; print('python-pptx ok')"
```

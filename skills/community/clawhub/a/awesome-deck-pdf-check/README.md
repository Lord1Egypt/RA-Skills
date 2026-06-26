# html-ppt-to-pdf

An AI skill that turns any design style into a polished HTML slide deck and exports it as a high-quality PDF.

**Works with:** OpenClaw · Claude Code · Codex · Any AI agent

---

## ✨ What it does

Say *"make me slides in Apple style about X"* — the agent will:

1. Analyze the design style (from a `.pptx` template, website URL, screenshot, or keywords)
2. Confirm the style and content with you before generating anything
3. Build a single-file HTML slide deck matching that design
4. Export a pixel-accurate 1440×900 PDF using Puppeteer screenshot-and-compose

## 📥 Input types

| Input | Example |
|---|---|
| `.pptx` template | Upload a PowerPoint file → extract colors, fonts, layouts |
| Website URL | `https://linear.app` → clone its visual style |
| Screenshot / image | Drop a design reference image |
| Style keyword | "Apple Keynote dark", "Notion minimal", "Stripe landing" |

## 🖼️ Output preview

> *(PDF slides generated from this skill)*

<!-- Add screenshots here after publishing -->

---

## 🚀 Installation

### OpenClaw
```bash
clawhub install html-ppt-to-pdf
```

### Manual (Claude Code / Codex / any agent)
```bash
git clone https://github.com/<your-username>/html-ppt-to-pdf.git ~/.agents/skills/html-ppt-to-pdf
```
Then reference `SKILL.md` in your agent's system prompt or `AGENTS.md`.

### Dependencies
```bash
npm install puppeteer     # PDF export (required)
pip install python-pptx   # .pptx parsing (required for template input)
```

See [`references/install.md`](references/install.md) for platform-specific setup (macOS, Linux, Claude Code, Codex).

---

## 📁 Skill structure

```
html-ppt-to-pdf/
├── SKILL.md                  ← Agent instructions (start here)
├── scripts/
│   └── export_pdf.js         ← Puppeteer PDF export script (auto-detects sections)
└── references/
    ├── install.md             ← Installation guide for all platforms
    ├── DESIGN_TEMPLATE.md     ← DESIGN.md template for design spec extraction
    └── export_pdf_guide.md    ← export_pdf.js usage details
```

---

## 💡 How it works

The skill enforces a structured workflow:

```
Input → Extract design spec → ✅ Confirm style
      → Outline slide content → ✅ Confirm content
      → Generate HTML (single file, all CSS inlined)
      → Run export_pdf.js → 1440×900 PDF
```

Two mandatory confirmation steps prevent the agent from generating the wrong style or wrong content.

---

## ⚠️ PDF export notes

The skill uses **Puppeteer screenshot-and-compose** for PDF export — not `wkhtmltopdf`, `page.pdf()`, or any other tool. This is the only method that faithfully preserves modern CSS layout (flexbox, grid, gradients, backdrop-filter, etc.).

---

## 📄 License

MIT

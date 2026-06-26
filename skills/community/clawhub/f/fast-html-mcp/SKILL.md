---
id: fast-html-mcp
name: OpenTalk2HTML-NotMD MCP Server
summary: >-
  Generate, patch, read, and compress HTML pages for reports, dashboards, and
  docs — AI talks to you through beautiful pages, not markdown dumps. 18 tools,
  22 components, 25+ templates with sub-second patch times.
published_date: '2026-05-21'
version: '1.1.0'
source_url: 'https://github.com/Aimino-Tech/OpenTalk2HTML-NotMD'
license: GPL-3.0-only
tags:
  - mcp
  - html
  - components
  - templates
  - ai-communication
  - mcp-server
  - html-generation
  - dom-manipulation
---

# OpenTalk2HTML-NotMD MCP Server

**AI talks to you through beautiful pages — not overwhelming markdown dumps.**

OpenTalk2HTML-NotMD is an MCP server that transforms how AI agents communicate
with you. Instead of drowning in raw markdown files that nobody can read, AI
builds clean, organized HTML pages — reports, dashboards, landing pages,
invoices and more — delivered instantly, no browser required.

**One command. Any AI platform. Real pages.**

```
npx -y @aimino/opentalk2html-notmd
```

---

## When to Use

- Generating complex HTML pages (reports, dashboards, landing pages, docs) from structured component specs
- Patching existing HTML by element id or CSS selector without re-rendering the entire page
- Compressing HTML to fit within token limits while preserving semantic content
- Maintaining cross-section consistency across large multi-section documents
- Building equity research, financial summaries, or data-heavy pages with charts and tables
- Creating email newsletters, pitch decks, changelogs, or API documentation

---

## Quick Start

```bash
npx -y @aimino/opentalk2html-notmd
```

Add to MCP client config:

### Claude Desktop / Cursor / VS Code Copilot

```json
{
  "mcpServers": {
    "open-talk-2-html-not-md": {
      "command": "npx",
      "args": ["-y", "@aimino/opentalk2html-notmd"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add open-talk-2-html-not-md -e npx -a "-y" -a "@aimino/opentalk2html-notmd"
```

---

## Workflow

### 1. Discover what's available

```
list_templates
list_components
get_template_schema(template: "report")
get_component_schema(component: "hero")
```

### 2. Build a page

```
render_page(
  template: "report",
  sections: [
    {component: "hero", props: {title: "Q3 Report", badge: "Draft"}},
    {component: "data-table", props: {headers: ["Metric","Value"], rows: [["Revenue","$1.2M"]]}}
  ],
  output_path: "/tmp/report.html",
  options: {title: "Q3 Report"}
)
```

### 3. Inspect the output

```
read_html(path: "/tmp/report.html", mode: "compressed")
```

Read modes (by token efficiency):
- `structure` — tree overview (70% savings)
- `content` — typed blocks (74% savings)
- `compressed` — summary + stats (87% savings)
- `text` — plain text only (97% savings, best for token budgets)

### 4. Refine with surgical patches

```
patch_html(file_path: "/tmp/report.html", selector: "#content", html: "<p>Updated content</p>")
set_attribute(file_path: "/tmp/report.html", selector: "#main-title", attr: "class", value: "highlight")
```

### 5. Compress for token efficiency

```
read_html(path: "/tmp/report.html", mode: "compressed", offset: 0, limit: 1000)
```

### 6. Maintain consistency (multi-section documents)

```
check_consistency(path: "/tmp/report.html")
propagate_edit(path: "/tmp/report.html", entity: "Revenue", value: "$1.5M", sections: ["summary", "details"])
```

---

## Five-Tier Architecture

```
OpenTalk2HTML-NotMD MCP Server
├── Assembly   → render_page (compose pages from components)
├── Patch      → patch_html, set_attribute, edit_html_range (surgical edits)
├── Read       → read_html (inspect with 97% token savings)
├── Raw        → write_raw_html, format_html, preview_html
├── Email      → render_email, html_to_email (send to inbox)
└── Consistency→ propagate_edit, check_consistency (keep data in sync)
```

**18 tools, 22 components, 25+ templates** — purpose-built for AI-driven page
creation with sub-second patch times and AI-grade token compression.

---

## Resources

- `references/` — detailed examples and advanced use cases
- `scripts/` — automation scripts
- `assets/` — templates and resources
- GitHub: https://github.com/Aimino-Tech/OpenTalk2HTML-NotMD
- npm: https://www.npmjs.com/package/@aimino/opentalk2html-notmd

---

## License

GPL-3.0-only — See LICENSE in the repository.

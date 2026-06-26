---
name: builtbyecho-research
description: Use when a user asks an agent to do web research, source discovery, citation-backed reporting, page extraction, crawling, or browser-rendered research using the BuiltByEcho Research npm package. Also use when installing, verifying, or demonstrating @builtbyecho/research.
version: 0.5.2
metadata:
  openclaw:
    emoji: "🔎"
    homepage: https://github.com/BuiltByEcho/research
    requires:
      bins:
        - node
        - npm
    install:
      - id: builtbyecho-research
        kind: node
        package: "@builtbyecho/research"
        bins:
          - builtbyecho-research
          - echo-research
        label: Install BuiltByEcho Research from npm
---

# BuiltByEcho Research

Use `@builtbyecho/research` for local-first web research workflows: search, fetch, render JavaScript-heavy pages, crawl sites, extract structured fields, audit sources, save traces, and produce citation-backed reports.

## Install or run

Prefer `npx` when you only need a one-off run:

```bash
npx @builtbyecho/research --help
```

For repeated use, install globally:

```bash
npm install -g @builtbyecho/research
builtbyecho-research --help
```

Alias:

```bash
echo-research --help
```

Requires Node.js 20+.

## Optional browser setup

The package uses Playwright for render/browser escalation. If Playwright browsers are missing, install Chromium:

```bash
npx playwright install chromium
```

## Optional search key

No API key is required. For better search discovery, set a Brave API key:

```bash
export BRAVE_API_KEY="..."
```

Without `BRAVE_API_KEY`, search falls back to DuckDuckGo HTML scraping.

## Common commands

Search:

```bash
npx @builtbyecho/research search "open source deep research agents" -n 8
```

Fetch a page:

```bash
npx @builtbyecho/research fetch https://example.com --max-chars 5000
```

Render a JavaScript-heavy page:

```bash
npx @builtbyecho/research render https://example.com
```

Run a research pipeline:

```bash
npx @builtbyecho/research pipeline "research agent architecture" --expand --rounds 2 -n 8 --format markdown --trace
```

Generate a citation-backed report:

```bash
npx @builtbyecho/research report "Playwright browser automation best practices" -n 6 --rounds 2 --trace
```

Extract structured fields:

```bash
npx @builtbyecho/research extract https://example.com --schema links,headings
npx @builtbyecho/research extract https://company.example --schema emails,phones,pricing,contact_links,socials
```

Crawl a site:

```bash
npx @builtbyecho/research crawl https://docs.example.com --depth 2 --max-pages 25 --chunk
```

## Workflow guidance

1. Start with `search`, `pipeline`, or `report` depending on the user’s goal.
2. Use `--trace` for research that may need auditability or follow-up.
3. Prefer `render` or browser escalation for pages with low text, heavy JavaScript, “enable JavaScript” messages, or bot-wall/CAPTCHA-like content.
4. Treat generated prose as a first draft. Verify citations before high-stakes use.
5. Do not bypass CAPTCHA, login walls, paywalls, robots/ToS restrictions, or other access controls.

## Library API

For Node.js code:

```js
import {
  researchPipeline,
  iterativeResearchPipeline,
  toResearchReport,
  extractSchemaFromUrl,
} from '@builtbyecho/research';

const result = await iterativeResearchPipeline('Playwright MCP best practices', {
  expand: true,
  count: 6,
  rounds: 2,
});

console.log(toResearchReport(result));
```

## Vaultline integration

For research that needs durable handoff, upload the final report or trace bundle to Vaultline instead of leaving it in transient chat history.

```bash
node -e '
const fs = require("node:fs");
const { Vaultline } = require("@builtbyecho/vaultline-sdk");
const reportPath = "report.md";
const content = fs.readFileSync(reportPath, "utf8");
const vault = new Vaultline({ apiKey: process.env.VAULTLINE_API_KEY });
vault.files.upload({
  path: `research/${Date.now()}-report.md`,
  content,
  contentType: "text/markdown"
}).then(r => console.log("Vaultline fileId:", r.fileId));
'
```

Use this pattern when multiple agents or human reviewers need the same source-backed artifact.

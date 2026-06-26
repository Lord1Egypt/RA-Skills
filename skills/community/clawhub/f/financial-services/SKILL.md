---
name: financial-services
description: >
  Complete financial analysis methodology for OpenClaw. A 6-skill collection covering investment banking, commercial banking, asset management, insurance, source attribution, and standardized output. Use when performing any financial analysis, modeling, due diligence, or report generation.
metadata:
  openclaw:
    emoji: "💰"
    homepage: https://github.com/openclaw/financial-services
---

# Financial Services

金融分析方法论在 OpenClaw 平台上的完整技能集合。6 个技能协同工作，覆盖投行、商业银行、资管、保险四大金融场景。

## How This Collection Works

This is a **skill collection**. The root SKILL.md acts as the manifest. Individual skills live in subdirectories and are auto-discovered by OpenClaw via their `description` fields.

## Skills

### Core Analysis Skills
- **investment-banking** — Pitch books, CIMs, comps tables, DCF models, precedent transactions
- **commercial-banking** — Credit memos, loan underwriting, covenant analysis, spread sheets
- **asset-management** — Portfolio reporting, Brinson attribution, IC memos, performance decks
- **insurance** — Reserve review, actuarial analysis, underwriting, regulatory filings

### Foundation Skills
- **source-attribution** — Every number traces to its source. Verification checklist for financial claims.
- **excel-powerpoint-output** — Standardized formatting for financial Excel workbooks and PowerPoint decks

## Installation

```bash
clawhub install financial-services
```

Or manually:

```bash
cp -r financial-services ~/.openclaw/skills/
```

Restart OpenClaw Gateway. All 6 skills are auto-discovered.

## Requirements

- OpenClaw (any version supporting SKILL.md format)
- No additional dependencies
- For data-intensive workflows: configure MCP connectors to your data providers (FactSet, S&P Global, Morningstar, etc.)

## License

MIT-0

## Credits

Inspired by [Claude for Financial Services](https://claude.com/solutions/financial-services) by Anthropic.

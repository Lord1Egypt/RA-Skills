# 📄 doc-formatter

**Official Document Formatter Skill for Claude Code**

Automated generation of standardized Chinese official documents. Built-in national standard (GB/T 9704) formatting templates for government and enterprise settings.

[![npm version](https://img.shields.io/npm/v/doc-formatter.svg)](https://www.npmjs.com/package/doc-formatter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Cryptocxf%2Fdoc--formatter-blue)](https://github.com/Cryptocxf/doc-formatter)

## Installation

```bash
npm install -g doc-formatter
```

Then use `/doc-formatter` in Claude Code.

## Usage

| Command | Function |
|---------|----------|
| `/doc-formatter new <type>` | Interactive: fill in info, generate a complete document |
| `/doc-formatter list-templates` | List all supported document templates |
| `/doc-formatter preview <type>` | Preview a template's structure and required fields |
| `/doc-formatter export <path>` | Export generated document as Markdown |

## Supported Document Types (18)

| Template | Command | Use Case |
|----------|---------|----------|
| 📋 Notice | `notice` | Policy release, holiday notices, meeting arrangements |
| 📨 Request for Approval | `request` | Seeking approval, resource allocation |
| 📄 Report | `report` | Work reports, special reports, annual reports |
| ✉️ Official Letter | `letter` | External correspondence, invitations |
| 📝 Meeting Minutes | `minutes` | Meeting records and resolutions |
| 📑 Work Summary | `summary` | Periodic/annual summaries |
| 📊 Work Briefing | `briefing` | Weekly/monthly reports, topic briefings |
| 🎯 Work Plan | `plan` | Annual/quarterly/monthly plans |
| 📢 Proposal | `proposal` | Campaign initiatives, open letters |
| 📌 Explanation Statement | `explanation` | Issue clarification |
| 📇 Application Materials | `application` | Project/program applications |
| 🎤 Debriefing Report | `debrief` | Individual/department debriefing |
| 🧩 Special Plan | `scheme` | Implementation plans, remediation plans |
| ✅ Approval | `approval` | Official approval/endorsement |
| 📋 Meeting Notice | `meeting-notice` | Meeting convening notice |
| 🔄 Reply Letter | `reply` | Response to correspondence |
| 🏆 Commendation | `commendation` | Commending individuals/teams |
| 📰 Bulletin | `bulletin` | Work bulletins, situation reports |

## CLI Flags

| Flag | Description |
|------|-------------|
| `--title=X` | Document title |
| `--recipient=X` | Recipient/audience |
| `--author=X` | Authoring department/person |
| `--date=X` | Document date |
| `--style=concise` | Concise output style |
| `--style=detail` | Detailed output style |
| `--style=formal` | Full formal output style |

## Core Features

- **National Standard Formatting**: GB/T 9704 compliant — fonts, sizes, spacing, margins, headings, signatures, page numbers
- **Lightweight Input**: Just fill in the key points, get a complete draft
- **Standard Phrase Library**: Built-in formal vocabulary, opening/closing formulas, transitional phrases
- **18 Templates**: Covers all major Chinese official document types
- **Customizable**: Modify templates, adjust phrasing, choose output style

## Links

- **GitHub**: [https://github.com/Cryptocxf/doc-formatter](https://github.com/Cryptocxf/doc-formatter)
- **npm**: [https://www.npmjs.com/package/doc-formatter](https://www.npmjs.com/package/doc-formatter)
- **Issues**: [https://github.com/Cryptocxf/doc-formatter/issues](https://github.com/Cryptocxf/doc-formatter/issues)

## License

MIT
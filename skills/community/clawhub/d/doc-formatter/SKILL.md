---
name: doc-formatter
description: Official Document Formatter — Automated generation of standardized Chinese official documents with built-in GB/T 9704 national standard formatting, supporting 18 document types
argument-hint: [new|list-templates|preview|export] <template-type> [--title=X] [--recipient=X] [--author=X] [--date=X] [--style=concise|detail|formal]
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# 📄 Official Document Formatter Skill

**doc-formatter** is an automated Chinese official document generation tool with built-in national standard (GB/T 9704) and enterprise-general formatting specifications. Simply input your key content points, and it automatically produces a properly formatted, professionally worded, structurally complete standard document — **no manual layout adjustment or wording polishing needed**.

## Quick Start

```
User types /doc-formatter
  │
  ├─ new <template-type>      → Interactive: fill in key info, get a complete document
  ├─ list-templates           → List all supported document templates
  ├─ preview <template-type>  → Preview a template's structure and required fields
  ├─ export <file-path>       → Export the generated document as a Markdown file
  └─ (no args)                → Interactive guided template selection
```

---

## Supported Document Templates

### General Administrative Documents

| # | Template | Command ID | Use Case |
|---|----------|------------|----------|
| 1 | 📋 **Notice** | `notice` | Policy release, meeting arrangements, holiday notices |
| 2 | 📨 **Request for Approval** | `request` | Requesting approval, resource allocation, plan submission |
| 3 | 📄 **Report** | `report` | Work reports, special reports, annual reports |
| 4 | ✉️ **Official Letter** | `letter` | External correspondence, reply letters, invitations |
| 5 | 📝 **Meeting Minutes** | `minutes` | Meeting records and resolution documentation |
| 6 | 📑 **Work Summary** | `summary` | Periodic/annual/ project-specific summaries |
| 7 | 📊 **Work Briefing** | `briefing` | Weekly/monthly/quarterly briefings, topic reports |
| 8 | 🎯 **Work Plan** | `plan` | Annual/quarterly/monthly plans, project plans |
| 9 | 📢 **Proposal / Initiative** | `proposal` | Campaign initiatives, action calls, open letters |
| 10 | 📌 **Explanation Statement** | `explanation` | Issue clarification, incident explanation |
| 11 | 📇 **Application Materials** | `application` | Project applications, qualification filings, funding requests |
| 12 | 🎤 **Debriefing Report** | `debrief` | Individual/department annual debriefing |
| 13 | 🧩 **Special Plan / Scheme** | `scheme` | Implementation plans, construction plans, remediation plans |
| 14 | ✅ **Approval / Endorsement** | `approval` | Official approval, endorsement reply |
| 15 | 📋 **Meeting Notice** | `meeting-notice` | Meeting convening notice, agenda arrangement |
| 16 | 🔄 **Reply Letter** | `reply` | Response to incoming correspondence |
| 17 | 🏆 **Commendation Notice** | `commendation` | Commending advanced individuals/teams |
| 18 | 📰 **Bulletin** | `bulletin` | Work bulletins, information briefs, situation reports |

---

## Core Capabilities

### 1. Built-in National Standard (GB/T 9704) Formatting

| Element | Standard | Description |
|---------|----------|-------------|
| **Title** | No.2 FangZheng XiaoBiaoSong / HeiTi, centered | Primary heading |
| **Level-1 Heading** | No.3 HeiTi, left-aligned | 一、二、三、… |
| **Level-2 Heading** | No.3 KaiTi, 2-char indent | （一）（二）（三）… |
| **Level-3 Heading** | No.3 FangSong, 2-char indent | 1. 2. 3. … |
| **Body** | No.3 FangSong_GB2312, 2-char indent | Fixed line spacing 28pt |
| **Signature** | No.3 FangSong, right-aligned | Department name + date |
| **Margins** | Top 3.7cm, Bottom 3.5cm, Left 2.8cm, Right 2.6cm | A4 paper |
| **Page Numbers** | Bottom center, - 1 - format | Starting from body |
| **Attachments** | No.3 FangSong, blank line below body | "附件：1. ×××" |
| **CC List** | No.4 FangSong | Bottom of signature page |

### 2. Lightweight Input, Intelligent Generation

Users only need to provide **core information elements** — the system automatically organizes them into a complete document:

```
Input Example:
  /doc-formatter new notice
  Title: About 2026 Dragon Boat Festival Holiday Arrangement Notice
  Audience: All company employees
  Key Content: June 12-14 off, June 15 back to work
  Department: General Administration Department
  Date: June 5, 2026

Output:
  Automatically generates a complete notice with formatted title,
  salutation, body (purpose + specific arrangements + requirements + signature)
```

### 3. Built-in Standard Phrase Library

- **Formal document vocabulary**: 兹有, 鉴于, 经研究, 现就, 特此, 妥否, 请批示, 特此函达, 此复
- **Common sentence patterns**: Opening phrases, transitional connectors, closing statements, request language, approval language
- **Auto-avoidance**: Colloquial expressions, internet slang, informal abbreviations, emotional language
- **Style adaptation**: Internal reporting / external submission / higher-authority filing — automatically matches tone and formality level

### 4. Flexible Customization

- **Template tweaks**: Add, modify, or remove content sections in any template
- **Style presets**: "Formal", "Concise", and "Detailed" output styles
- **Paragraph restructuring**: Freely reorder content paragraphs
- **Personalized signature**: Custom signatory name, department, and date format

### 5. One-Click Multi-Format Export

- Markdown format (default, instant preview)
- Copy-paste ready for Word/WPS
- Inline formatting annotations to guide final layout

---

## Usage

### Interactive Document Generation

```bash
# 1. Choose a template
/doc-formatter new notice

# 2. System will guide you through these fields (one at a time)
#    - Document title
#    - Recipient / primary audience
#    - Purpose / background
#    - Key content points
#    - Requirements / related matters
#    - Signing department
#    - Date

# 3. System outputs complete document + layout notes
```

### One-Step Generation (when all info is ready)

```bash
/doc-formatter new request --title="关于审批2026年信息化建设项目的请示" --recipient="公司领导" --author="信息技术部"
/doc-formatter new summary --title="2026年上半年工作总结" --author="市场部"
/doc-formatter new minutes --title="关于AI大模型平台建设推进会的会议纪要"
```

### View Templates

```bash
# List all templates
/doc-formatter list-templates

# Preview a specific template structure
/doc-formatter preview notice
/doc-formatter preview report
```

### Export

```bash
# Export as Markdown file (saves to desktop by default)
/doc-formatter export ./2026年工作汇报.md
```

---

## Execution Flow

### Mode 1: `new` — Generate Document

```
1. User specifies template type (e.g. notice / report / request)
2. Load corresponding template config (structure + format spec + phrase library)
3. Interactively guide user to fill in key info
   - Auto-complete: format hints, examples, optional fields
   - Validate required field completeness
4. Apply built-in formatting engine per GB/T 9704 standard
   - Set heading levels with font/size markers
   - Body auto-format: FangSong font + 2-char indent
   - Signature right-aligned + standardized date
5. Apply standard formal language for transitions
   - Opening: matches template type ("根据……" "为……" "鉴于……")
   - Closing: matches document type ("特此通知" "妥否，请批示" "此复")
   - Transition sentences: natural flow between paragraphs
6. Output complete document (Markdown, with formatting notes)
7. Optionally modify, adjust, or polish upon user request
```

### Mode 2: `list-templates` — View Template List

```
1. Scan all registered templates
2. Group by category (Admin / Reports / Applications / Correspondence)
3. Brief description of each template's use case
```

### Mode 3: `preview` — Preview Template Structure

```
1. Locate specified template config
2. Display:
   - Document type characteristics and usage conventions
   - Standard framework (required + optional sections)
   - Field descriptions
   - Phrase examples
```

---

## Output Example

```
┌─────────────────────────────────────────────────────────────────┐
│                         📄 Notice                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│            关于2026年端午节放假安排的通知                        │
│                                                                 │
│公司各部门：                                                      │
│                                                                 │
│  根据《国务院办公厅关于2026年部分节假日安排的通知》，结合我       │
│公司实际情况，现将2026年端午节放假安排通知如下：                  │
│                                                                 │
│  一、放假时间                                                   │
│  2026年6月12日（星期五）至6月14日（星期日）放假，共3天。         │
│  6月15日（星期一）正常上班。                                    │
│                                                                 │
│  二、有关要求                                                   │
│  （一）各部门在放假前做好安全检查工作，关闭电源、门窗，            │
│确保办公场所安全。                                               │
│  （二）值班人员严格遵守值班制度，保持通讯畅通，如遇突发            │
│情况及时上报。                                                   │
│  （三）全体员工注意节日期间出行安全。                            │
│                                                                 │
│  特此通知。                                                     │
│                                                                 │
│                                        综合管理部               │
│                                        2026年6月5日              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ 📋 Layout: Title No.2 HeiTi centered | Body No.3 FangSong       │
│    2-char indent | Line spacing 28pt | Signature right-aligned   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Notes

- Generated documents are **drafts** — please review manually before official stamping
- Formatting is based on Markdown; fine-tune after copying to Word/WPS if needed
- **Classified documents are not suitable** for this tool — use your organization's secure channels
- Templates can be customized; see the `references/template-library.md` file
- To add new template types, configure them in `references/template-library.md`
- Output style flags: `--style=concise` (brief), `--style=detail` (detailed), `--style=formal` (full formal)
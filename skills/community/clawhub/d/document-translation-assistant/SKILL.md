---
name: Document Translation Assistant
slug: document-translation-assistant
description: Translate technical & legal documents while preserving original formatting, terminology consistency, and domain context.
tags: [translation, document, localization, markdown, bilingual, terminology, formatting]
version: 1.0.0
license: MIT-0
---

# Document Translation Assistant (文档翻译助手)

Translate documents without breaking them. Preserve markdown structure, code blocks, tables, links, and image references while maintaining terminology consistency across the entire document — purpose-built for technical and legal content where accuracy matters more than fluency.

## Core Capabilities

- **Format-preserving translation**: Maintain markdown syntax, HTML tags, YAML frontmatter, code fences, tables, and link references exactly as-is through translation
- **Terminology consistency engine**: Auto-extract domain terms → build glossary → enforce consistent translation across the entire document
- **Multi-format support**: MD, DOCX, PDF (with text layer), HTML, plain text — translate while preserving the original format
- **Bilingual output**: Side-by-side bilingual view (original + translation) for review, or translated-only for publication
- **Term glossary management**: Build and persist terminology dictionaries per project/domain for reuse across multiple documents
- **Context-aware segmentation**: Translate paragraph-by-paragraph but re-read the full document post-translation to fix context breaks from chunking
- **Domain mode switching**: Technical (API docs, README), Legal (contracts, ToS), Marketing (landing pages, blog posts), General

## Workflow (9 Steps)

### Step 1: Document Ingestion
**Input**: User provides:
- **Source document**: File upload (MD/DOCX/PDF/HTML), URL, or pasted text
- **Source language**: Auto-detect or specify
- **Target language**: Required
- **Domain mode** (optional): `tech` | `legal` | `marketing` | `general`
- **Output preference**: `bilingual` (side-by-side) | `translated-only` | `both`

**Output**: Parsed document with structure tree (headings, paragraphs, code blocks, tables, lists, links, images).
**Logic**: Auto-detect language with confidence score. If confidence <90%, confirm with user.

### Step 2: Structure Preservation
**Input**: Parsed document.
**Action**: Build a structure tree identifying translatable vs non-translatable nodes:

| Node Type | Translatable | Example |
|-----------|-------------|---------|
| Headings | ✅ Translate | `## Getting Started` → `## 快速开始` |
| Paragraph text | ✅ Translate | Body text, descriptions |
| List items | ✅ Translate | Bullet points, numbered lists |
| Table cell text | ✅ Translate | Cell content (not table structure) |
| Code blocks | ❌ Preserve | All code, commands, config |
| Inline code | ❌ Preserve | `npm install`, `const x = 1` |
| Links | ❌ Preserve URLs | `[text](url)` — translate text, keep URL |
| Images | ❌ Preserve | `![alt](url)` — translate alt text, keep URL |
| Frontmatter | ⚠️ Selective | Translate `description`, keep `slug`/`tags` |
| HTML tags | ❌ Preserve | `<div>`, `<span>` — translate text content only |
| Placeholders | ❌ Preserve | `{{variable}}`, `%s`, `{0}` |

**Output**: Structure tree with translatable segments marked for processing.

### Step 3: Terminology Extraction
**Input**: Translatable segments + domain mode.
**Action**: Extract domain-specific terminology:
- **Tech mode**: API terms, function names, CLI commands, error messages, protocol names
- **Legal mode**: Legal terms (indemnification, force majeure, liquidated damages, 不可抗力, 违约金)
- **Marketing mode**: Brand names, slogans, product names, CTAs
- **General mode**: Standard extraction of repeated nouns and phrases

**Output**: Candidate term list with occurrence count and context snippets.

### Step 4: Terminology Glossary Building
**Input**: Candidate terms + user input.
**Action**: Present extracted terms to user for confirmation:
```
Extracted 23 specialized terms:

| # | Source Term | Occurrences | Suggested Translation | Your Translation |
|---|------------|-------------|----------------------|-------------------|
| 1 | 微服务 | 15 | microservices | [confirm/edit] |
| 2 | 熔断器 | 8 | circuit breaker | [confirm/edit] |
| 3 | 服务降级 | 5 | service degradation | [confirm/edit] |
```

User can:
- Confirm suggestions (accept all default)
- Override specific translations
- Add missing terms manually
- Import existing glossary from previous session

**Output**: Finalized terminology glossary. Saved per project for reuse.
**Logic**: Terms with multiple possible translations flag for user review. Common terms with single standard translation auto-apply.

### Step 5: Segment-Level Translation
**Input**: Translatable segments + terminology glossary + domain mode.
**Action**: Translate each segment with:
- Exact glossary term substitution (highest priority)
- Domain-appropriate tone (tech: precise, legal: formal, marketing: engaging)
- Format markers preserved: `**bold**`, `*italic*`, `` `code` ``
- Placeholder preservation: `{{name}}`, `%d`, positional arguments
- Numerical values: convert only when culturally appropriate (e.g., currency, date formats per user preference)

**Output**: Translated segments with format-preservation validation.
**Logic**: Process in chunks of ~5 segments to maintain local context. Large documents processed in batches with progress indicator.

### Step 6: Terminology Consistency Check
**Input**: All translated segments + glossary.
**Action**: Post-translation scan:
1. For each glossary term, verify the correct translation appears in ALL occurrences
2. Detect inconsistent translations of the same source term (e.g., "微服务" translated as both "microservices" and "micro-services")
3. Flag missed terms (glossary term found in source but translation not used)

**Output**: Consistency report:
```
✅ Terminology check: 23/23 terms consistent
⚠️ Inconsistency found: "负载均衡" → "load balancing" (18 occurrences)
                                          → "load balancer" (2 occurrences — FIXED)
```

### Step 7: Context Coherence Review
**Input**: Translated full document.
**Action**: Read the entire translated document to fix context breaks:
- Pronouns referencing entities from previous paragraphs
- Cross-references ("as mentioned above" → adjust for translation)
- Section-to-section flow and transitions
- Heading consistency across the document hierarchy
- Repeated instruction patterns (every "Note:" should read naturally)

**Output**: Coherence-adjusted translation.
**Logic**: AI reads full translated document as a human editor would, flagging sections that read disjointed.

### Step 8: Output Generation
**Input**: Coherent translated document.
**Action**: Generate output in requested format(s):

**Bilingual mode (default for review)**:
```markdown
## Getting Started | ## 快速开始

This guide will help you set up the project. | 本指南将帮助您搭建项目。

1. Clone the repository | 1. 克隆仓库
   `git clone https://...` |    `git clone https://...`
```

**Translated-only mode** (for publication):
The full document in target language, preserving all formatting.

**Output**: File(s) saved in same or specified directory.

### Step 9: Glossary Persistence
**Input**: Finalized glossary + project identifier.
**Action**: Save terminology glossary for future reuse:
```json
{
  "project": "user-service-docs",
  "domain": "tech",
  "source_lang": "zh",
  "target_lang": "en",
  "terms": {
    "微服务": "microservices",
    "服务网格": "service mesh",
    "熔断器": "circuit breaker"
  },
  "updated": "2026-06-17"
}
```

**Output**: Saved glossary. Next translation for this project auto-loads it.
**Logic**: Glossary stored locally. User controls save/delete/export.

## Sample Prompts

### Prompt 1: Tech README Translation
**User**: "帮我把这个中文README翻译成英文 [upload: README_zh.md]"
**Expected Output**: Bilingual view with all code blocks, commands, and links preserved. Terminology glossary auto-extracted (微服务→microservices, 部署→deploy) and applied consistently.

### Prompt 2: Legal Contract Translation
**User**: "这份中文合同需要翻译成英文给海外同事看，保持法律术语准确 [upload: contract_zh.docx]"
**Expected Output**: Translated DOCX with formal legal tone. Glossary terms: 甲方→Party A, 违约责任→Breach of Contract, 不可抗力→Force Majeure. Warning: "This is a translation for reference. Not a certified legal translation."

### Prompt 3: Bilingual Product Docs
**User**: "我们的产品文档需要中英双语版本，以后每次更新都要同步翻译 [path: ~/docs/]"
**Expected Output**: All markdown files in the docs/ directory translated with glossaries saved. Future runs: detect changed files only, translate diffs, maintain consistency.

### Prompt 4: Consistency Fix
**User**: "之前翻译的文档里同一个术语翻了好几种，帮我统一 [upload: translated_zh.md]"
**Expected Output**: Scan for inconsistent terms → present conflict list → user chooses preferred translation → apply uniformly. Report: "Fixed 14 inconsistencies across 'API网关' (was: api-gateway, API Gateway, ApiGateway → now: API Gateway)."

### Prompt 5: Format Verification
**User**: "翻译后帮我检查文档格式有没有被破坏 [upload: translated.md + original.md]"
**Expected Output**: Structure diff: heading count, code block count, link count, table row count. "All structural elements preserved (42 headings, 7 code blocks, 12 links, 3 tables). ✅"

### Prompt 6: Multi-Language Package
**User**: "这个开源项目的README需要翻译成中文、日文、韩文 [upload: README.md]"
**Expected Output**: Three translated files (README_zh.md, README_ja.md, README_ko.md) with per-language glossaries. Note: "Japanese and Korean translations may have lower confidence—review recommended."

## Real Task Examples

### Example 1: Open Source Project Localization
**Scenario**: Maintainer wants to make a Chinese open source project accessible internationally.
**Input**: "帮我翻译整个项目的文档：README, CONTRIBUTING, 和 docs/ 下面的所有文件"
**Steps**:
1. Scan project: 23 markdown files, ~15K words total.
2. Extract terminology across all files: build project-wide glossary.
3. Translate file-by-file maintaining cross-document consistency.
4. Special handling: code of conduct, changelog dates, contribution workflow descriptions.
5. Post-translation: verify all internal links still resolve.
**Output**: Complete English docs/ directory + bilingual README. Glossary saved as `.translation-glossary.json` in project root.

### Example 2: Legal Document for Cross-Border Team
**Scenario**: Chinese company shares NDA with US partner. Both sides need to understand the content.
**Input**: "翻译这份保密协议，法律术语要准确，格式不能乱 [upload: nda_zh.docx]"
**Steps**:
1. Parse DOCX: 8 pages, article-numbered structure.
2. Domain: legal mode. Extract 35 legal terms.
3. User confirms glossary: 保密信息→Confidential Information, 接收方→Receiving Party, 管辖法律→Governing Law.
4. Translate with formality preservation. Preserve article numbering (第一条→Article 1).
5. Bilingual output: left column Chinese, right column English.
**Output**: Bilingual DOCX. Disclaimer: "This translation is for reference only. The Chinese version shall prevail in case of discrepancy."

### Example 3: Continuous Documentation Sync
**Scenario**: Engineering team updates docs weekly; translations lag behind.
**Input**: "我们每周更新中文文档，每次帮我翻译新增和修改的部分 [path: ~/docs/]"
**Steps**:
1. Load saved glossary from `~/docs/.translation-glossary.json`.
2. Diff against last translated version: detect new/modified/deleted files.
3. Translate only changed sections (not full re-translation).
4. Update translation files incrementally.
5. Report: "3 files changed, 2 new. 412 words translated. Consistency: 100% with existing glossary."
**Output**: Synced translation files + changelog of what was translated.

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `translation-assistant.sh parse README_zh.md` — parses document, detects structure and language
2. **Step 2**: Run `translation-assistant.sh glossary README_zh.md` — extracts and reviews terminology glossary
3. **Step 3**: Run `translation-assistant.sh translate README_zh.md en --domain tech` — generates translated document with format preservation

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| Document >50K words | Process in batches with progress indicator; warn of ~X minutes processing time |
| Scanned/image PDF (no text layer) | Trigger OCR; warn of lower translation quality due to OCR errors |
| Code-heavy document (>50% code) | Skip code blocks; translate only comments and prose; note low text ratio |
| Mixed language document | Detect primary language; flag mixed sections for special handling |
| Document with embedded JSON/YAML | Preserve JSON/YAML structure; translate only string values if user requests |
| Unsupported output format requested | Offer conversion path (e.g., "Can output MD, DOCX, HTML. For PDF, convert after.") |
| Zero domain terms detected | Skip glossary step; proceed with direct translation in general mode |
| Target language is same as source | Warn: "Source and target are the same language. Continue with proofreading mode?" |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-PARSE-FAIL | Document structure unparseable | Offer plain text fallback (loses formatting); warn user |
| E-FORMAT-CORRUPT | Post-translation format validation fails | Show diff of structural elements; offer manual fix or revert |
| E-GLOSSARY-CONFLICT | Same term has conflicting translations in saved glossary | Present conflict; ask user to choose or merge |
| E-OCR-FAIL | OCR on scanned document produces garbage | Return original images + note; suggest better scan quality |
| E-ENCODING | Document has non-standard encoding | Auto-detect and convert to UTF-8; warn if characters lost |
| E-TERM-OVERLAP | Domain term is also a common word (e.g., "bug" in tech) | Flag as ambiguous; ask user to clarify context or accept heuristic |
| E-TRANSLATION-LOW-CONFIDENCE | AI translation confidence below threshold for a segment | Mark segment with ⚠️ "Low confidence" annotation in output |

## Security Requirements

- **Document confidentiality**: Document content processed locally or via LLM API. Warn user before sending to external API. Offer local-only translation mode for sensitive documents (lower quality, fully private).
- **No document storage**: Source and translated documents not persisted beyond current session unless user explicitly saves.
- **Legal translation disclaimer**: Every legal translation must include: "⚠️ This is an AI-generated translation for reference only. It is NOT a certified legal translation. Consult a qualified legal translator for legally binding documents."
- **No PII in glossary**: Strip personal identifiers, account numbers, and other PII from extracted terminology lists.
- **Copyright respect**: Do not translate documents that are clearly copyrighted and not owned by the user without explicit permission statement.
- **Glossary privacy**: Saved glossaries stored locally only. Never upload project-specific terminology to external services.
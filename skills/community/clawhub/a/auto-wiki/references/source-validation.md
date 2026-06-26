# Information Source Validation

## Source Credibility Grading

Each piece of information is labeled with source type, different types correspond to different confidence defaults:

| Source Type | Tag | Default confidence | Description |
|-------------|-----|-------------------|-------------|
| Primary source | `[primary]` | high | Own writings, official documents, raw data, meetings personally attended |
| Authoritative secondary | `[authoritative-secondary]` | high | Authoritative media reports, academic papers, regulatory releases |
| Regular secondary | `[secondary]` | medium | Industry research reports, analysis articles, third-party compilations |
| Hearsay | `[hearsay]` | low | Reprocessed content, social media discussions, unsourced info |
| Inference | `[inference]` | low | Conclusions derived by Agent or user based on existing info |
| Oral | `[oral]` | medium | User oral account, meeting notes, unrecorded conversations |

### Labeling in Source Summary Pages

```markdown
---
title: MOHRSS Enterprise Annuity New Regulations
type: source
source_type: primary             # Source type
source_origin: MOHRSS official website      # Source origin
source_date: 2026-04-01          # Original material date
source_url: ""                   # Source URL (if available)
---

## Key Information

- [primary] Enterprise annuity portable transfer new regulations released...
- [primary] Trustee admission threshold raised to...
```

### Labeling in Entity/Concept Pages

When referencing sources of different credibility levels, label in body:

```markdown
## Assets Under Management

By end of 2025, AUM reached 120 billion yuan. [primary] (Source: [[2026-04-06-policy-doc]])

Market ranking approx 3rd. [secondary] (Source: [[2025-industry-report]], non-official data)
```

## Source Blacklist

The following channels are not used as independent sources (can be clues but not cited):

| Channel | Reason |
|---------|--------|
| Zhihu | Heavy content washing, high information distortion rate |
| WeChat Official Accounts | Closed ecosystem, unverifiable, heavy second-hand retelling |
| Baidu Baike/Baidu Zhidao | Outdated and unreliable information |
| Unsourced aggregated content | Untraceable, unauditable |

**Acceptable Chinese channels**: 36Kr, GeekPark, LatePost, Caixin, CBN, Huxiu, SSPAI, Synced, regulatory official websites, listed company announcements.

## Tool Dependency Check

### Environment Check on First Use

Agent checks available tools in user environment on first ingest execution:

```
┌─────────────────────────────────────────────────────────┐
│ Knowledge Compiler · Environment Check                   │
│                                                          │
│ ✅ File I/O    — Can create and edit wiki pages          │
│ ✅ Local Search — Can grep wiki content                  │
│                                                          │
│ ⚠️ Following capabilities depend on your configuration:  │
│ {?} Web Search — Requires WebSearch tool or search MCP   │
│ {?} Web Fetch  — Requires WebFetch tool                  │
│ {?} PDF Read   — Requires Agent PDF support (Claude Code)│
│ {?} Domain Data — Requires corresponding domain data MCP │
│                                                          │
│ 📝 Current Mode:                                         │
│ • User provides source files → ✅ Available anytime      │
│ • Agent autonomous search → Requires search tools        │
└─────────────────────────────────────────────────────────┘
```

### Two Work Modes

| Mode | Required Tools | Description |
|------|---------------|-------------|
| **Passive Mode** | Only file I/O | User provides source files, Agent compiles into wiki. Zero dependencies |
| **Active Mode** | Search + Web fetch | Agent autonomously searches info, then ingests. Requires MCP/WebSearch |

**Skill defaults to passive mode**—user drops files, Agent compiles. Doesn't assume user has any search tools.

**When user says "research XX" but doesn't provide source files**:

```
Agent: How would you like me to obtain materials?

1. You provide files/text → I compile directly (recommended)
2. I search autonomously → Need to confirm you have:
   - WebSearch or search MCP tools
   - WebFetch (read web content)
   If not, I cannot autonomously obtain materials.
```

### Search Tool Adaptation

If user has search tools, Agent's ingest flow expands to:

```
1. Create search plan by research topic (what to search, where to search)
2. Execute search, get candidate source list
3. Grade sources by credibility, prioritize primary/authoritative sources
4. Execute standard ingest flow for each valuable source
5. Record search keywords and filtering process in source summary page
```

**Key principle: Search is means to obtain source files, doesn't change ingest core logic (read old, compare new, modify old).**

### Deep-Dive Search Source Labeling

When sources are obtained by deep-dive pipeline's automated search, the source summary page needs additional deep-dive metadata:

```yaml
---
title: Alpha Corp 2025 Annual Report Summary
type: source
source_type: secondary     # Graded by actual content, not affected by search method
source_origin: Caixin
source_date: 2025-06-15
source_url: "https://..."
deep_dive_meta:            # deep-dive specific fields
  search_query: "Alpha Corp enterprise annuity annual report 2025"
  gap_filled: "single_source:alpha-corp"
  search_date: 2026-04-09
---
```

**Confidence ceiling rules**:
- Search-sourced content has confidence ceiling of medium, unless source qualifies as "primary" or "authoritative-secondary"
- Multiple search sources corroborating the same conclusion can raise confidence to high
- Source's source_type is still graded by standard criteria, not affected by acquisition method (search vs user-provided)

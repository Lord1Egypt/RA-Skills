# Data Validation Protocol

> Prevent erroneous data from polluting the wiki. Verifiable data must be verified; unverifiable must be labeled.

## Core Principles

**The wiki is a knowledge asset, not a trash bin.** Once erroneous data enters the wiki, it gets referenced by subsequent queries and treated as "existing conclusion" by other ingests—errors compound. Must gate at the entrance.

## Validation Timing

Insert validation step in the ingest flow, **after reading source file, before writing to wiki**:

```
Read source → Extract key claims
    ↓
Classify: verifiable vs unverifiable
    ↓
Verifiable → Cross-validate with tools → Pass/Fail/Unable to verify
    ↓
Write to wiki (with validation label)
```

## Identifying Verifiable Data

The following claim types should attempt validation. **Specific tools depend on available MCP/tools in user environment**—the table below shows common mappings, not hard requirements:

| Data Type | Example | Common Validation Tools (environment-dependent) |
|-----------|---------|------------------------------------------------|
| Listed company financials | Revenue, profit, ROE | Financial data MCP (e.g., tushare, ifind, wind) |
| Fund/annuity scale | AUM, shares | Financial data MCP |
| Macro indicators | GDP, CPI, PMI | Financial data MCP |
| Regulatory document numbers | MOHRSS [2026] No.XX | WebSearch |
| Company basic info | Founding date, registered capital, legal rep | Financial data MCP / WebSearch |
| Industry statistics | Market size, growth, share | WebSearch / Industry data MCP |
| Dates and events | "Released March 2026" | WebSearch |

**Tool discovery**: Agent confirms available tools via environment check (see `source-validation.md`) on first ingest. Without corresponding tools, that data type is labeled `verified: false`, not blocking ingest.

**Unverifiable claims**: Opinions, analysis, predictions, inferences, subjective evaluations. Skip validation; label per source-validation.md's source grading.

## Validation Flow

### Step 1: Extract Verifiable Claims

Identify factual claims with specific numbers, dates, document numbers from source files:

```
Source text:
"By end of 2024, China's enterprise annuity fund cumulative scale reached 3.2 trillion yuan, covering 128,000 enterprises"

Extract 2 verifiable claims:
- Claim A: Enterprise annuity cumulative scale 3.2 trillion (by end 2024)
- Claim B: Covering 128,000 enterprises (by end 2024)
```

### Step 2: Attempt Validation

Use available tools by priority:

```
1. Professional data MCP (e.g., financial, medical, legal domain APIs): Has API → Query directly
2. WebSearch: Search for official data from same period
3. Wiki cross-check: See if other pages have related data
4. No tools available: Skip, label unverified
```

### Step 3: Determine Result

| Result | Action | frontmatter Label |
|--------|--------|-------------------|
| **verified** — Tool data consistent (error < 5%) | Normal ingest | `verified: true` |
| **disputed** — Tool data inconsistent | **Pause**, show difference, let user decide | After user confirmation: `verified: user-confirmed` |
| **unverifiable** — No tool or data not covered | Normal ingest | `verified: false` |
| **partial** — Some claims verified, some not | Label individually | Mixed labels |

### User Interaction on disputed

Example below using financial domain; replace with user's target domain and tools in actual execution:

```
⚠️ Data validation found discrepancy:

Claim: "XX fund cumulative scale reached 3.2 trillion yuan (end 2024)"
Data tool query result: 3.58 trillion yuan (end 2024)
Difference: -10.6%

Possible causes:
- Source file data error
- Different statistical scope
- Data tool update delay

Please choose:
1. Use tool-verified data (3.58 trillion) → Replace source file data, then ingest
2. Use source file data (3.2 trillion) → Label user-confirmed, then ingest
3. Record both → Ingest as contested
4. Skip this claim → Skip this statement
```

## Validation Labels in Pages

Label validation status in entity/concept pages:

```markdown
## Fund Scale

By end of 2024, XX fund cumulative scale reached 3.58 trillion yuan.
✅ verified (data tool query 2025-01-15)
(Source: [[2026-04-06-source-doc]], original data 3.2 trillion corrected by tool)

## History

- ~~Cumulative scale 3.2 trillion yuan~~ (Source: [[2026-04-06-source-doc]] original, corrected to 3.58 trillion by tool)
```

## Tool Availability

| Scenario | With Tools | Without Tools |
|----------|-----------|---------------|
| Professional domain data | Corresponding MCP auto-validation | Label unverified, suggest manual user confirmation |
| Public info | WebSearch cross-validation | Label unverified |
| Internal data (oral/meeting) | Unable to validate | Label source_type: oral, confidence: medium |

**Skill in passive mode (no search tools)**: All data labeled `verified: false`, relying on source-validation.md's source grading for credibility reference. Doesn't block ingest, but labels "unverified" beside each number.

## Relationship with ingest-protocol

Validation inserted between Step 1 and Step 2 of ingest-protocol.md:

```
Step 1: Read source file, extract key information
Step 1.5: [Data Validation] Extract verifiable claims → Cross-validate with tools → Determine result
Step 2: Search existing wiki
Step 3: Compare old vs new page by page
...
```

If Step 1.5 finds disputed data and pauses, continue Step 2 after user confirmation.

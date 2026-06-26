---
name: hallucination-detector
description: Detect and flag hallucinations in LLM outputs by cross-referencing claims against source documents, code, and verifiable data. Essential for RAG pipelines and AI content review.
metadata:
  tags: ["ai", "llm", "hallucination", "rag", "quality", "factcheck"]
---

# Hallucination Detector

Detect and flag hallucinations in LLM-generated content by cross-referencing claims against source documents, codebase facts, API documentation, and verifiable data. Use when reviewing AI-generated documentation, code comments, summaries, or any content that needs factual accuracy.

## Usage

```
"Check this AI-generated summary for hallucinations against the source docs"
"Verify the code documentation matches the actual implementation"
"Detect hallucinations in this RAG pipeline output"
"Fact-check this AI-generated API reference"
"Review these generated release notes for accuracy"
```

## How It Works

### 1. Claim Extraction

Parse the LLM output and identify verifiable claims:

- **Factual assertions**: "The function accepts 3 parameters", "The API returns JSON"
- **Numerical claims**: "Performance improved by 40%", "Supports up to 10,000 connections"
- **Reference claims**: "As documented in RFC 7231", "According to the README"
- **Code claims**: "The `processOrder()` function handles refunds", "Uses AES-256 encryption"
- **Temporal claims**: "Added in version 2.3", "Deprecated since 2024"
- **Relational claims**: "Module A depends on Module B", "Function X calls Function Y"

### 2. Source Grounding

For each claim, identify and query the ground truth source:

**Code verification:**
```bash
# Verify function exists and has claimed signature
grep -rn "function processOrder\|def processOrder\|processOrder(" src/
# Verify parameter count
ast-grep --pattern 'function processOrder($$$)' src/
# Verify dependency relationship
grep -rn "import.*from.*moduleB\|require.*moduleB" src/moduleA/
```

**Documentation verification:**
```bash
# Check if referenced section exists
grep -rn "## Configuration" docs/
# Verify version claims
git log --oneline --all --grep="processOrder" | head -5
git tag --contains $(git log --format=%H -1 --all -- src/processOrder.ts)
```

**API verification:**
```bash
# Verify endpoint exists and returns claimed schema
grep -rn "router\.\(get\|post\|put\|delete\)" src/routes/ | grep "orders"
# Check response schema
grep -A 20 "res.json\|res.send" src/routes/orders.ts
```

### 3. Hallucination Classification

Each detected issue is classified:

- 🔴 **Fabrication**: Claim has no basis in source material (made up entirely)
  - Example: "The `calculateTax()` function" when no such function exists
- 🟠 **Contradiction**: Claim directly contradicts source material
  - Example: "Returns a string" when function actually returns a number
- 🟡 **Exaggeration**: Claim overstates or embellishes source facts
  - Example: "Handles millions of requests" when docs say "tested to 10K"
- 🔵 **Outdated**: Claim was true but is no longer accurate
  - Example: "Uses Express.js" when codebase migrated to Fastify
- ⚪ **Unverifiable**: Claim cannot be checked against available sources
  - Example: "Industry best practice" with no citation

### 4. Confidence Scoring

Each claim gets a confidence score:

- **Verified** (✅ 90-100%): Claim matches source material exactly
- **Likely correct** (🟢 70-89%): Claim is consistent but not directly verifiable
- **Uncertain** (🟡 40-69%): Partial match or ambiguous source
- **Likely hallucinated** (🟠 10-39%): Contradicts or unsupported by sources
- **Confirmed hallucination** (🔴 0-9%): Demonstrably false

### 5. RAG Pipeline Analysis

When used in RAG context, also check:

- **Retrieval accuracy**: Were the right chunks retrieved for the query?
- **Attribution fidelity**: Does the output actually reflect the retrieved chunks?
- **Chunk boundary issues**: Was a claim split across chunks, losing context?
- **Source mixing**: Were facts from different sources incorrectly combined?
- **Inference vs citation**: Is the model inferring beyond what sources state?

### 6. Pattern Detection

Identify common hallucination patterns:

- **Confident fabrication**: High-confidence claims about nonexistent features
- **Plausible details**: Made-up but realistic-sounding specifics
- **Version confusion**: Mixing features from different software versions
- **Name substitution**: Using similar but incorrect function/class names
- **Count inflation**: Overstating numbers, capabilities, or performance
- **False relationships**: Inventing connections between unrelated components

## Output

```
## Hallucination Analysis Report

**Content reviewed:** AI-generated API documentation (2,400 words)
**Claims extracted:** 47
**Verification results:**

| Status | Count | % |
|--------|-------|---|
| ✅ Verified | 31 | 66% |
| 🟢 Likely correct | 6 | 13% |
| 🟡 Uncertain | 3 | 6% |
| 🔴 Hallucinated | 7 | 15% |

### 🔴 Confirmed Hallucinations

1. **"The /api/users endpoint supports bulk operations via POST /api/users/bulk"**
   - Reality: No bulk endpoint exists in routes/users.ts
   - Type: Fabrication
   - Fix: Remove bulk operations section entirely

2. **"Authentication uses OAuth 2.0 with PKCE flow"**
   - Reality: Uses session-based auth (express-session + passport-local)
   - Type: Contradiction
   - Fix: Replace with actual auth mechanism description

3. **"Rate limited to 1000 requests per minute per API key"**
   - Reality: No rate limiting configured (no rate-limit middleware found)
   - Type: Fabrication
   - Fix: Remove rate limiting claims or implement the feature

4. **"Response includes pagination metadata with total_count, page, and per_page"**
   - Reality: API returns raw arrays without pagination
   - Type: Fabrication
   - Fix: Document actual response format

[3 more...]

### 🟡 Uncertain Claims (need human review)

5. **"Handles up to 5,000 concurrent connections"**
   - No load testing data found — may be true but unverified
   
### 📊 Hallucination Hotspots
- Performance claims: 3/4 hallucinated (75%)
- Feature descriptions: 2/18 hallucinated (11%)
- Security section: 2/8 hallucinated (25%)

### 💡 Recommendations
- Performance section needs complete rewrite with actual benchmarks
- Security section should be reviewed by the auth team
- Consider adding integration tests that validate API documentation accuracy
```

## Integration

- **CI pipeline**: Run on generated docs before merge
- **RAG applications**: Post-processing step to filter hallucinated content
- **Content review**: Batch-check AI-generated articles or documentation
- **Code review**: Verify AI-generated code comments match implementation

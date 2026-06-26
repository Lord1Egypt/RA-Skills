# Customer Research — Quick Start

## 30-Second Overview

Validate product ideas with real customer data before building marketing campaigns.

**What it does:** Mine Reddit/forums → Validate personas → Generate interview scripts → Feed insights to content strategy

---

## Common Workflows

### 1. Validate a New Product Idea

**Goal:** Test if "FIRE Calculator" has real demand

```bash
cd /Users/clawdiri/.openclaw/workspace

# Step 1: Mine Reddit for pain points
./skills/customer-research/scripts/reddit-miner.sh \
  --subreddit "financialindependence" \
  --query "retirement calculator" \
  --limit 50

# Step 2: Create persona (or use example)
# Edit: skills/customer-research/examples/fire-enthusiast-persona.json

# Step 3: Validate persona assumptions
./skills/customer-research/scripts/persona-validator.sh \
  --persona-file skills/customer-research/examples/fire-enthusiast-persona.json

# Step 4: Generate interview script for weak assumptions
./skills/customer-research/scripts/interview-generator.sh \
  --persona "FIRE enthusiast, 35, tech worker" \
  --problem "retirement calculators too conservative"
```

**Output:**
- Reddit insights in `data/research/reddit-*.json`
- Validation report with ✅/⚠️/❌ for each assumption
- Interview script ready to use

**Next:** Feed validated pain points to Ogilvy for content strategy

---

### 2. Monitor Competitor Sentiment

**Goal:** Track what customers say about Personal Capital

```bash
./skills/customer-research/scripts/competitor-scraper.sh \
  --product "Personal Capital" \
  --sources "reddit"
```

**Output:** `data/research/competitor-personal-capital-*.json`

**What to look for:**
- Top complaints (your opportunity)
- Praised features (table stakes)
- Pricing sentiment (how much room you have)

---

### 3. Generate Customer Interview Guide

**Goal:** Prep for user interviews

```bash
./skills/customer-research/scripts/interview-generator.sh \
  --persona "Product manager, IC5, preparing for IC6" \
  --problem "promotion frameworks too vague"
```

**Output:** Structured interview script with:
- 5 sections (Current State, Problem Discovery, Solutions, Validation, Closing)
- 14 questions with probing prompts
- Interview tips (what to do/avoid)

---

## File Locations

**Scripts:** `skills/customer-research/scripts/`
**Examples:** `skills/customer-research/examples/`
**Research output:** `data/research/`
**Documentation:** `skills/customer-research/SKILL.md`

---

## Integration with Marketing Pipeline

```
Reddit Mining → Persona Validation → Customer Interviews → Content Strategy
     ↓                  ↓                    ↓                    ↓
data/research/   Validation Report    Interview Notes    Ogilvy Content
```

**Where to feed insights:**
1. **Content pillars** — Use validated pain points
2. **Landing pages** — Use customer language verbatim
3. **Product roadmap** — Prioritize validated needs
4. **Social proof** — Extract sample quotes

---

## Quality Checks

✅ **Good research:**
- 50+ Reddit threads per product
- Mix of sources (Reddit + reviews)
- Some assumptions invalidated (you're learning!)
- Verbatim customer quotes captured

❌ **Bad research:**
- All assumptions validated (confirmation bias)
- Single source only
- No surprising findings
- Marketing-speak quotes (you led the witness)

---

## Troubleshooting

**"No research data found"**
→ Run reddit-miner.sh first

**"Reddit API rate limiting"**
→ Add `sleep 2` between requests (line 85 in reddit-miner.sh)

**"All assumptions show NO EVIDENCE"**
→ Either wrong persona or need broader keywords

**"Validation shows false positives"**
→ Keyword matching is basic. For production, use semantic similarity.

---

## Next Steps

1. **Read full docs:** `skills/customer-research/SKILL.md`
2. **See example run:** `skills/customer-research/examples/README.md`
3. **Integration guide:** `skills/customer-research/INTEGRATION.md`
4. **Run first validation** using examples above

---

**Pro tip:** Run research BEFORE building product. Measure twice, cut once.

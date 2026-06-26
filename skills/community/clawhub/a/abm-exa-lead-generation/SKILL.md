---
name: exa-lead-generation
description: "When the user wants to build targeted prospect lists using web search. Also use when the user mentions 'find leads,' 'lead gen,' 'prospect list,' 'build a list,' 'find companies like,' 'ICP search,' or 'prospecting.' Builds LISTS of companies or people matching ideal customer criteria -- not for researching a single company or finding one specific person. For finding specific people at a company, see exa-people-search. For researching a single company in depth, see exa-company-research."
metadata:
  version: 1.0.0
---

# Exa Lead Generation

You help users build targeted prospect lists using Exa web search. Your goal is to find companies and contacts that match the user's ideal customer profile (ICP) and organize them into actionable prospect lists.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Ideal customer profile** -- industry, company size, tech stack, funding stage, geography
2. **List size** -- how many prospects they want
3. **Qualifying signals** -- what makes a company a good fit (recent funding, hiring, product launch, etc.)
4. **Output use** -- cold outreach, ABM campaign, partnership prospecting, etc.

## Workflow

### Step 1: Define Search Queries

Break the ICP into 2-4 search queries that target different angles:

- **Industry + signal:** `"[industry] startup [signal]"` (e.g., "fintech startup series A 2024")
- **Tech stack:** `"[technology] company [qualifier]"` (e.g., "companies using Kubernetes enterprise")
- **Problem-based:** `"[problem the ICP faces]"` (e.g., "scaling customer support team fast-growing")

### Step 2: Run Prospect Searches

Execute each query:

```bash
node tools/clis/exa.js search --query "[ICP-targeted query]" --num-results 20 --text
```

For domain-specific searches, filter to relevant sites:

```bash
node tools/clis/exa.js search --query "[query]" --num-results 20 --include-domains "crunchbase.com,linkedin.com" --text
```

To find companies similar to existing customers:

```bash
node tools/clis/exa.js search --query "[existing customer name] competitors alternatives" --num-results 15 --text
```

To preview without making API calls:

```bash
node tools/clis/exa.js search --query "[query]" --num-results 20 --dry-run
```

### Step 3: Enrich Top Prospects

For the most promising results, fetch detailed content:

```bash
node tools/clis/exa.js contents --ids "[id1],[id2],[id3]" --text --highlights
```

Look for qualifying signals: recent funding, hiring posts, product launches, tech stack mentions.

### Step 4: Build the Prospect List

Organize findings into the output format below. Deduplicate across queries. Rank by fit strength.

## Output Format

### Prospect List: [ICP Description]

**Search criteria:** [Summary of what was searched]
**Results:** [X] companies found, [Y] qualified

| Company | Website | Why They Fit | Key Signal | Fit Score |
|---------|---------|-------------|------------|-----------|
| [Name] | [URL] | [ICP match reason] | [Funding/hiring/tech signal] | High/Med |

### Prospect Details

For each high-fit prospect, include:

- **Company:** [Name]
- **Website:** [URL]
- **What they do:** [One-liner]
- **Why they fit:** [Specific ICP match]
- **Key signal:** [What triggered inclusion]
- **Suggested next step:** [Research deeper / find contacts / reach out]

### Search Queries Used

List the queries that produced the best results for reproducibility.

---

## Tips

- **Cast a wide net, then filter.** Run broad queries with high result counts, then qualify manually.
- **Combine angles.** A company that shows up in multiple queries is a stronger fit.
- **Look for recency.** Recent funding, hiring, or product launches indicate active companies.
- **Save your queries.** Good ICP queries can be rerun periodically to find new prospects.

---

## Related Skills

- **exa-people-search**: Find specific individuals at companies on your list
- **exa-company-research**: Research a single company in depth before outreach
- **cold-email**: Write outreach emails to prospects you've found

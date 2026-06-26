---
name: exa-company-research
description: "When the user wants to research a company using web search -- company overview, products, funding, team, and recent news. Also use when the user mentions 'company research,' 'company info,' 'what does [company] do,' 'tell me about [company],' or 'company overview.' Searches the web via Exa for comprehensive company intelligence. For finding individual people at companies, see exa-people-search. For building prospect lists, see exa-lead-generation."
metadata:
  version: 1.0.0
---

# Exa Company Research

You help users research companies by searching the web via Exa. Your goal is to gather comprehensive company intelligence -- what the company does, who leads it, how it's funded, and what's happening recently.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Company name or domain** -- the target company
2. **Research focus** -- overview, funding, team, product, news, or all
3. **Purpose** -- competitive research, partnership evaluation, prospect qualification, etc.

## Workflow

### Step 1: Search for Company Information

Run a broad search for the company:

```bash
node tools/clis/exa.js search --query "[company name] company overview" --num-results 10 --text
```

Review the results. If the company has a common name, add the domain or industry to narrow results:

```bash
node tools/clis/exa.js search --query "[company name] [domain.com] overview" --num-results 10 --text
```

To preview the request without making an API call:

```bash
node tools/clis/exa.js search --query "[company name] company overview" --num-results 10 --dry-run
```

### Step 2: Narrow by Focus Area

Based on the user's research focus, run targeted searches:

- **Funding:** `node tools/clis/exa.js search --query "[company] funding round investment" --num-results 5 --text`
- **Team:** `node tools/clis/exa.js search --query "[company] leadership team executives" --num-results 5 --text`
- **Product:** `node tools/clis/exa.js search --query "[company] product features pricing" --num-results 5 --text`
- **News:** `node tools/clis/exa.js search --query "[company] news announcement" --num-results 5 --start-date "[30 days ago YYYY-MM-DD]" --text`

Skip this step if the user wants a general overview -- the initial search usually covers enough.

### Step 3: Fetch Detailed Content

For the most relevant results from Steps 1-2, fetch full content using the result IDs:

```bash
node tools/clis/exa.js contents --ids "[id1],[id2],[id3]" --text --highlights
```

Focus on 3-5 of the most relevant sources. Quality over quantity.

### Step 4: Synthesize Findings

Organize everything into the output format below. Cross-reference multiple sources for accuracy. Flag anything that appears outdated or unverified.

## Output Format

Structure your findings as:

### Company Overview

- **Name:** [Full legal/brand name]
- **Website:** [Primary domain]
- **One-liner:** [What they do in one sentence]
- **Founded:** [Year]
- **Headquarters:** [City, Country]
- **Company size:** [Employee count or range, if available]

### Products & Services

- [Product/service 1]: [Brief description]
- [Product/service 2]: [Brief description]

### Team & Leadership

| Name | Title | Background |
|------|-------|------------|
| [Name] | [Title] | [Notable background] |

### Funding & Financials

- **Total raised:** [Amount, if available]
- **Latest round:** [Type, amount, date]
- **Key investors:** [Notable investors]
- **Revenue signals:** [Any public revenue data or signals]

### Recent News

- [Date]: [Headline / summary]
- [Date]: [Headline / summary]

### Competitive Position

- **Market:** [Industry/category]
- **Key competitors:** [Top 2-3 competitors]
- **Differentiation:** [What sets them apart]

---

## Related Skills

- **exa-people-search**: Find specific individuals at companies
- **exa-lead-generation**: Build prospect lists matching criteria
- **competitor-alternatives**: Create competitor comparison and alternative pages

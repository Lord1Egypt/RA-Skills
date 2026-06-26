---
name: exa-personal-site-search
description: "Find personal websites, blogs, and portfolios for specific people using Exa's personal site category search. Use when the user mentions 'find someone's site,' 'personal website,' 'portfolio search,' 'find [person]'s blog,' 'personal blog,' 'developer portfolio,' or 'find their website.' Searches for personal sites by name and affiliations. NOT for finding people at companies (see exa-people-search). For company research, see exa-company-research."
metadata:
  version: 1.0.0
---

# Exa Personal Site Search

You help users find personal websites, blogs, and portfolios for specific people using Exa's personal site category search.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Person's name** -- who are you looking for?
2. **Known affiliations** -- company, university, community, or role
3. **What they're looking for** -- blog, portfolio, personal site, speaking page, or any

## Workflow

### Step 1: Search by Person Name

Run via exec:
```bash
exa.js search --query "[person name] personal site" --category "personal site" --num-results 10
```

### Step 2: Narrow with Affiliations

If the initial results are too broad or return the wrong person, add context to the query:

```bash
exa.js search --query "[person name] [company/university/role]" --category "personal site" --num-results 10
```

### Step 3: Fetch Content from Best Matches

For the most relevant results, fetch full content to verify the site belongs to the right person:

```bash
exa.js contents --ids "[id1],[id2]" --text
```

Use the IDs returned from the search results.

### Step 4: Present Findings

Summarize what you found with context about the person and their site content.

---

## Dry Run

To preview the request without making an API call:
```bash
exa.js search --query "[person name]" --category "personal site" --dry-run
```

---

## Output Format

For each result, present:

- **Person's Name:** [name]
- **Site URL:** [url]
- **Site Type:** Blog / Portfolio / Personal site / Speaking page
- **Key Content Found:** [brief summary of what the site contains]
- **Last Updated:** [if visible from the content]

If multiple sites are found for the same person, list all with a note about which appears to be their primary site.

---

## Tips

- **Common names:** Add role, company, or location to disambiguate ("Jane Smith Stripe engineer" vs just "Jane Smith")
- **Academics:** Try including university name or research area
- **Developers:** Try including GitHub handle or programming language specialty
- **Multiple results:** Cross-reference with LinkedIn or company pages to confirm identity

---

## Related Skills

- **exa-people-search**: Find specific people at companies (who works at X, find the CTO of Y)
- **exa-company-research**: Research a company's overview, products, funding, and news

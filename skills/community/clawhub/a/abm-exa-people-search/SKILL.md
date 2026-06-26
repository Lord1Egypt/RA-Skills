---
name: exa-people-search
description: "When the user wants to find specific people at companies or discover who holds certain roles. Also use when the user mentions 'find people,' 'who works at,' 'people search,' 'find [role] at [company],' 'look up person,' or 'find the CEO of.' Finds SPECIFIC individuals using Exa similarity search -- not for building prospect lists of many companies. For building prospect lists, see exa-lead-generation. For researching the company itself, see exa-company-research."
metadata:
  version: 1.0.0
---

# Exa People Search

You help users find specific people at companies using Exa's similarity search. Your goal is to locate individuals by role, company, or profile -- finding the right person, not building a list of companies.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Target company or person** -- company name, domain, or a known person's profile URL
2. **Role or title** -- the type of person they're looking for (e.g., "VP of Engineering," "Head of Marketing")
3. **Purpose** -- outreach, research, hiring, partnership contact

## Workflow

### Step 1: Find a Starting URL

People search works best with a starting URL -- a LinkedIn profile, company page, or personal site. If the user provides one, skip to Step 2.

If the user only has a company name + role, search for a starting point:

```bash
node tools/clis/exa.js search --query "[company name] [role] LinkedIn" --num-results 5 --include-domains "linkedin.com" --text
```

### Step 2: Find Similar People

Use the `find-similar` subcommand with the starting URL to find people in similar roles or at similar companies:

```bash
node tools/clis/exa.js find-similar --url "[linkedin-or-company-url]" --num-results 10
```

To narrow results to specific domains:

```bash
node tools/clis/exa.js find-similar --url "[url]" --num-results 10 --include-domains "linkedin.com"
```

To preview without making API calls:

```bash
node tools/clis/exa.js find-similar --url "[url]" --num-results 10 --dry-run
```

**Important:** This skill uses `find-similar` (not `search`). The `find-similar` subcommand finds pages similar to a given URL, which is ideal for finding people with similar profiles or roles.

### Step 3: Fetch Profile Details

For the most relevant results, fetch full content:

```bash
node tools/clis/exa.js contents --ids "[id1],[id2],[id3]" --text --highlights
```

Extract name, title, company, and any other relevant details from the content.

### Step 4: Organize Results

Structure findings into the output format below. Verify names and titles from the fetched content -- don't rely solely on URL patterns.

## Output Format

### People Found: [Search Context]

**Target:** [What was searched for]
**Results:** [X] people found

| Name | Title | Company | Profile URL | Key Info |
|------|-------|---------|-------------|----------|
| [Name] | [Title] | [Company] | [URL] | [Notable detail] |

### Person Details

For each person found, include what's available:

- **Name:** [Full name]
- **Title:** [Current title]
- **Company:** [Current company]
- **Profile:** [URL]
- **Background:** [Brief professional background if available]
- **Relevance:** [Why this person matches the search]

---

## Tips

- **Start with a strong URL.** The better the starting URL, the better the similarity results. A specific LinkedIn profile works better than a generic company page.
- **LinkedIn is your friend.** Filter with `--include-domains "linkedin.com"` when searching for professional profiles.
- **Iterate.** If the first results aren't quite right, use the best result as a new starting URL for another `find-similar` search.
- **Combine with search.** If `find-similar` doesn't find enough results, supplement with a targeted search query.

---

## Related Skills

- **exa-lead-generation**: Build prospect lists of companies matching ICP criteria
- **exa-company-research**: Research a company in depth before reaching out to people there
- **exa-personal-site-search**: Find personal websites and portfolios

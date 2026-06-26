---
name: exa-research-papers
description: "Find academic papers, studies, and research on any topic using Exa's research paper category search. Use when the user mentions 'find papers,' 'research papers,' 'academic search,' 'studies about,' 'scientific papers,' 'find research on,' or 'literature search.' Covers finding and synthesizing academic research. NOT for general web search or company research. For company research, see exa-company-research. For market/industry research, see market-research."
metadata:
  version: 1.0.0
---

# Exa Research Papers

You help users find academic papers and research studies using Exa's research paper category search. Your goal is to find relevant papers and synthesize key findings for the user's research question.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Research topic** -- what subject or question are they researching?
2. **Specific questions** -- what do they want to learn or prove?
3. **Field/discipline** -- if known (e.g., computer science, psychology, economics)
4. **Recency preference** -- recent papers only, foundational/seminal works, or both?

## Workflow

### Step 1: Search for Papers

Run via exec:
```bash
exa.js search --query "[research topic]" --category "research paper" --num-results 10
```

For recent papers only, add a date filter:
```bash
exa.js search --query "[topic]" --category "research paper" --num-results 10 --start-date [current-year]-01-01  # Use current year
```

### Step 2: Refine the Search

If results are too broad, narrow with specific terms:
```bash
exa.js search --query "[topic] [specific method or finding]" --category "research paper" --num-results 10
```

### Step 3: Fetch Paper Content

For the most relevant results, fetch content to read abstracts and key sections:
```bash
exa.js contents --ids "[id1],[id2]" --text --highlights
```

Use the IDs returned from the search results.

### Step 4: Synthesize Key Findings

Summarize the papers in the context of the user's research question. Highlight agreements and disagreements across papers.

---

## Dry Run

To preview the request without making an API call:
```bash
exa.js search --query "[topic]" --category "research paper" --dry-run
```

---

## Output Format

For each paper found:

- **Title:** [paper title]
- **Authors:** [author names]
- **Year:** [publication year]
- **Key Findings:** [2-3 sentence summary of main findings]
- **Relevance:** [how this paper relates to the user's question]
- **URL:** [link to paper]

After listing papers, provide a **Synthesis** section:
- Common themes across papers
- Areas of agreement and disagreement
- Gaps in the research
- Suggested next steps or follow-up searches

---

## Tips

- **Broad topics:** Start with a focused subtopic, then expand if needed
- **Technical terms:** Use field-specific terminology for better results
- **Foundational works:** Omit the date filter to find seminal papers
- **Cross-disciplinary:** Run separate searches for each discipline and compare

---

## Related Skills

- **exa-company-research**: Research companies, not academic topics
- **content-strategy**: Turn research findings into content plans

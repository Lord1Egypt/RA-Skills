---
name: citation-verifier
description: Verify, normalize, and enrich a single citation or paper identifier. Use when the user pastes a DOI, URL, arXiv ID, PubMed ID, citation string, or paper title and wants it checked.
---

# Citation Verifier

Use this skill when the user wants to quickly verify or normalize a single paper reference rather than run a full literature search.

## Workflow

1. Accept whatever the user provides: DOI, URL, arXiv ID, PubMed ID, citation string, or a partial title.
2. Call `verify_citation` with the raw input.
3. If verification succeeds, call `fetch` with the resolved identifier to get the full paper record.
4. Present the normalized result.

## Output Style

Return a clean, structured card with:

- **Title** — full paper title
- **Authors** — first three authors, et al. if more
- **Year** — publication year
- **Venue** — journal or conference
- **DOI** — canonical DOI if available
- **Identifiers** — any additional IDs (arXiv, PubMed, Semantic Scholar)
- **Status** — whether the citation was verified successfully or had issues

If verification fails or is ambiguous, say so clearly and suggest what the user can try (e.g., a more complete title, a different identifier).

## Tool Guidance

### Use `verify_citation`

Always call this first. It handles:

- DOI strings (with or without resolver prefix)
- arXiv IDs (e.g., `2301.12345`, `arXiv:2301.12345`)
- PubMed IDs
- full or partial URLs from publisher sites, Semantic Scholar, Google Scholar
- free-text citation strings (e.g., "Smith et al. 2020, Neural networks for...")

### Use `fetch`

Call after successful verification to hydrate the full paper record with abstract, citation count, and venue details.

### Do NOT use

- `search_literature` — this skill is for a known reference, not topic discovery
- `get_citation_graph` — the user wants verification, not graph exploration

## Examples

- User pastes: `10.1038/s41586-021-03819-2`
- User pastes: `https://arxiv.org/abs/2301.12345`
- User says: "Check this cite: Vaswani et al., Attention Is All You Need, NeurIPS 2017"
- User says: "Is this DOI valid? 10.1234/fake.doi.000"
- User pastes a Semantic Scholar or Google Scholar URL

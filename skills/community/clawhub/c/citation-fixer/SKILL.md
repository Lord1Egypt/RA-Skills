---
name: citation-fixer
description: "Audit and fix provenance in knowledge base notes. Ensure every factual claim has an inline citation with date and source."
tags: [provenance, citation, audit, knowledge-management, quality]
---

# Citation Fixer

Provenance audit for knowledge base notes. Scans notes for citation compliance and fixes formatting, missing dates, missing sources, and broken reference links.

## Contract

- Every note is scanned for citation compliance
- Missing citations flagged with specific location and suggested fix
- Malformed citations fixed to the standard format
- Results reported with counts (scanned, fixed, remaining gaps)
- Read-only by default: draft fix suggestions unless the user approves batch apply
- Never fabricate a citation for an uncited claim — flag it

## Citation Standard

Every fact in the knowledge base should carry an inline `[Source: ...]` citation:

- **User's own statements:** `[Source: user, {context}, YYYY-MM-DD]`
- **Web content:** `[Source: {publication}, {URL}, YYYY-MM-DD]`
- **Papers/articles:** `[Source: {authors}, "{title}", {year}]`
- **Conversations:** `[Source: chat with {name} re: {topic}, YYYY-MM-DD]`
- **Synthesis:** `[Source: compiled from {list of source slugs}]`
- **AI model output:** `[Source: {model name}, YYYY-MM-DD]`

## Phases

1. **Scan.** Walk through source notes, concept notes, and wiki pages. Check for inline `[Source: ...]` citations on factual claims.
2. **Identify issues:**
   - Facts without any citation
   - Citations missing date
   - Citations missing source type
   - Citations with wrong format
   - Reference links that 404 or point to wrong slugs
3. **Draft fixes.** For each issue, show the current text and the proposed fix. Group by note.
4. **Report.** Count: notes scanned, citations found, issues fixed, remaining gaps. Surface as a queue item for user review.

## Output Format

```
Citation Audit — YYYY-MM-DD
────────────────────────────
Notes scanned:       X
Citations found:     X total (X valid, X issues)
Issues by type:
  Missing citation:     X
  Missing date:         X
  Missing source type:  X
  Malformed format:     X
  Broken reference:     X
────────────────────────────
Top notes to fix: [paths]
```

## Anti-Patterns

- Fabricating a citation for an uncited claim — flag it as missing, don't invent
- Overwriting a claim citation without checking the source still exists
- Being too aggressive with ad-hoc conversational facts that don't need formal provenance (preference, opinion, speculation clearly marked as such)
- Running the full audit on the entire knowledge base without prioritizing — start with high-traffic pages
- Editing notes directly without the user's approval on the proposed changes

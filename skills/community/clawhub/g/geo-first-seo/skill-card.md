## Description:

Helps users create, audit, rewrite, and mark up content so it is more likely to be cited by AI answer engines such as ChatGPT, Perplexity, Google AI Overviews, Gemini, and Copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and developers use this skill to plan GEO strategy, draft or audit AI-search-ready content, generate technical markup, and score the result against citation-oriented criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SEO or GEO content may contain unverified claims, sources, dates, quotes, or author details.

Mitigation: Review all generated claims before publishing and resolve any [verify] placeholders with real, attributed sources.

Risk: Structured data may be misleading if JSON-LD, FAQ markup, or metadata describes content that is not visible on the page.

Mitigation: Only publish markup that matches the page content and validate structured data before release.

Risk: Citation-gap research can become stale or be unavailable when web access is limited.

Mitigation: Use live read-only research when available, note when it is unavailable, and avoid presenting unverified search-citation findings as fact.

## Reference(s):

- [GEO Content Tactics](artifact/references/geo-content-tactics.md)
- [Technical GEO](artifact/references/technical-geo.md)
- [schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON-LD, llms.txt, FAQ, heading, and metadata snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include [verify] placeholders for claims, sources, authors, URLs, or dates the agent cannot verify.]

## Skill Version(s):

0.1.0 (source: evidence.release.version and changelog, released 2026-06-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Academic Search.Bak helps an agent search arXiv, Google Scholar, and Semantic Scholar, screen scholarly papers, analyze citation context, and synthesize the most relevant results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunhe730](https://clawhub.ai/user/xunhe730)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to perform scholarly literature discovery, compare academic papers, and produce concise literature summaries with bibliographic metadata, publication status, citation signals, and research synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers such as research, cite, and scholar may activate the skill for prompts that are not intentional scholarly literature searches.

Mitigation: Review and narrow the trigger list before installation, especially for agents that auto-activate skills from fuzzy matches.

Risk: The artifact documents a plaintext arXiv API endpoint.

Mitigation: Prefer an updated release or local patch that uses HTTPS-only arXiv endpoints before production use.

Risk: Broad research prompts may expose confidential topics to external academic search services.

Mitigation: Use the skill only for intended literature searches and avoid submitting confidential research topics or sensitive project details in prompts.

## Reference(s):

- [Academic Search Strategy](strategies/main.md)
- [Academic Database APIs and Paper Structure](knowledge/domain.md)
- [Academic Search Best Practices](knowledge/best-practices.md)
- [Academic Search Anti-Patterns](knowledge/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research summaries with ranked paper entries, bibliographic metadata, citation analysis, and synthesis sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns the top relevant scholarly papers for a query and distinguishes publication status, venue, identifiers, open-access availability, and relevance.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json; package metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

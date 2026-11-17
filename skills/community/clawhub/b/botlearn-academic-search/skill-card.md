## Description:

Academic paper discovery across arXiv, Google Scholar, and Semantic Scholar with abstract screening, citation analysis, and research synthesis for OpenClaw Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developers use this skill to find and evaluate academic papers across arXiv, Google Scholar, and Semantic Scholar, then receive a ranked top-five bibliography with publication status, citation context, key findings, and synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search queries may be sent to arXiv, Semantic Scholar, and Google Scholar-related services.

Mitigation: Avoid sending confidential research questions or unpublished sensitive project details through the skill unless the deployment's data-sharing policy permits those external searches.

Risk: Broad triggers such as research or cite may activate the skill for general research requests.

Mitigation: Review activation behavior during installation and narrow trigger routing if the agent should only use the skill for explicit academic literature requests.

Risk: The artifact references an insecure arXiv HTTP endpoint.

Mitigation: Prefer an HTTPS arXiv endpoint where supported before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-academic-search)
- [README](artifact/README.md)
- [Academic Search Strategy](artifact/strategies/main.md)
- [Academic Search Best Practices](artifact/knowledge/best-practices.md)
- [Academic Search Domain Knowledge](artifact/knowledge/domain.md)
- [Academic Search Anti-Patterns](artifact/knowledge/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research summaries with ranked paper entries, bibliographic metadata, citation context, and synthesis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected output is a top-five paper set with publication status, open-access notes, identifiers, relevance rationale, and thematic synthesis.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.md frontmatter; package metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

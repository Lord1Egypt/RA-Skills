## Description:

Academic Search helps an agent find, screen, rank, and synthesize scholarly papers across arXiv, Google Scholar, and Semantic Scholar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurnie](https://clawhub.ai/user/arthurnie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research assistants use this skill to run structured literature searches, compare scholarly sources, and produce concise paper summaries with bibliographic metadata, publication status, citation signals, and synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search queries may be sent to external scholarly services.

Mitigation: Avoid submitting confidential or sensitive research details unless those services are approved for the use case.

Risk: Broad activation triggers may route generic research requests into this skill.

Mitigation: Confirm the user wants scholarly literature search before running database-specific searches.

Risk: Transport-quality issues are present in the artifact's arXiv endpoint examples.

Mitigation: Prefer HTTPS scholarly endpoints and approved client libraries where available.

Risk: Literature-search outputs can mislead if paper details are incomplete or fabricated.

Mitigation: Return only retrieved papers and include persistent identifiers, publication status, venue, and source database metadata for verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthurnie/skills/academic-search)
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/api-docs/graph)
- [Google Scholar](https://scholar.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown literature summaries with ranked paper entries and synthesis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bibliographic metadata, publication status, citation signals, open-access status, and database-query details when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

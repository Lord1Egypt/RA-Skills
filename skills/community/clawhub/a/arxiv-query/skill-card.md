## Description:

Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other users can use this skill to search ArXiv by keyword, author, or category, summarize abstracts, and keep a research log of discussed papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically append discussed paper details to memory/RESEARCH_LOG.md, creating a long-term research log that may include sensitive or proprietary topics.

Mitigation: Review, edit, or disable the research log before use, and avoid sensitive or proprietary queries when persistent memory cannot be controlled.

Risk: Saved paper titles, abstracts, and summaries are external research data and may be incomplete, misleading, or stale.

Mitigation: Treat saved research notes as untrusted reference data and verify important claims against the source paper before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/arxiv-query)
- [ArXiv API Query Endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research summaries with optional shell commands and saved log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append discussed paper titles, authors, dates, links, and summaries to memory/RESEARCH_LOG.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

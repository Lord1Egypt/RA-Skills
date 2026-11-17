## Description:

Search, download, and summarize academic papers from arXiv. Built for AI/ML researchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carloscbrls](https://clawhub.ai/user/carloscbrls)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, technical content creators, job seekers, and security practitioners use this skill to find arXiv papers, inspect metadata and abstracts, download PDFs, and maintain an optional reading list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs arXiv network lookups and downloads PDFs to local storage.

Mitigation: Use it in an environment where arXiv access is expected, and configure ARXIV_PAPERS_DIR to a dedicated download directory.

Risk: Optional MongoDB tracking stores saved paper metadata when MONGODB_URI is configured.

Mitigation: Use a dedicated database and connection string with least-privilege access for reading-list storage.

Risk: Dependency hygiene depends on the installed Python packages.

Mitigation: Install from a locked or reviewed dependency environment before using the skill in shared or production workflows.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/carloscbrls/arxiv)
- [ClawHub skill listing](https://clawhub.ai/carloscbrls/skills/cc3po-arxiv)
- [arXiv API documentation](https://arxiv.org/help/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown summaries with optional JSON from command-line operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include arXiv metadata, paper abstracts, PDF download paths, saved-paper status, and optional MongoDB-backed reading-list results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact package metadata contains differing local versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

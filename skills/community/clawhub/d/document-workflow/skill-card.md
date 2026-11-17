## Description:

Academic paper research workflow for searching, downloading, and analyzing arXiv papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjr-123456](https://clawhub.ai/user/yjr-123456)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to find academic papers, download arXiv source or PDFs, and guide an agent through extracting metadata, methods, experiments, metrics, and structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote paper archives and LaTeX include paths may read or write outside intended folders.

Mitigation: Use the skill only in a contained workspace and avoid untrusted or arbitrary paper sources until archive extraction, LaTeX include resolution, and download destination validation are fixed.

Risk: Search terms are sent to external providers and the package includes a bundled Semantic Scholar API key.

Mitigation: Avoid sensitive search queries and configure a user-controlled Semantic Scholar API key before use.

## Reference(s):

- [Output Schema](artifact/references/output_schema.json)
- [ClawHub Skill Page](https://clawhub.ai/yjr-123456/skills/document-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured paper summaries follow artifact/references/output_schema.json.]

## Skill Version(s):

1.3.1 (source: evidence.release.version, artifact/_meta.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

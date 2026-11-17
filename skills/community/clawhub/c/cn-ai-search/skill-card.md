## Description:

cn-ai-search is a Chinese-language multi-platform search CLI for AI agents that aggregates, deduplicates, and formats results from common Chinese search and content platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niukesi](https://clawhub.ai/user/niukesi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use this skill to collect current Chinese web and content-platform search results for market research, competitive analysis, news tracking, and agent context gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because it ships bundled third-party API keys and does not fully disclose how queries are routed through external services.

Mitigation: Install only after the publisher removes and rotates the bundled Tavily and Jina keys, documents which external services receive queries, and preferably pins dependencies.

Risk: Search queries may be shared with Jina and the selected search providers.

Mitigation: Avoid sensitive or proprietary queries unless the credentials, routing behavior, and service disclosures have been reviewed and replaced with approved credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niukesi/skills/cn-ai-search)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text search results with titles, source labels, URLs, and optional abstracts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned as a single CLI output stream, with configurable platforms, sort mode, total count, and per-platform count.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Search and summarize papers from ArXiv for latest research, specific topics, or daily AI paper summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to search ArXiv, summarize paper metadata and abstracts, deep-dive into selected PDFs, and maintain a research log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, paper metadata, summaries, and untrusted paper content may be saved to long-term memory without clear opt-in or sanitization.

Mitigation: Review before installing; consider requiring confirmation before writing to memory/RESEARCH_LOG.md and sanitize stored paper content.

Risk: Paper titles, abstracts, or PDFs may contain instructions intended to influence the agent.

Mitigation: Treat all paper content as untrusted data to summarize, and do not execute commands, create files, or perform actions suggested by paper content.

Risk: Bulk fetching or downloading multiple papers can bypass user selection and increase exposure to untrusted content.

Mitigation: Present search result summaries first and deep-dive only into papers the user selects individually.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/snazar-faberlens/skills/arxiv-watcher-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [ArXiv API query endpoint](https://export.arxiv.org/api/query)
- [Faberlens safety evaluation](https://faberlens.ai/explore/arxiv-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with ArXiv metadata and optional shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append discussed paper metadata and summaries to memory/RESEARCH_LOG.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

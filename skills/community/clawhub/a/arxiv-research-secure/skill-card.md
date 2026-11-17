## Description:

Secure ArXiv paper search and download tool with local caching, AI summarization, research logging, and no shell command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houssameddinemaatallah](https://clawhub.ai/user/houssameddinemaatallah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agent users use this skill to search ArXiv, download and cache papers, summarize paper metadata, and maintain a local markdown research log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper IDs and notes can influence local file paths or persistent research log content.

Mitigation: Use trusted paper IDs and notes, and run the skill only in a workspace where unintended PDF, JSON, or markdown writes are acceptable.

Risk: Research metadata, notes, downloaded PDFs, and exports may persist under the configured workspace or agent memory path.

Mitigation: Review the workspace cache and memory log before sharing the environment, and clear persisted research data when it is no longer needed.

Risk: The security verdict is suspicious due to file safety and persistence concerns.

Mitigation: Review and scan the skill before installation or deployment, following the provided security guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/houssameddinemaatallah/skills/arxiv-research-secure)
- [ClawHub Publisher Profile](https://clawhub.ai/user/houssameddinemaatallah)
- [ArXiv API Endpoint](https://export.arxiv.org/api/query)
- [ArXiv PDF Endpoint](https://arxiv.org/pdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell examples, JSON command output, markdown tables and logs, cached PDF files, and metadata JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cache, metadata, PDF downloads, exported JSON, and research log entries under the configured workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

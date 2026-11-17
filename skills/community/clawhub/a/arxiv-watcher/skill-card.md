## Description:

Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

External users and researchers use this skill to search ArXiv for recent papers, summarize abstracts, and keep a local research log of papers discussed with the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires long-term logging of every discussed paper, which can preserve research interests, paper selections, and summaries without an opt-in step.

Mitigation: Review the logging behavior before installation and use the skill only in workspaces where persistent research logs are acceptable.

Risk: The skill retrieves remote ArXiv content through the ArXiv API and may summarize external paper metadata or abstracts.

Mitigation: Treat summaries as research assistance, verify important claims against the original ArXiv paper, and avoid sharing sensitive research topics in environments where logs are retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rubenfb23/skills/arxiv-watcher)
- [Publisher profile](https://clawhub.ai/user/rubenfb23)
- [ArXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with ArXiv links and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may append discussed paper metadata and summaries to memory/RESEARCH_LOG.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

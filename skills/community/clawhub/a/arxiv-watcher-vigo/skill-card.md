## Description:

Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

External users, developers, and researchers use this skill to find recent ArXiv papers by topic, author, category, or paper ID, summarize abstracts, and maintain a local research log of discussed papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discussed papers and research topics may be saved locally in memory/RESEARCH_LOG.md for long-term tracking.

Mitigation: Install only if local research logging is acceptable; review or delete the log before using the skill for confidential research topics.

## Reference(s):

- [ArXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summaries with ArXiv links and optional local research-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the ArXiv API through a shell script; discussed papers may be appended to memory/RESEARCH_LOG.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

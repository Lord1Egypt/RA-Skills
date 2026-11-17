## Description:

Read newly announced arXiv papers from cs.AI and cs.CL, filter them by user-defined research topics such as diffusion llm, summarize matching papers into reading notes, and optionally publish a Xiaohongshu post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhrli324](https://clawhub.ai/user/zhrli324)

### License/Terms of Use:


## Use Case:

Developers and research operators use this skill to run a configurable daily arXiv discovery workflow, generate reading notes and Xiaohongshu-ready drafts, and optionally publish reviewed posts through a local Xiaohongshu MCP setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish unattended Xiaohongshu posts through a logged-in local MCP setup.

Mitigation: Use dry-run first, inspect generated drafts before publishing, and avoid scheduled --publish runs unless a review gate is added.

Risk: Generated posts are based on untrusted arXiv metadata and fetched external content.

Mitigation: Review notes and post drafts for accuracy and inappropriate content before publishing.

Risk: Publishing uses the local mcporter configuration and could target the wrong account if the config path is mis-set.

Mitigation: Set MCPORTER_CONFIG_PATH explicitly to the intended account configuration before running publish commands.

## Reference(s):

- [arXiv XHS Daily Operations](references/operations.md)
- [ClawHub skill page](https://clawhub.ai/zhrli324/skills/arxiv-xhs-daily)
- [arXiv API endpoint](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON post drafts, PNG cover images, text publish results, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes run artifacts under data/<topic>/<date>/ and can publish only when invoked with --publish.]

## Skill Version(s):

0.1.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

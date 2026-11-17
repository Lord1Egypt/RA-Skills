## Description:

Expert Finder helps users find domain experts, thought leaders, and subject-matter authorities by searching Twitter and Reddit for people who demonstrate deep knowledge and frequent discussion of a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External users, recruiters, researchers, and developers use this skill to identify and rank domain experts, thought leaders, practitioners, educators, and key opinion leaders for a specified topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external npm package and an Xpoz OAuth account for search access.

Mitigation: Review the mcporter package before installation, prefer a pinned version when available, and authorize only the Xpoz access needed for the task.

Risk: Expert rankings based on social media activity can be incomplete, stale, or biased toward visible public discussion.

Mitigation: Treat rankings as leads for review and validate expertise through independent sources before outreach, hiring, or sourcing decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atyachin/skills/expert-finder)
- [Xpoz](https://xpoz.ai)
- [Xpoz MCP Service](https://mcp.xpoz.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks candidate experts with profile context, reasons, activity signals, and representative examples for human review.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

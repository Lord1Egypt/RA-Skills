## Description:

Work the people who engaged with the user's LinkedIn posts through ContentIn (Agent Pro or Pro plan). Use when the user asks who is engaging with them, which engagers fit their ideal customer, who to follow up with, or wants a comment reply or a connection note drafted for a specific person. Reads list_leads and list_my_comments, drafts text the user approves, never sends anything.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kinzi](https://clawhub.ai/user/kinzi)

### License/Terms of Use:

MIT-0

## Use Case:

The user's agent uses ContentIn to identify and summarize people who engaged with the user's LinkedIn posts, review likely fit and conversation history, and draft a reply or connection note. The user chooses whether to send the draft from their own LinkedIn account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan could not resolve one local path-like reference, leaving that item unassessed.

Mitigation: Identify and review the referenced item before installation, and scan it if it is available.

Risk: Lead records include personal profile and engagement details that could be exposed if shared outside the user's tools.

Mitigation: Keep lead data within the conversation and the user's own tools; only share it elsewhere when the user explicitly names the destination.

Risk: ContentIn's ICP fit score is an estimate based on a person's headline, not verified information about that person.

Mitigation: Describe scores as estimates, preserve unscored leads as unscored, and do not treat a score as verified personal information.

Risk: Outreach drafts could be sent without the user's review if an agent automates posting or messaging.

Mitigation: Provide drafts for the user to review and send themselves; do not send, post, or queue outreach on the user's behalf.

## Reference(s):

- [ContentIn LinkedIn for AI Agents](https://contentin.io/linkedin-for-ai-agents/)
- [ContentIn MCP server](https://mcp.contentin.io/mcp-server)
- [ClawHub skill release](https://clawhub.ai/kinzi/skills/contentin-linkedin-leads)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summaries and tables with short outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts only; the user reviews and sends them.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

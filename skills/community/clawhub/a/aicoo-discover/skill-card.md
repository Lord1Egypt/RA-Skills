## Description:

Finds relevant people on Aicoo Square in automatic or manual mode and presents usernames, profile hooks, reachability, and suggested next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover relevant Aicoo Square profiles for collaboration, hiring, events, or project discovery. It can infer search angles from available context or use an explicit user query, then present curated people results and optional follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use memory, conversation, and repository-derived interests to search Aicoo, which can expose private context to an external service.

Mitigation: Use manual searches or generic Square browsing unless the user explicitly approves using private context for discovery.

Risk: The skill includes authenticated connect, batch connect, messaging, and friend-request actions.

Mitigation: Require explicit user review of each target and message or action before using authenticated endpoints.

Risk: API-key-backed connection operations can expose credentials if key values are printed or copied into output.

Mitigation: Keep credentials in environment variables and never print or include API key values in generated output.

## Reference(s):

- [Aicoo Discover ClawHub release](https://clawhub.ai/xisen-w/skills/aicoo-discover)
- [Aicoo Square search API](https://www.aicoo.io/api/square)
- [Aicoo guest chat API](https://www.aicoo.io/api/chat/guest-v04)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown list with usernames, profile summaries, reachability notes, and optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default result count is 10; output may include public profile snippets, engagement signals, and user-relevance notes.]

## Skill Version(s):

2.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

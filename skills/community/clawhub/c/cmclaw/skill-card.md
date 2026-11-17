## Description:

cmclaw connects agents to YouCloud Creative Manager to analyze ad creatives, generate advertising strategy reports, and support iterative creative brainstorming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcloud](https://clawhub.ai/user/youcloud)

### License/Terms of Use:

MIT-0

## Use Case:

External YouCloud customers and advertising teams use this skill to analyze third-party and owned ad creatives, produce placement strategy reports, and continue brainstorming in a saved conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional DAM_API_BASE override can redirect prompts, account context, and the API key to a non-default endpoint.

Mitigation: Use the default YouCloud production endpoint unless a trusted operator has explicitly approved another destination.

Risk: YOUCLOUD_API_KEY grants access to paid YouCloud Creative Manager functionality and may be exposed through environment or process logs.

Mitigation: Store the key only in a secret manager or protected environment variable and rotate it if logs or shell history may have exposed it.

Risk: CLI output may include user, team, and session identifiers.

Mitigation: Avoid sharing raw execution logs externally and redact identifiers before attaching logs to support or review tickets.

## Reference(s):

- [DamClaw Skill API](references/cm-claw-api.md)
- [cmclaw ClawHub Skill Page](https://clawhub.ai/youcloud/skills/cmclaw)
- [YouCloud Publisher Profile](https://clawhub.ai/user/youcloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown strategy analysis or brainstorming response with a conversation detail link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content is assembled from the service stream before being returned to the user.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

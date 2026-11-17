## Description:

In-memory awareness layer for agents to track their own activity within a single process and query what they are doing in other sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palxislabs](https://clawhub.ai/user/palxislabs)

### License/Terms of Use:


## Use Case:

Developers and agent operators use ARTA to let an agent track its active sessions, channel metadata, user identifiers, task descriptions, and status within a single process. It supports queries such as what the agent is doing in other sessions without requiring persistence, credentials, or external network calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose active session metadata such as channel identifiers, sender names, and task summaries to users who query cross-session activity.

Mitigation: Use it only where users are authorized to see that metadata, and add redaction or authorization checks before returning cross-session summaries.

Risk: Awareness is limited to a single agent process and does not provide true cross-instance state sharing.

Mitigation: Do not rely on it for cross-process coordination unless a shared backend is added and reviewed separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/palxislabs/skills/arta)
- [Publisher profile](https://clawhub.ai/user/palxislabs)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local implementation guidance for an in-memory session awareness protocol.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

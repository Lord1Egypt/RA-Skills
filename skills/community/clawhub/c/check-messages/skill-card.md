## Description:

Check Messages helps an agent retrieve and summarize Aicoo inbox, conversation, and pending request activity for a user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to review messages received by their Aicoo agent, inspect direct and shared-agent conversation history, identify unread activity, and see pending network requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's Aicoo API key to fetch private inbox data, conversation contents, contact identities, timestamps, and pending request details.

Mitigation: Install only when the agent session is allowed to handle private inbox data, and avoid sharing generated summaries outside the intended audience.

Risk: Broad message queries may expose more direct and shared-agent conversation history than the user intended to review.

Mitigation: Use explicit channel, time, contact, or unread filters when possible before displaying or acting on message results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xisen-w/skills/check-messages)
- [Aicoo API base URL](https://www.aicoo.io/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and suggested follow-up actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include message excerpts, contact identifiers, timestamps, channels, unread status, and pending request details.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Searches Douyin for popular videos matching a keyword and helps an agent post a comment from a logged-in Douyin account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users or operators use this skill to automate keyword-based Douyin discovery and submit context-relevant comments through an already authenticated browser profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post public Douyin comments from a logged-in account.

Mitigation: Confirm the target video and exact comment text before allowing the agent to submit the comment.

Risk: The skill includes automatic local gateway recovery that can terminate matching gateway processes.

Mitigation: Review and approve any local process restart or termination behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/douyin-comment)
- [Publisher profile](https://clawhub.ai/user/mars82311111)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with browser action instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in openclaw browser profile for Douyin actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

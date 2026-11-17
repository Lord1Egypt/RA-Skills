## Description:

Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant learning resources from HackerNews, and automatically sends a personalized growth report to your Slack DMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javotillo](https://clawhub.ai/user/javotillo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review recent Claude Code work patterns, identify targeted improvement areas, and receive a personalized growth report with learning resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent Claude Code chat history, which may include pasted code, secrets, proprietary text, or sensitive project details.

Mitigation: Review the generated report locally first and redact sensitive details before allowing any external delivery.

Risk: The skill instructs the agent to send the report to Slack DMs, creating a privacy risk if the content is delivered without explicit approval.

Mitigation: Require explicit user approval before sending Slack messages and confirm the intended recipient and content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javotillo/skills/developer-growth-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report and Slack-formatted messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prioritized improvement areas, action items, and links to relevant learning resources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

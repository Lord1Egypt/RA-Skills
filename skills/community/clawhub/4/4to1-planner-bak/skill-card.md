## Description:

AI planning coach using the 4To1 Method(tm) to turn a 4-year vision into daily action across Notion, Todoist, Google Calendar, or local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to set up and maintain a personal planning system, run weekly and sprint reviews, choose daily priorities, and keep tasks aligned to longer-term goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and status scripts store or load integration credentials in ~/.config/4to1/config, and the status script sources that file.

Mitigation: Prefer the local Markdown backend or tightly scoped integration tokens, restrict permissions on ~/.config/4to1/config, and avoid running status.sh until config loading is changed to parse data without source.

Risk: The skill can connect an agent to third-party planning services such as Notion and Todoist.

Mitigation: Use least-privilege integrations, review requested permissions before connecting services, and rotate any token exposed during setup.

## Reference(s):

- [4To1 Planner website](https://4to1planner.com)
- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/skills/4to1-planner-bak)
- [ClawHub publisher profile](https://clawhub.ai/user/dorjenorbulim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with conversational guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backend-specific setup steps for Notion, Todoist, Google Calendar, or local Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

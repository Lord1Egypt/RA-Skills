## Description:

Interact with Slack workspaces using browser automation to check unread channels, navigate Slack, send messages, extract data, find information, search conversations, and automate Slack tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workplace automation users use this skill to inspect Slack activity, search conversations, capture screenshots, extract structured browser snapshots, and prepare Slack analysis reports from sessions they are authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate a logged-in Slack session and save private workspace content locally.

Mitigation: Use it only for Slack accounts and conversations the operator is authorized to access, prefer summaries over raw screenshots or JSON exports, and delete local captures after use.

Risk: The skill can interact with Slack through browser controls, including actions that may send messages or expose private channel and DM content.

Mitigation: Confirm the active workspace, channel or DM, and message content before taking action, and use fresh snapshots or screenshots to verify state.

Risk: The documented npx path may execute the agent-browser tool from the package ecosystem.

Mitigation: Pin or vet the agent-browser tool before relying on the npx invocation in a real workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/skills/daxiang-slack)
- [Common Slack Tasks & Patterns](artifact/references/slack-tasks.md)
- [Slack Analysis Report Template](artifact/templates/slack-report-template.md)
- [Slack Help Center](https://slack.com/help)
- [Slack Web App](https://app.slack.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional local screenshot, text, JSON, or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local browser snapshots, screenshots, JSON extracts, and Markdown reports from the active Slack session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

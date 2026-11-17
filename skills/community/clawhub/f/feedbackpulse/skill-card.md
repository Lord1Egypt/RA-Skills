## Description:

FeedbackPulse (feedbackpulse.com) for HR teams: design employee surveys with no sign-in, and read engagement survey results, eNPS, review cycles, peer reviews and recognition through the FeedbackPulse MCP server. Use this skill for any FeedbackPulse request or when the user wants to draft an employee survey.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feedbackpulse-bot](https://clawhub.ai/user/feedbackpulse-bot)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams use the skill to draft employee surveys and, after connecting an authorized workspace, review engagement results, eNPS, review cycles, peer feedback, recognition, and employee data. Survey templates and drafts are saved only after the user approves the preview and save choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Employee information and survey responses may be sensitive.

Mitigation: Connect only an authorized HR workspace, consider what employee information may be shared with the AI client, and keep API tokens in client credential settings rather than chat.

Risk: Saving survey templates or drafts changes workspace data.

Mitigation: Show the survey preview and get the user's explicit approval of the preview and save choice before saving.

Risk: The optional stdio bridge requires installing and running third-party software.

Mitigation: Prefer a native remote connection; if using the bridge, pin a reviewed version.

## Reference(s):

- [FeedbackPulse](https://feedbackpulse.com/)
- [ClawHub release page](https://clawhub.ai/feedbackpulse-bot/skills/feedbackpulse)
- [MCP overview](https://feedbackpulse.com/help/integrations/mcp-overview/)
- [MCP tools reference](https://feedbackpulse.com/help/integrations/mcp-tools-reference/)
- [API token management](https://feedbackpulse.com/help/integrations/token-management/)
- [MCP troubleshooting](https://feedbackpulse.com/help/integrations/mcp-troubleshooting/)

## Skill Output:

**Output Type(s):** [Guidance, Survey proposals, Workspace data summaries]

**Output Format:** [Markdown and structured MCP data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Survey writes require explicit user approval; surveys are not launched and notifications are not sent.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

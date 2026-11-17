## Description:

龙虾教研日报助手 helps education and research staff record daily work through conversation, write entries to Tencent Docs, and generate monthly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team members who track education or research work use this skill to configure Tencent Docs access, log daily work, leave, and overtime, and prepare monthly summaries from the shared report sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared Tencent Docs report data may expose team report contents to users who should not see them.

Mitigation: Use the skill only where all users are authorized for the configured shared sheet, and review Tencent Docs collaborator permissions before deployment.

Risk: The runtime invokes mcporter through npx and package metadata lists mcporter as latest, which can execute changing code over time.

Mitigation: Pin and vet the mcporter version before installation or production use.

Risk: Tencent Docs tokens and local memory/configuration can expose account or report access if mishandled.

Mitigation: Avoid entering tokens directly on the command line, revoke leaked authorization in Tencent Docs, and treat workspace memory and mcporter configuration as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmww/skills/daily-report-assistant)
- [Setup guide](references/setup-guide.md)
- [Data schema](references/data-schema.md)
- [Deployment guide](references/deploy-guide.md)
- [Tencent Docs authorization](https://docs.qq.com/scenario/open-claw.html?nlc=1)
- [Tencent Docs MCP endpoint](https://docs.qq.com/openapi/mcp)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown with shell command invocations and Tencent Docs status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, Python 3, mcporter, Tencent Docs authorization, and access to the configured report sheets.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

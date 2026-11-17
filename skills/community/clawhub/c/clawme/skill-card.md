## Description:

Sends browser actions to the user's Chrome extension for review and confirmation before execution in their logged-in session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with the ClawMe Chrome extension can draft posts and emails, fill forms, click pages, and extract text in their own browser, approving actions in the side panel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser actions can post, send email, submit forms, or click in logged-in sessions.

Mitigation: Review each proposed action in the Chrome side panel before approving it.

Risk: Extracting content from logged-in pages may expose private information to the agent.

Mitigation: Approve extraction only for pages and content you intend to share.

## Reference(s):

- [ClawMe on ClawHub](https://clawhub.ai/dongsheng123132/skills/clawme)
- [Project homepage listed in skill metadata](https://github.com/dongsheng123132/clawme)

## Skill Output:

**Output Type(s):** [Text, JSON browser instructions]

**Output Format:** [Text and structured browser-action requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted page text can be returned to the agent; browser actions require user confirmation.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automate content creation, management, and distribution workflows for blogs, social media, newsletters, and publishing calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacealllc](https://clawhub.ai/user/jacealllc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, agencies, and business operators use this skill to plan, generate, schedule, distribute, and review recurring content workflows across publishing and social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command execution and path handling can expose the host environment when scripts are run with untrusted arguments or workflow files.

Mitigation: Review and patch command construction and path validation before use; run only in a constrained workspace until fixed.

Risk: Credential and live-posting workflows can affect real publishing, social, email, analytics, or storage accounts.

Mitigation: Do not connect real credentials until secrets are stored safely, live posting requires explicit confirmation, and credential redaction is in place.

Risk: Generated reports and logs may contain workflow inputs, outputs, or operational details.

Mitigation: Review report locations and add log/report redaction before processing sensitive content or customer data.

## Reference(s):

- [Scheduled Blog Pipeline Guide](references/scheduled_blog.md)
- [Multi-Platform Social Pipeline Guide](references/social_multi.md)
- [ClawHub Skill Page](https://clawhub.ai/jacealllc/skills/content-workflow-engine)
- [Publisher Profile](https://clawhub.ai/user/jacealllc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workflow definitions, local reports, and content drafts when its scripts are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Cotrace lets an agent retrieve a user's recent work-activity context from Pieces OS and Cotrace through the ftc CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyqqj0](https://clawhub.ai/user/tyqqj0)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or authorized agents use Cotrace to answer questions about recent or same-day work activity by querying summaries and details from the user's Pieces/Cotrace workstream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve work-activity records that may contain sensitive personal or business context.

Mitigation: Confirm what Pieces and Cotrace collect, query narrow date ranges, and fetch detailed records only when needed.

Risk: The installation flow uses a global third-party ftc CLI install.

Mitigation: Use a pinned or isolated CLI installation and install it only when the ftc CLI publisher is trusted.

Risk: The skill configures login access and an external bridge endpoint for Cotrace calls.

Mitigation: Trust the configured bridge endpoint before use and keep revocation, resource removal, and alias removal steps available.

## Reference(s):

- [Cotrace installation and configuration](references/install.md)
- [ClawHub Cotrace skill page](https://clawhub.ai/tyqqj0/skills/cotrace)
- [Pieces and Cotrace setup guide](https://nxwu5gzs9f9.feishu.cn/wiki/DsVrwc2QMiVhR4kigdMct8XKntg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text with inline bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local-time presentation of UTC workstream timestamps.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

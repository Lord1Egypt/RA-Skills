## Description:

Helps agents manage ClickFunnels contacts, products, orders, courses, forms, and webhooks through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and developers use this skill to manage ClickFunnels sales data and set up approved automations using their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-account actions can change or delete sensitive ClickFunnels records.

Mitigation: Start with read-only requests and obtain explicit approval for each write or delete after checking the account and resource IDs.

Risk: Webhooks, hosted functions, and scheduled triggers can keep running or forwarding data after setup.

Mitigation: Confirm the destination URL, data flow, and intended duration separately before enabling persistent automation.

## Reference(s):

- [ClickFunnels skill release](https://clawhub.ai/byungkyu/skills/clickfunnels)
- [Maton](https://maton.ai)
- [ClickFunnels API documentation](https://developers.myclickfunnels.com/docs/intro)
- [ClickFunnels API reference](https://developers.myclickfunnels.com/reference)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a user-authorized Maton connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata; skill frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

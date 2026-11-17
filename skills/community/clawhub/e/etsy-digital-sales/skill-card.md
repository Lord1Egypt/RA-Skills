## Description:

Build and manage an automated Etsy digital product store using Python, Etsy API OAuth, and Selenium browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Etsy shop operators can use this skill to generate, list, renew, and monitor digital products such as templates, spreadsheets, checklists, and prompt packs. It should be reviewed before use on a real Etsy shop because it can involve live account automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt agents to use Etsy credentials and OAuth tokens.

Mitigation: Store credentials only in secure secret storage and never commit them to files.

Risk: Listing creation, renewal, messaging, and account or earnings access can affect fees, account standing, and customer communications.

Mitigation: Require dry-run behavior or explicit manual confirmation before live Etsy actions.

Risk: Automated Etsy store workflows may violate platform policy if configured incorrectly.

Mitigation: Confirm the workflow complies with Etsy policies before connecting it to a real shop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/etsy-digital-sales)
- [Etsy Developers](https://developer.etsy.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve live Etsy API and browser automation actions when implemented by an agent.]

## Skill Version(s):

1.0.17 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

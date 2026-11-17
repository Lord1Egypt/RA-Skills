## Description:

Checks whether a website's 301 redirect configuration is correct.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomeng-agi](https://clawhub.ai/user/xiaomeng-agi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and site operators use this skill to request paid remote analysis of 301 redirect behavior and receive findings, recommendations, and an action plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends analysis requests and credentials to an external paid service.

Mitigation: Use only data appropriate for the provider and payment flow; do not submit internal URLs, confidential site data, secrets, or reusable credentials unless trust has been established.

Risk: The skill may be mistaken for a local 301 redirect checker.

Mitigation: Treat it as a paid third-party remote analysis client and review returned recommendations before applying SEO or redirect changes.

Risk: Credentials are passed through the result retrieval command.

Mitigation: Avoid exposing credentials in shell history, logs, or shared terminals, and use short-lived credentials where possible.

## Reference(s):

- [API Reference](references/api-reference.md)
- [XiaoMeng API Homepage](https://xiaomeng-api.qisir.com)
- [ClawHub Skill Page](https://clawhub.ai/xiaomeng-agi/skills/301-redirect-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured analysis text or Markdown returned through a remote JSON API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid remote service; results are retrieved after order creation and payment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

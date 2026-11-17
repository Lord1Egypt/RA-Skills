## Description:

Helps agents manage Chargebee customers, subscriptions, invoices, and billing workflows through an authorized Maton connection, with optional user-approved automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Billing administrators and developers use this skill to inspect and, with explicit approval, update Chargebee billing records or configure related automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized calls can change customers, subscriptions, invoices, and other billing data.

Mitigation: Default to read-only access; confirm the connection ID, exact endpoint, account, resource, and consequence before each write.

Risk: Hosted functions, triggers, and destinations can run actions or forward event data persistently.

Mitigation: Require separate explicit approval for each automation or destination, including its target and data flow; use narrow scopes and least-privilege access.

Risk: Billing connections and authentication material may expose sensitive customer information or credentials.

Mitigation: Keep credentials in the approved credential store, avoid logging sensitive responses, and revoke unused connections promptly.

## Reference(s):

- [Chargebee skill release](https://clawhub.ai/byungkyu/skills/chargebee)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Chargebee API documentation](https://apidocs.chargebee.com/docs/api)
- [Calendly trigger event reference](references/calendly/triggers.md)
- [GitHub trigger event reference](references/github/triggers.md)
- [Gmail trigger event reference](references/google-mail/triggers.md)
- [HubSpot trigger event reference](references/hubspot/triggers.md)
- [Linear trigger event reference](references/linear/triggers.md)
- [Notion trigger event reference](references/notion/triggers.md)
- [Slack trigger event reference](references/slack/triggers.md)
- [Stripe trigger event reference](references/stripe/triggers.md)
- [Scheduled trigger event reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account and authorized Chargebee connection; billing writes and automation require explicit user approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

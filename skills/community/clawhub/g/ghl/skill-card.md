## Description:

Provides agent-facing GoHighLevel API v2 CRM automation for reading and updating contacts, conversations, notes, opportunities, calendars, tags, forms, workflows, payments, and invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianxmacdonald](https://clawhub.ai/user/brianxmacdonald)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and CRM automation teams use this skill to let an agent operate a GoHighLevel location for lead response, contact lookup, record updates, pipeline movement, calendar checks, workflow triggering, and activity logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad live CRM authority and can send customer messages or modify CRM records.

Mitigation: Use a least-privilege GoHighLevel token and limit enabled scopes to the operations approved for the deployment.

Risk: Autonomous message sending, workflow triggering, contact updates, opportunity changes, and invoice or payment-related operations can create business or compliance impact.

Mitigation: Require an external approval and compliance layer before allowing those actions to run without human review.

Risk: CRM credentials may be exposed if secrets are placed directly in shell commands or logs.

Mitigation: Load GHL_API_KEY and GHL_LOCATION_ID from protected environment storage and avoid echoing token values in prompts, commands, or logs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/brianxmacdonald/skills/ghl)
- [Publisher profile](https://clawhub.ai/user/brianxmacdonald)
- [SetupClaw homepage](https://setupclaw.tech)
- [GoHighLevel API endpoint](https://services.leadconnectorhq.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus GHL_API_KEY and GHL_LOCATION_ID environment variables.]

## Skill Version(s):

1.3.0 (source: server release metadata, artifact metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manages account switching after bans, including device coordination, contact migration, account status updates, pre-switch contact filtering, and notifications for ban detection, switch requests, or risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage platform account replacement workflows after bans or risk alerts, including account status updates, contact notification planning, device login coordination, and migration summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad authority over accounts, contacts, cookies, device login, notifications, and memory migration.

Mitigation: Install and run it only in environments where the operator is authorized to manage those accounts, contacts, devices, cookies, and memories.

Risk: Account switching, contact export, notifications, configuration changes, cron changes, and memory migration can affect users and platform compliance.

Mitigation: Require manual approval before those actions and confirm the workflow complies with applicable platform rules and privacy obligations.

## Reference(s):

- [Account Manager Skill](https://clawhub.ai/thcjp/skills/account-manager)
- [Business Rules](references/business_rules.md)
- [Error Codes](references/error_codes.md)
- [Examples](references/examples.md)
- [Account Manager Reference](scripts/account_manager_reference.json)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON input and output examples plus executable Python command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured account-switch results, error codes, notification counts, and migration summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps developers integrate with Didit Case Management to manage compliance investigations and prepare FIU regulatory reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build API-key integrations that manage Didit investigation cases, assignments, review workflows, audit records, analytics, and FIU reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API key to make requests to Didit's external service.

Mitigation: Keep DIDIT_API_KEY in a secure secret store and confirm the organization and application IDs before making changes.

Risk: Finalizing an FIU report is irreversible.

Mitigation: Validate the report and have an authorized reviewer confirm its contents before finalizing it.

## Reference(s):

- [Didit Case Management API Reference](https://docs.didit.me/management-api/cases/list)
- [Didit Case Management Guide](https://docs.didit.me/console/case-management/cases)
- [Didit Case Blueprints Guide](https://docs.didit.me/console/case-management/blueprints)
- [Didit Four-Eyes Approval Guide](https://docs.didit.me/console/case-management/four-eyes)
- [Didit FIU Reports Guide](https://docs.didit.me/console/case-management/fiu-reports)

## Skill Output:

**Output Type(s):** [Code, API calls, Shell commands, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples, REST payloads, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key setup and workflows for case management and FIU reporting.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

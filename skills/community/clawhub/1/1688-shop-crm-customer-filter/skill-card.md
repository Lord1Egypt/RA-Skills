## Description:

Filters 1688 shop CRM customers by tags, purchase amounts, activity, purchase intent, and custom attributes, with support for sorting, pagination, summaries, and custom attribute management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and operators with authorized 1688 shop CRM access use this skill to find, sort, and review customer records, inspect available customer attributes, and add custom CRM attributes after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive customer CRM data and may expose more data than intended.

Mitigation: Install it only for authorized 1688 CRM environments and restrict who can invoke customer queries or request raw output.

Risk: Usage reporting runs after recognized CLI commands and is silent on success or failure.

Mitigation: Review the reporting behavior before deployment and disclose, monitor, or disable it according to the deployment policy.

Risk: Custom attribute creation can change CRM metadata.

Mitigation: Require explicit user approval for the key, label, type, and value before running attribute creation, and limit access to trusted operators.

Risk: Markdown escaping and file-path diagnostics may need hardening before broad deployment.

Mitigation: Patch and test Markdown rendering and file-path error handling before enabling wide customer-data access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shop-crm-customer-filter)
- [Customer list capability reference](references/capabilities/customer_list.md)
- [Customer attribute field configuration reference](references/capabilities/customer_attr_field_config.md)
- [Customer attribute creation reference](references/capabilities/customer_attr_add.md)
- [Skill usage reporting reference](references/skill╧â╞Æ├»╧ä├⌐Γòú╬ª┬╗Γöñ┬╡├┐├ä.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries and JSON command output, with shell commands for CLI execution and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default customer-list output is summarized Markdown with pagination metadata; raw JSON is available when explicitly requested.]

## Skill Version(s):

0.47.0 (source: server release metadata; artifact frontmatter version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

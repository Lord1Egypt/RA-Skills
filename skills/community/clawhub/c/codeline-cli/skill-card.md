## Description:

Manage Codeline through a CLI for tools, products, orders, users, and coupons when interacting with the Codeline API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate with Codeline and run CLI commands that inspect tools, products, orders, users, and coupons. It also guides coupon creation and structured JSON output for programmatic workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run mutable external installers and package commands.

Mitigation: Review the install commands first and prefer pinned, verified installs from trusted sources.

Risk: The CLI uses an API token to access e-commerce resources such as users, orders, products, and coupons.

Mitigation: Use a least-privilege, revocable Codeline token and avoid production tokens unless the task requires them.

Risk: Some commands can expose customer or order data or create coupons that affect commerce workflows.

Mitigation: Confirm the exact command and parameters before listing sensitive resources or creating coupons.

## Reference(s):

- [Codeline Cli on ClawHub](https://clawhub.ai/melvynx/skills/codeline-cli)
- [Bun installer](https://bun.sh/install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for programmatic CLI calls.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

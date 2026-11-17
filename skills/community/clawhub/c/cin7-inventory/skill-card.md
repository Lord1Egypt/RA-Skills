## Description:

Cin7 Core inventory management -- products, stock, orders, purchases, customers, and suppliers via bash scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yashthesiya1](https://clawhub.ai/user/yashthesiya1)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to run Cin7 Core inventory, order, purchase, stock, customer, and supplier workflows through bash scripts backed by the Cin7 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update live Cin7 business records, including orders, purchases, stock adjustments, and stock transfers.

Mitigation: Require explicit user approval before running create, update, or stock-changing scripts, and use Cin7 credentials with the minimum permissions needed.

Risk: Credential configuration can be redirected through CIN7_API_URL if that environment value is present.

Mitigation: Keep any .env file private and verify CIN7_API_URL is absent or set to the official Cin7 HTTPS API before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yashthesiya1/skills/cin7-inventory)
- [Cin7 Core API Docs](https://help.core.cin7.com/)
- [Cin7 Core API Base URL](https://inventory.dearsystems.com/ExternalApi/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, CIN7_ACCOUNT_ID, and CIN7_APP_KEY; scripts may return Cin7 API response data.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

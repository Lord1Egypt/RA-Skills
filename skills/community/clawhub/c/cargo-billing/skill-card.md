## Description: <br>
Pull usage metrics, check subscription status, view invoices, and manage credits using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cargo workspace admins and developers use this skill to inspect billing analytics, usage reports, credit consumption, subscription details, invoice history, and billing portal access for a Cargo workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires admin-level billing access and sensitive credentials. <br>
Mitigation: Install only when Cargo billing administration is needed, prefer OAuth or a narrowly managed admin token, verify the workspace with cargo-ai whoami, and rotate or revoke credentials when access is no longer required. <br>
Risk: Invoice, card, portal-session, usage, and workflow-run commands may expose billing information or consume credits. <br>
Mitigation: Review commands before execution, share outputs only with authorized users, check remaining credits before large runs, and estimate batch cost from a small sample before scaling. <br>


## Reference(s): <br>
- [Cargo Billing on ClawHub](https://clawhub.ai/cargo-ai/cargo-billing) <br>
- [Cargo skills repository](https://github.com/getcargohq/cargo-skills) <br>
- [Usage metrics examples](references/examples/usage-metrics.md) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Cargo CLI, a Cargo account, and admin-level OAuth or API-token access.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

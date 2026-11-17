## Description:

Helps agents operate Alibaba Cloud Lingjun compute nodes by locating resources, submitting diagnostics, producing diagnostic reports, proposing repair plans, and tracking fault reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud infrastructure operators and site reliability engineers use this skill to investigate Alibaba Cloud Lingjun GPU node issues, collect diagnostic evidence, prepare repair plans, and manage fault-report workflows. It is intended for users who can grant and supervise Alibaba Cloud eflo-controller permissions.

### Deployment Geography for Use:

Alibaba Cloud Lingjun supported regions, with live region discovery authoritative; the artifact's fallback list includes China East, China North, China South, and Singapore regions.

## Known Risks and Mitigations:

Risk: The skill can guide high-impact cloud operations including reimage, stop, repair approval, and fault-report termination.

Mitigation: Grant only the minimum Alibaba Cloud RAM permissions needed for the intended workflow, and require a fresh human confirmation and an approved change window before mutating actions.

Risk: The installation guidance includes a curl-to-bash CLI installer path.

Mitigation: Use package-manager or independently verified Alibaba Cloud CLI installation methods when possible, and verify the installer source before execution.

Risk: Diagnostic evidence and logs may contain operationally sensitive details.

Mitigation: Review and redact logs, node identifiers, credentials, and other sensitive values before sharing reports or submitting fault information.

Risk: The security evidence notes that referenced safety wrappers were not included for review.

Mitigation: Confirm wrapper availability and behavior in the deployed environment before allowing the agent to issue Alibaba Cloud CLI commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-lingjun-node-diagnose)
- [Alibaba Cloud Eflo-Controller OpenAPI](https://api.aliyun.com/api/eflo-controller/2022-12-15)
- [API Parameters Reference](references/api-parameters.md)
- [Command Quick Reference](references/command-quick-reference.md)
- [Diagnose Operations](references/diagnose-operations.md)
- [Endpoint Routing and Region Rules](references/endpoint-routing.md)
- [Parameter Confirmation Templates](references/parameter-confirmation.md)
- [RAM Policies](references/ram-policies.md)
- [Repair Plan Templates](references/repair-plan-templates.md)
- [Fault Report Tracking](references/fault-report-tracking.md)
- [Verification Method](references/verification-method.md)
- [Supported Regions](references/supported-regions.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands, confirmation tables, diagnostic summaries, and repair-plan guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on real Alibaba Cloud CLI responses for diagnostic reports and repair status, with sensitive values masked.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

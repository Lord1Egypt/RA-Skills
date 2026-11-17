## Description:

Audits Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and OPA/Rego policies to detect overly permissive IAM policies, public resource exposure, missing encryption, and insecure defaults before cloud deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and security teams use this skill to audit Terraform code, plans, and state before cloud deployment. It helps add IaC security checks and policy-as-code gates to CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party scanner packages and CI actions can change behavior across releases.

Mitigation: Pin scanner packages and GitHub Actions to reviewed versions or commit SHAs before using the workflow in CI.

Risk: Terraform plan and state files may contain sensitive infrastructure details or secrets.

Mitigation: Run scans in isolated development or CI environments and handle generated plan, state, SARIF, and JSON outputs as sensitive artifacts.

Risk: Automated IaC findings can include false positives or accepted exceptions.

Mitigation: Review findings before changing infrastructure and document justified suppressions or accepted risks.

## Reference(s):

- [API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/ling-qian/skills/auditing-terraform-security)
- [Checkov Documentation](https://www.checkov.io/)
- [tfsec Documentation](https://aquasecurity.github.io/tfsec/)
- [Terrascan Documentation](https://runterrascan.io/)
- [Conftest Documentation](https://www.conftest.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Rego, YAML, and JSON examples; optional JSON audit reports from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scanner findings grouped by severity and file/resource location]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

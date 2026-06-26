## Description: <br>
Audits Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and OPA/Rego policies before cloud deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and security engineers use this skill to audit Terraform modules, plans, and state for cloud security issues and to add security scanning gates to CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform plans, state files, scan outputs, and SARIF or JSON reports can expose sensitive infrastructure details. <br>
Mitigation: Treat these artifacts as sensitive, limit sharing, and store reports only in approved systems. <br>
Risk: Optional integrations may require API keys or other sensitive credentials. <br>
Mitigation: Use least-privilege credentials, avoid embedding secrets in Terraform or CI configuration, and rotate credentials according to policy. <br>
Risk: Running scans against unauthorized Terraform projects or cloud environments can expose data outside the user's remit. <br>
Mitigation: Install and use the skill only for Terraform projects the user is authorized to review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ling-qian/auditing-terraform-security) <br>
- [API Reference: Auditing Terraform Infrastructure for Security](artifact/references/api-reference.md) <br>
- [Checkov documentation](https://www.checkov.io/) <br>
- [tfsec documentation](https://aquasecurity.github.io/tfsec/) <br>
- [Terrascan documentation](https://runterrascan.io/) <br>
- [Conftest documentation](https://www.conftest.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, YAML, Rego, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Terraform plans, state files, scanner output, and SARIF or JSON reports that should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Cloud infrastructure and IaC security scanner that detects insecure Terraform, open S3 buckets, permissive IAM, missing encryption, exposed ports, and cloud misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and security teams use CloudGuard to scan infrastructure-as-code repositories for cloud security misconfigurations before deployment. It can also generate reports and install git hooks that block commits or pushes with severe findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License keys can be exposed through command-line arguments or insecure local configuration. <br>
Mitigation: Prefer CLOUDGUARD_LICENSE_KEY in a protected environment or a restricted OpenClaw config file; avoid passing license keys with --license-key. <br>
Risk: License token handling and local shell scripts can create local execution risk when tokens or skill files come from untrusted sources. <br>
Mitigation: Review the license-handling scripts before installation and do not use license tokens from untrusted sources. <br>
Risk: Git hook integration can block commits or pushes in repositories where that workflow is not expected. <br>
Mitigation: Enable lefthook integration only in repositories where commit and push blocking is acceptable. <br>


## Reference(s): <br>
- [CloudGuard ClawHub Page](https://clawhub.ai/suhteevah/cloudguard) <br>
- [CloudGuard Website](https://cloudguard.pages.dev) <br>
- [CloudGuard Pricing](https://cloudguard.pages.dev/#pricing) <br>
- [CloudGuard License Terms](https://cloudguard.pages.dev/license) <br>
- [Publisher Profile](https://clawhub.ai/user/suhteevah) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, markdown reports, JSON, HTML reports, and shell command/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scanner output may include severity, category, file, line number, check ID, score, grade, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Scans web endpoints for CORS misconfigurations such as origin reflection, wildcard policies, null-origin acceptance, credential leaks, subdomain trust, HTTP-origin trust on HTTPS, preflight issues, and private network access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to scan one or more web endpoints for unsafe CORS behavior and receive findings, grades, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner disables HTTPS certificate verification by default, which can make results unreliable on intercepted or spoofed connections. <br>
Mitigation: Use the skill only against targets you control and treat results as potentially unreliable unless TLS verification is restored or an explicit insecure-mode workflow is added. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown scan reports with CORS findings, grades, evidence, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can scan single or multiple URLs and can return CI-oriented exit codes with --min-grade.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

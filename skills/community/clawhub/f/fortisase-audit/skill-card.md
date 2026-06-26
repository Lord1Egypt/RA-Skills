## Description: <br>
Fortinet FortiSASE audit for Secure Web Gateway policy review, ZTNA application gateway assessment, thin edge FortiGate integration validation, SD-WAN security overlay analysis, FortiClient endpoint compliance verification, and cloud security posture evaluation across FortiSASE tenants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and network operations teams use this skill to review FortiSASE tenant posture across SWG, ZTNA, thin edge, endpoint compliance, FortiGuard service health, logging, and configuration drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-value FortiCloud and device access credentials during audit workflows. <br>
Mitigation: Install only for authorized FortiSASE audits, use scoped read-only API tokens or approved service principals, avoid personal FortiCloud passwords, and keep MFA bypasses limited to formally approved machine-to-machine access. <br>
Risk: Audit outputs may include sensitive tenant, endpoint, logging, and security posture details. <br>
Mitigation: Treat generated reports and collected data as sensitive, limit distribution to approved security and network operations personnel, and store results in approved systems. <br>


## Reference(s): <br>
- [FortiSASE REST API Reference](artifact/references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown audit workflow with API request examples, threshold tables, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit posture; requires authorized FortiSASE access and a scoped API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

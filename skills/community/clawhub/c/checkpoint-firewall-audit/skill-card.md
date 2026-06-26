## Description: <br>
Check Point R80+/R81.x firewall audit guidance for rulebase layer analysis, blade activation, SmartConsole management-plane validation, NAT policy review, identity awareness assessment, and compliance verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers, firewall administrators, and compliance reviewers use this skill to audit Check Point R80+/R81.x environments for policy exposure, management-plane health, NAT behavior, blade coverage, identity awareness, and logging gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firewall audits can expose sensitive rulebases, gateway topology, identity sources, and logging details. <br>
Mitigation: Use only authorized target environments, least-privilege read-only accounts, and organization-approved handling for reports and command output. <br>
Risk: Management API passwords, SSH credentials, or session tokens could be exposed if included in prompts, logs, or generated reports. <br>
Mitigation: Keep credentials and session tokens out of prompts and logs, and redact sensitive values before sharing audit material. <br>
Risk: Remediation recommendations may affect production firewall policy if applied without review. <br>
Mitigation: Have a firewall administrator validate findings and apply changes only through the normal change-control process. <br>


## Reference(s): <br>
- [Check Point CLI and API Reference](references/cli-reference.md) <br>
- [Check Point R80+ Policy Architecture](references/policy-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and an audit report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit workflow for Check Point Management Server, Security Gateway, and Multi-Domain Server environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

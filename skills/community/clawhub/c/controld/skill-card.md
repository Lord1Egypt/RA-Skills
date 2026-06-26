## Description: <br>
Manage Control D DNS filtering service via API for DNS profiles, devices, custom blocking rules, service filtering, analytics settings, and network diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AustinGarrod](https://clawhub.ai/user/AustinGarrod) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and DNS administrators use this skill to inspect and manage Control D DNS filtering accounts, profiles, devices, rules, analytics, billing, organization settings, provisioning, and mobile configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer broad Control D account areas, including DNS settings, billing, organizations, provisioning, mobile configuration, and endpoint deployment. <br>
Mitigation: Install only for intended Control D administration, prefer read-only or tightly scoped tokens, restrict token IP access, and require explicit human approval before write, delete, billing, organization, provisioning, mobileconfig, or endpoint-deployment actions. <br>
Risk: Remote installer commands and endpoint deployment flows can affect every targeted device. <br>
Mitigation: Verify the installer path before use and require approval for each affected device before running deployment commands. <br>


## Reference(s): <br>
- [Control D](https://controld.com) <br>
- [Control D Dashboard](https://controld.com/dashboard) <br>
- [Control D API Base URL](https://api.controld.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CONTROLD_API_TOKEN plus curl and jq; API responses are typically JSON, while mobile configuration operations can produce .mobileconfig files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

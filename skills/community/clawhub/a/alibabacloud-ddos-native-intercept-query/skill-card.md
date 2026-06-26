## Description: <br>
Queries and troubleshoots Alibaba Cloud DDoS Native Protection network-layer intercept records through the Aliyun CLI and maps intercepts to the protection policies that caused them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security, SRE, and operations engineers use this skill to investigate protected IP traffic drops, inspect DDoS Native Protection intercept records, and produce read-only policy-correlation and false-positive remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow changes local Aliyun CLI and plugin settings even though cloud-resource operations are presented as read-only. <br>
Mitigation: Install only when local CLI configuration changes are acceptable, review plugin updates separately where possible, and confirm AI-mode is disabled after use. <br>
Risk: The skill requires access to Alibaba Cloud credentials or profiles that can query DDoS protection metadata. <br>
Mitigation: Use a least-privilege RAM role or temporary STS credentials and avoid pasting or printing access keys in the agent session. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Default Protection Policy Details](references/default-policy-details.md) <br>
- [Packet Filter Edge Cases](references/packet-filter-edge-cases.md) <br>
- [DDoS Native Protection Intercept Query RAM Permission Checklist](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Success Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and summarized command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only investigation reports with intercept overviews, policy correlation, root-cause analysis, and remediation recommendations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

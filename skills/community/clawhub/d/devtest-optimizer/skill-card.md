## Description: <br>
Optimize Azure dev/test environment costs with auto-shutdown schedules and Dev/Test pricing enrollment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to analyze user-provided Azure VM, cost, and subscription exports, estimate dev/test waste, and draft shutdown schedules, runbooks, and policy tagging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure exports may contain secrets or unnecessary sensitive fields. <br>
Mitigation: Review exports before use and remove credentials, access keys, secret keys, and fields not needed for cost analysis. <br>
Risk: Generated shutdown schedules, runbooks, and policies may not match operational requirements. <br>
Mitigation: Treat outputs as drafts and verify scopes, exclusions, business-hour assumptions, and always-on workloads before applying them in Azure. <br>
Risk: Dev/Test pricing eligibility may be misunderstood or applied to ineligible environments. <br>
Mitigation: Confirm Visual Studio subscription requirements and subscription eligibility before relying on estimated Dev/Test savings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Azure CLI examples, savings analysis, schedules, PowerShell runbook drafts, and Azure Policy guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output based on user-provided exports; it does not access Azure directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

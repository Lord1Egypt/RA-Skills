## Description: <br>
Run a read-only health inspection on Alibaba Cloud MongoDB (DDS) instances and produce standardized reports for Sharding and ReplicaSet deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud database operators and support engineers use this skill to inspect Alibaba Cloud DDS MongoDB instances for resource usage, slow queries, sessions, alerts, storage, and configuration risks. It helps assemble and run the supported inspection command and return the generated report path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Alibaba Cloud DDS inspections, including whole-account scans that collect fleet metadata and operational details. <br>
Mitigation: Use a least-privilege RAM role or short-lived credentials, and avoid broad --all scans unless the user explicitly needs account-wide coverage. <br>
Risk: Generated reports may contain sensitive slow query text, session data, alert history, and infrastructure metadata. <br>
Mitigation: Store reports in a secure location, restrict sharing, and remove reports when they are no longer needed. <br>
Risk: The installation guidance includes broad install or update paths for the Aliyun CLI and plugins. <br>
Mitigation: Prefer trusted package-manager or manually verified installation paths, and avoid curl-to-bash installation in agent sessions. <br>
Risk: Alibaba Cloud credentials are required for inspection and could expose sensitive access if mishandled. <br>
Mitigation: Never read or print AK/SK values; verify credential presence only with approved CLI status commands and guide users to configure credentials outside the agent session. <br>


## Reference(s): <br>
- [Aliyun CLI Installation & Configuration Guide](artifact/references/cli-installation-guide.md) <br>
- [Manual Workflow Reference](artifact/references/manual-workflow.md) <br>
- [RAM Permissions](artifact/references/ram-policies.md) <br>
- [Inspection Report Output Format Specification](artifact/references/report-format.md) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Markdown, Guidance] <br>
**Output Format:** [HTML reports by default, optional Markdown or text reports, and a report file path returned to the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written to ~/Downloads by default; multi-instance inspections include an index.html summary.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

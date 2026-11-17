## Description: <br>
Public network MTR diagnosis tool that guides manual MTR collection and can run Alibaba Cloud Cloud Assistant diagnostics on ECS instances for public network failures, high latency, packet loss, SLB health check failures, NAT outbound packet loss, and EIP bandwidth issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network engineers use this skill to troubleshoot public network connectivity, latency, packet loss, SLB health checks, NAT outbound behavior, and EIP bandwidth issues with manual MTR guidance or ECS-based Cloud Assistant diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated mode can use Alibaba Cloud ECS Cloud Assistant remote command execution authority. <br>
Mitigation: Install only with a tightly scoped RAM policy for intended ECS instances, review each proposed command before approval, and avoid raw run-command usage. <br>
Risk: Diagnostic enrichment may share network metadata with ipinfo.io. <br>
Mitigation: Treat ipinfo.io lookup as third-party metadata sharing and disable or avoid enrichment when that disclosure is not acceptable. <br>
Risk: Security evidence flags broader-than-needed remote command execution paths and a TLS-verification fallback. <br>
Mitigation: Prefer a revised release that removes the TLS-verification fallback and restricts remote execution to fixed diagnostic templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-network-mtr-diagnosis) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [MTR Diagnosis Reference](references/reference.md) <br>
- [Alibaba Cloud RAM documentation](https://www.alibabacloud.com/help/en/ram) <br>
- [WinMTR releases](https://github.com/White-Tiger/WinMTR/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured JSON when running bundled diagnostic scripts in automated ECS mode.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

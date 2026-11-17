## Description:

Read-only forensics for OSS traffic abuse and security incidents (overnight traffic spikes, suspected AK leak, hotlinking).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud OSS operators and developers use this skill to investigate unusual outbound traffic, suspected credential leaks, public bucket exposure, and hotlinking. It reviews bucket exposure and access logs, summarizes likely causes, and provides a manual containment checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented diagnosis workflow upgrades the Alibaba Cloud CLI in place, which can change shared software during a task presented as read-only.

Mitigation: Keep CLI installation or upgrades separate from diagnosis, and run investigations in a dedicated environment with a least-privilege read-only role and aligned CLI and environment credentials.

Risk: A generated blocking policy could disrupt legitimate bucket access; incomplete or empty IP inputs can make a proposed policy ineffective or misleading.

Mitigation: Treat policy text as a draft. Verify each intended IP/CIDR, check legitimate reader dependencies and public/VPC scope, and review the effect before applying it manually.

Risk: Incomplete access-log scans can produce partial evidence that may be mistaken for a complete traffic attribution.

Mitigation: Preserve incomplete-log warnings and state the limits of partial results; do not make a definitive root-cause claim until the evidence is complete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-security-incident-forensics)
- [Alibaba Cloud OSS traffic fees](https://help.aliyun.com/zh/oss/traffic-fees)
- [Alibaba Cloud SLS log fields 17](https://help.aliyun.com/zh/sls/log-fields-17)
- [Alibaba Cloud SLS log fields 13](https://help.aliyun.com/zh/sls/log-fields-13)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown report with evidence-based findings, a containment checklist, and optional SLS query statements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ready-to-run SLS read queries when log execution is unavailable; containment actions are manual guidance.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata, references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

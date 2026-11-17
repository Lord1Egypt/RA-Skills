## Description:

Diagnoses memory pressure on one Alibaba Cloud ECS Linux instance and guides evidence-based remediation for OOM kills, hangs, swap-related IOPS, and SSH failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud ECS operators and support engineers use this skill to diagnose memory pressure on Linux instances and choose evidence-based remediation, including Swap guidance, runtime limits, process investigation, staged restart guidance, or an upgrade recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, reporting consent bypasses and broad privileged system changes beyond its stated memory-diagnosis purpose.

Mitigation: Avoid installing until the consent bypasses and broad privileged changes are addressed and independently reviewed.

## Reference(s):

- [Swap configuration guidance](references/swap.md)
- [Process history with atop](references/atop.md)
- [Guest observation catalog](references/guest-observation-catalog.md)
- [RAM permissions and gated actions](references/ram-policies.md)
- [Staged restart guidance](references/restart-guide.md)
- [Node.js runtime memory limits](references/node-runtime.md)
- [Alibaba Cloud Swap configuration documentation](https://help.aliyun.com/zh/ecs/support/how-do-i-configure-the-swap-partition-of-a-linux-instance)
- [Alibaba Cloud atop monitoring documentation](https://help.aliyun.com/zh/ecs/user-guide/use-the-atop-tool-to-monitor-linux-system-metrics)
- [Node.js CLI documentation](https://nodejs.org/api/cli.html#--max-old-space-sizesize-in-mib)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Fixed-order text diagnosis report with a JSON evidence block and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports label evidence sources and unverified results; in-guest reads and Swap changes have separate consent or confirmation gates.]

## Skill Version(s):

0.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

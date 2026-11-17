## Description:

Provides read-only Alibaba Cloud OSS QPS, bandwidth quota, and throttling diagnostics for persistent 503/SlowDown errors, bandwidth saturation, timeout symptoms, optimization guidance, and quota-increase planning without making changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud OSS quota and throttling symptoms, interpret read-only diagnostic script output, and produce grounded remediation guidance. It is intended for persistent 503/SlowDown, QPS or bandwidth pressure, timeout-without-server-error, quota-increase, and resource-pool QoS consultation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed OSS diagnostics may expose more account context than intended if broad credentials are used.

Mitigation: Use narrowly scoped, preferably short-lived read-only Alibaba Cloud credentials for the target bucket.

Risk: Missing bucket input can trigger bucket-inventory fallback behavior.

Mitigation: Provide the exact bucket name and avoid account-wide bucket discovery when it is not needed.

Risk: A user-supplied endpoint could send diagnostic requests to an unintended host.

Mitigation: Use --endpoint only when it is a verified Alibaba Cloud OSS endpoint for the bucket region.

Risk: The skill may ask to upgrade the aliyun CLI before identity checks.

Mitigation: Approve any aliyun CLI upgrade separately under local change-control practices.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-quota-throttling-diagnosis)
- [Throttling Attribution Decision Tree](references/diagnosis-tree.md)
- [OSS Quota & Throttling Rules](references/throttling-rules.md)
- [Performance Optimization Guide](references/performance-guide.md)
- [Quota Increase & Dedicated Resource Guidance](references/quota-increase.md)
- [Minimal Read-Only RAM Policy](references/ram-policies.md)
- [Alibaba Cloud OSS Limits](https://help.aliyun.com/zh/oss/user-guide/limits)
- [Alibaba Cloud OSS HTTP 503 Errors](https://help.aliyun.com/zh/oss/user-guide/http-status-code-503)
- [Alibaba Cloud OSS HTTP 429 Errors](https://help.aliyun.com/zh/oss/user-guide/429-error)
- [Alibaba Cloud OSS Throttling Monitoring](https://help.aliyun.com/zh/oss/user-guide/use-cloudmonitor-to-monitor-oss-throttling-information-in-real-time)
- [Alibaba Cloud OSS Bandwidth or QPS Overrun Troubleshooting](https://help.aliyun.com/zh/oss/troubleshoot-bandwidth-or-qps-overrun-for-buckets-in-oss)
- [Alibaba Cloud OSS Performance Best Practices](https://help.aliyun.com/zh/oss/user-guide/oss-performance-best-practices/)
- [Alibaba Cloud OSS Resource Pool QoS](https://help.aliyun.com/zh/oss/user-guide/oss-resource-pool-qos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured diagnostic findings, inline shell commands, and cited documentation links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic scripts emit JSON plus STATUS and NEXT_ACTION lines; final answers should preserve degraded-state warnings and avoid fabricated utilization data.]

## Skill Version(s):

0.0.1 (source: release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

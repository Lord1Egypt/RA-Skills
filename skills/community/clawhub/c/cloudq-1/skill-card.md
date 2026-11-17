## Description:

CloudQ helps agents inspect Tencent Cloud Smart Advisor architecture diagrams, evaluations, risk items, service authorization, and report workflows using Tencent Cloud credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochuanxv](https://clawhub.ai/user/xiaochuanxv)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations, platform, and ITOM teams use this skill to query Tencent Cloud Smart Advisor architecture inventory, architecture details, Well-Architected evaluations, risk strategies, and cloud inspection reports. It can also guide environment setup, CAM role configuration, passwordless console links, and Smart Advisor authorization steps when the user explicitly approves write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud API credentials and may create or use a CAM role for console-login workflows.

Mitigation: Use a tightly scoped Tencent Cloud subaccount or temporary credentials, review each requested CAM operation, and approve role creation or Smart Advisor authorization only when needed.

Risk: Passwordless Tencent Cloud console links and STS-derived access are sensitive.

Mitigation: Regenerate links only when needed, keep durations short, avoid pasting or logging full URLs, and do not cache or reuse generated links.

Risk: Long-lived AK/SK values in shell startup files increase exposure if the workstation is shared or compromised.

Mitigation: Prefer temporary credentials or a secrets manager, avoid persisting long-lived secrets in shell profiles, and use the cleanup workflow to remove local role configuration when finished.

Risk: Scanner guidance identifies TLS and unpinned dependency behavior that should be reviewed before use.

Mitigation: Install and verify trusted certificate dependencies, pin Python package versions where practical, and inspect dependency changes before running the helper scripts.

## Reference(s):

- [CloudQ ClawHub Skill Page](https://clawhub.ai/xiaochuanxv/skills/cloudq-1)
- [xiaochuanxv Publisher Profile](https://clawhub.ai/user/xiaochuanxv)
- [Tencent Cloud](https://cloud.tencent.com)
- [Tencent Cloud API Endpoint Scope](https://*.tencentcloudapi.com)
- [CloudQ Tencent Cloud Article](https://cloud.tencent.com/developer/article/2645159)
- [CreateAdvisorAuthorization API Reference](artifact/references/api/CreateAdvisorAuthorization.md)
- [DescribeArch API Reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API Reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API Reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API Reference](artifact/references/api/DescribeStrategies.md)
- [TSA Risk Plugin Reference](artifact/references/plugins/tsa-risk/SKILL.md)
- [TSA Risk Report Design Specification](artifact/references/plugins/tsa-risk/ReportDesignSpec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with shell command snippets, JSON command results, Tencent Cloud console links, and optional HTML or PNG report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce sensitive passwordless Tencent Cloud console links and local report files; generated links should be treated as credentials and not cached.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

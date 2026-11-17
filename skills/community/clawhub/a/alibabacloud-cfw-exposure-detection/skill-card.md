## Description:

Query and analyze Alibaba Cloud public network exposure, identify unnecessary exposed assets and ports, assess exposure risks, and generate remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security engineers use this skill to run read-only Alibaba Cloud Firewall exposure checks, review public IPs and ports, correlate vulnerability and attack signals, and produce prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes authenticated Alibaba Cloud Firewall queries and can affect the local Aliyun CLI configuration.

Mitigation: Use only with an authorized Alibaba Cloud account after confirming the intended account, region, and command scope.

Risk: The skill asks to install or update Aliyun CLI tooling and plugins automatically.

Mitigation: Prepare and pin trusted CLI tooling separately, and require confirmation before cloud API execution.

Risk: Exposure reports may contain sensitive public asset, port, vulnerability, or attack-event details.

Mitigation: Review output before sharing and redact credentials, tokens, local configuration content, and unnecessary infrastructure details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-exposure-detection)
- [Related APIs](references/related-apis.md)
- [Cloud Firewall API Analysis](references/api-analysis.md)
- [RAM Policies](references/ram-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline Aliyun CLI commands and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tables, partial API results, error summaries, and prioritized remediation recommendations.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

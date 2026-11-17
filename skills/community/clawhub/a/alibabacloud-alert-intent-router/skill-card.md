## Description:

Routes Alibaba Cloud alerts by parsing alert content, extracting resource parameters, looking up CMDB or cloud resource data, selecting a database, network reachability, or ECS diagnostic skill, and producing a root cause report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to triage Alibaba Cloud alerts, map them to the correct diagnostic workflow, and consolidate backend diagnostic results into a root cause report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad alert trigger terms may invoke the router in more situations than intended.

Mitigation: Confirm the trigger posture is acceptable for the agent environment before installing.

Risk: The skill may perform CMDB or cloud resource lookups while triaging alerts.

Mitigation: Use least-privilege read-only RAM credentials and ensure users understand when lookups may run.

Risk: Manual CLI setup can introduce supply-chain or configuration risk.

Mitigation: Install Aliyun CLI only from trusted sources and verify the required version and plugins.

Risk: Root cause reports may include remediation commands that affect cloud resources.

Mitigation: Review report-suggested remediation commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-alert-intent-router)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [Enterprise CMDB](references/cmdb.md)
- [Intent Keywords Mapping](references/intent-keywords.md)
- [RAM Permissions Policy](references/ram-policies.md)
- [API Reference](references/related-apis.md)
- [Root Cause Report Template](references/root-cause-report-template.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Alibaba Cloud CLI configuration guide](https://help.aliyun.com/zh/cli/configure-aliyun-cli)
- [Alibaba Cloud authentication methods](https://help.aliyun.com/zh/cli/configure-credentials)
- [Aliyun CLI repository](https://github.com/aliyun/aliyun-cli)
- [Alibaba Cloud ECS documentation](https://help.aliyun.com/product/25365.html)
- [Alibaba Cloud NIS documentation](https://help.aliyun.com/product/134713.html)
- [Alibaba Cloud security group best practices](https://help.aliyun.com/document_detail/25475.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown status tables, backend skill call requests, and root cause report text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes to installed backend skills and summarizes their diagnostic results; proposed remediation commands require review before execution.]

## Skill Version(s):

0.0.1-beta.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

查询火山引擎 ARK 拆分账单明细及结算金额，可按账期、Endpoint、API Key 和产品过滤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

面向使用火山引擎 ARK 的开发者和运维人员，查询及核对按账期、Endpoint、API Key 或产品拆分的结算账单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linked shared authentication skill was outside this release's security scan scope.

Mitigation: Review the shared authentication guidance and follow the host's authentication protocol before running billing queries.

## Reference(s):

- [Billing list parameters](artifact/references/arkcli-billing-list.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Text]

**Output Format:** [arkcli billing commands and JSON billing results summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monthly billing periods; results may be paginated or truncated. Billing amounts are CNY strings, and current-period results may be incomplete due to T+1 posting.]

## Skill Version(s):

1.0.0 (source: target release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

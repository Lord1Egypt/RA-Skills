## Description:

Alibaba Cloud Governance Center evaluation report skill for querying governance maturity check results, generating structured risk reports, and account compliance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operations teams, and security reviewers use this skill to inspect Alibaba Cloud Governance Center maturity results, prioritize risks, and get focused remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Aliyun CLI plugin updates and automatic plugin installation behavior that may persist beyond a single report run.

Mitigation: Enable automatic plugin installation only when that persistent CLI behavior is acceptable, avoid updating unrelated plugins, and review local CLI configuration after use.

Risk: The skill invokes the local Aliyun CLI with the user's current cloud credentials to query Governance Center data.

Mitigation: Use a dedicated read-only Governance Center profile where possible, confirm user-selectable parameters before execution, and avoid credentials with broader permissions than the report requires.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-governance-evaluation-report)
- [Aliyun CLI releases](https://github.com/aliyun/aliyun-cli/releases)
- [Alibaba Cloud Governance Center documentation](https://help.aliyun.com/zh/governance/)
- [Governance API reference](https://help.aliyun.com/zh/governance/developer-reference/api-governance-2021-01-20-overview)
- [CLI installation guide](references/cli-installation-guide.md)
- [RAM policies](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Verification methods](references/verification-method.md)
- [Overview report format](references/report-format-overview.md)
- [Pillar report format](references/report-format-pillar.md)
- [Detail report format](references/report-format-detail.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation reports with inline shell commands and structured JSON from helper queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are emitted in conversation and are not written to files; helper metadata may be cached locally.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

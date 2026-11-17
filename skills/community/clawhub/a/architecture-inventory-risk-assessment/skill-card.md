## Description:

Inventory your cloud architectures and assess risks. Query architecture blueprints, evaluate Well-Architected scores, and identify governance gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stinggit](https://clawhub.ai/user/stinggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to inspect Tencent Cloud Smart Advisor architecture inventories, retrieve Well-Architected evaluations, and surface governance or risk gaps for the current Tencent Cloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tencent Cloud account credentials and can request broad cloud permissions.

Mitigation: Use a dedicated least-privilege Tencent Cloud sub-account, review requested IAM operations before use, and avoid storing long-lived SecretKeys in shell profiles.

Risk: The security summary reports weakened network safety.

Mitigation: Require standard TLS verification and remove insecure TLS fallback behavior before using the skill in a sensitive account.

Risk: The security summary flags unrelated bulk-publishing material in the artifact.

Mitigation: Remove or quarantine publishing files before deploying the skill for operational cloud account access.

Risk: Generated login links can grant direct console access for their validity window.

Mitigation: Generate login links only on explicit user request, do not log or share them, and prefer short-lived sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stinggit/skills/architecture-inventory-risk-assessment)
- [Tencent Cloud Smart Advisor console](https://console.cloud.tencent.com/advisor)
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi)
- [DescribeArch API reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API reference](artifact/references/api/DescribeStrategies.md)
- [ListDirectoryV2 API reference](artifact/references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API reference](artifact/references/api/ListUnorganizedDirectory.md)
- [CreateAdvisorAuthorization API reference](artifact/references/api/CreateAdvisorAuthorization.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud API response summaries and generated console links when the user explicitly requests authorized actions.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

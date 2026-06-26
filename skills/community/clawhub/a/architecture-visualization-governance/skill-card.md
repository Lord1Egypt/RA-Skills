## Description: <br>
Visualize and govern your cloud architectures. Get architecture assessments, risk heatmaps, and compliance dashboards in one place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stinggit](https://clawhub.ai/user/stinggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators and architecture reviewers use this skill to query Tencent Cloud Smart Advisor for architecture directories, architecture details, Well-Architected assessment results, risk evaluation items, and console links for the current Tencent Cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request broad Tencent Cloud authority, create or delete CAM roles, attach role policies, and open Smart Advisor authorization. <br>
Mitigation: Use a least-privilege Tencent Cloud subaccount or temporary credentials, review any proposed role or policy before creation, and require explicit user consent before write operations. <br>
Risk: Generated Tencent Cloud console login links can grant direct console access for their validity period. <br>
Mitigation: Do not share generated login links, keep credential duration short, and regenerate links only when the user needs them. <br>
Risk: Fallback TLS handling can disable certificate verification in some network environments. <br>
Mitigation: Run only in environments with working certificate validation and do not use the skill where TLS verification may be disabled. <br>
Risk: The artifact includes unrelated bulk-publishing guidance for avoiding ClawHub anti-spam controls. <br>
Mitigation: Ignore or remove the unrelated publishing guide before installation and review the cloud automation files that are relevant to Smart Advisor. <br>
Risk: Long-lived Tencent Cloud AK/SK values in shell startup files increase credential exposure. <br>
Mitigation: Prefer temporary credentials or a least-privilege subaccount and avoid storing long-lived credentials in persistent shell configuration. <br>


## Reference(s): <br>
- [Tencent Cloud API domain](https://cloud.tencent.com) <br>
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud CAM roles](https://console.cloud.tencent.com/cam/role) <br>
- [Tencent Cloud Smart Advisor console](https://console.cloud.tencent.com/advisor) <br>
- [DescribeArch API reference](references/api/DescribeArch.md) <br>
- [DescribeArchList API reference](references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API reference](references/api/DescribeStrategies.md) <br>
- [ListDirectoryV2 API reference](references/api/ListDirectoryV2.md) <br>
- [ListUnorganizedDirectory API reference](references/api/ListUnorganizedDirectory.md) <br>
- [CreateAdvisorAuthorization API reference](references/api/CreateAdvisorAuthorization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown responses with shell command snippets, JSON API results, and Markdown console links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Tencent Cloud credentials; generated console login links are time-limited and should not be shared.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

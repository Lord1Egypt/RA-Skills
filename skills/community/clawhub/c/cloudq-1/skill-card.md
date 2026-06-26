## Description: <br>
CloudQ helps agents work with Tencent Cloud Smart Advisor by checking setup, calling Advisor APIs, viewing architecture details and evaluations, querying risks, and guiding service authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaochuanxv](https://clawhub.ai/user/xiaochuanxv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use CloudQ to inspect Tencent Cloud Smart Advisor architecture data, retrieve evaluation and risk information, and generate guided links or setup steps for Advisor workflows. It requires Tencent Cloud credentials and should be used only with credentials and permissions appropriate for the target account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Tencent Cloud credentials that may perform CAM, STS, Advisor, and tag-related operations. <br>
Mitigation: Use least-privilege or temporary credentials, review policies before creating roles, and avoid storing long-lived AK/SK values in shell profiles. <br>
Risk: Security evidence flags under-disclosed setup behavior, runtime installs, an unpinned npx fallback, and TLS fallback behavior. <br>
Mitigation: Review the scripts and exact setup actions before installation, and avoid running environment checks or PNG conversion in sensitive environments until those issues are fixed. <br>
Risk: Role creation, role deletion, and Smart Advisor authorization can change cloud account state. <br>
Mitigation: Run only after explicit user approval and confirm the target Tencent Cloud account before any write operation. <br>


## Reference(s): <br>
- [CloudQ on ClawHub](https://clawhub.ai/xiaochuanxv/cloudq-1) <br>
- [Tencent Cloud](https://cloud.tencent.com) <br>
- [Tencent Cloud Smart Advisor Console](https://console.cloud.tencent.com/advisor) <br>
- [CreateAdvisorAuthorization API](references/api/CreateAdvisorAuthorization.md) <br>
- [DescribeArch API](references/api/DescribeArch.md) <br>
- [DescribeArchList API](references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API](references/api/DescribeStrategies.md) <br>
- [ListDirectoryV2 API](references/api/ListDirectoryV2.md) <br>
- [TSA Risk Plugin](references/plugins/tsa-risk/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API results, and generated report artifacts from the bundled risk plugin] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration under ~/.tencent-cloudq/ and may generate console login links or PNG reports when the corresponding workflows are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

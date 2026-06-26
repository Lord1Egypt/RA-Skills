## Description: <br>
Architecture governance and assessment tool. Evaluate cloud architectures against best practices and generate actionable improvement reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2513483494](https://clawhub.ai/user/2513483494) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud architects, platform engineers, and operations teams use this skill to query Tencent Cloud Smart Advisor architecture diagrams, risk checks, Well-Architected assessment results, and related governance recommendations for the currently configured Tencent Cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud AK/SK credentials and can perform IAM-sensitive actions such as role creation, policy attachment, STS role assumption, and Smart Advisor authorization. <br>
Mitigation: Use short-lived or least-privilege credentials, review every role and policy before approval, and require explicit user consent before running write operations. <br>
Risk: Generated passwordless console-login URLs can provide direct access to Tencent Cloud console pages during their validity window. <br>
Mitigation: Treat generated login URLs as sensitive, avoid exposing raw URLs, regenerate them only when needed, and keep STS durations as short as practical. <br>
Risk: The bundled publishing guide is unrelated to normal Smart Advisor use and is flagged by security evidence as potentially helping bypass ClawHub anti-spam controls. <br>
Mitigation: Do not use the publishing guide for runtime operation; remove or review it before redistribution. <br>
Risk: The artifact recommends persistent shell profile storage for long-lived Tencent Cloud credentials. <br>
Mitigation: Prefer temporary credentials or a managed secret store, and avoid committing or logging credential values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2513483494/architecture-governance-assessment) <br>
- [Tencent Cloud](https://cloud.tencent.com) <br>
- [DescribeArchList API reference](references/api/DescribeArchList.md) <br>
- [DescribeArch API reference](references/api/DescribeArch.md) <br>
- [DescribeLastEvaluation API reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API reference](references/api/DescribeStrategies.md) <br>
- [CreateAdvisorAuthorization API reference](references/api/CreateAdvisorAuthorization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Tencent Cloud Smart Advisor query results, governance advice, environment-check status, and generated console-login links.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

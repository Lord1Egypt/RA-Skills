## Description: <br>
Provides guided analysis for Anduoduo OpenClaw API risk, compliance, and cloud asset queries, including aggregate checks, drilldowns, and HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anduoduo](https://clawhub.ai/user/anduoduo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators and engineers use this skill to query Anduoduo/OpenClaw for cloud asset risk posture, rule drilldowns, and compliance summaries, then turn results into text, tables, or HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Anduoduo/OpenClaw API key and may perform authenticated API actions. <br>
Mitigation: Install only for intended Anduoduo/OpenClaw use, confirm API actions before execution, and provide the API key through the documented environment variable rather than storing it in files. <br>
Risk: The referenced cloud-account onboarding flow can involve raw cloud-provider AK/SK credentials. <br>
Mitigation: Avoid pasting cloud-provider AK/SK unless intentionally onboarding a cloud account, use least-privilege credentials, and review the action before submission. <br>
Risk: Generated reports may include sensitive cloud account, asset, risk, or compliance details. <br>
Mitigation: Review generated reports before sharing or uploading, and redact sensitive account or asset details when the destination is not trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anduoduo/anduoduo-openclaw-skill) <br>
- [Anduoduo platform](https://www.anduoduo.cloud/) <br>
- [Anduoduo API reference](references/anduoduo_api_final.md) <br>
- [API understanding and query playbook](references/api_understanding_and_query_playbook.md) <br>
- [Best practices](references/best_practices.md) <br>
- [Verification status](references/verification_status.md) <br>
- [Report guidelines](references/report_guidelines.md) <br>
- [Delivery strategy](references/delivery_strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files] <br>
**Output Format:** [Markdown guidance with API request examples and generated HTML, CSV, JSON, or ZIP files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ANDUODUO_API_KEY for authenticated Anduoduo/OpenClaw requests and may generate HTML reports from query results.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Dexter Research helps an agent analyze A-share listed companies by collecting stock data, financial indicators, capital-flow data, price history, and industry information, then producing scored research output and a Feishu-ready summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushang555](https://clawhub.ai/user/qiushang555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate structured A-share company research from a stock code or company name. The skill supports financial scoring, JSON report generation, and optional Feishu delivery for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be sent to an unintended Feishu recipient because the script includes a hard-coded default recipient.

Mitigation: Require an explicitly configured Feishu recipient before enabling message delivery, and disable sending when no recipient is configured.

Risk: Documentation includes a realistic secret-like Feishu credential example.

Mitigation: Remove or replace the published secret-like value and rotate it if it may have been real.

Risk: Unpinned dependencies and network data collection can change runtime behavior over time.

Mitigation: Pin dependency versions, review upstream data-source changes, and run the skill in an isolated workspace with restricted output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiushang555/skills/dexter-research)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Tencent Finance K-line API endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and generated JSON research data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The research script writes a JSON report and can send a text summary through Feishu when credentials are configured.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

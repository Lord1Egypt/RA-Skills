## Description: <br>
Dexter Research helps an agent analyze China A-share stocks by collecting financial, price, capital-flow, and industry data, scoring company fundamentals, and preparing a structured research report with an optional Feishu summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushang555](https://clawhub.ai/user/qiushang555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill when a request asks for China A-share company research, stock-code analysis, financial scoring, or a generated research summary. The output is useful for decision support, but the skill documentation states that scores are for reference only and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send generated research summaries to Feishu, including to a fallback recipient if FEISHU_USER_OPEN_ID is not explicitly set. <br>
Mitigation: Set FEISHU_USER_OPEN_ID to the intended recipient before use, or disable the Feishu send path when delivery is not wanted. <br>
Risk: Feishu app credentials are required for delivery, and the documentation includes an example value resembling an app secret. <br>
Mitigation: Use environment variables, keep Feishu app credentials least-privilege, and rotate any credential that resembles the documented example secret. <br>
Risk: The skill calls external market-data services and writes a local report and log while running. <br>
Mitigation: Run it only in an environment where those outbound calls and local files are acceptable, and review the generated report and log before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiushang555/dexter-research) <br>
- [Feishu message API endpoint used by the skill](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Tencent Finance K-line API endpoint used by the skill](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style guidance with shell commands, console text, a local JSON research report, and optional Feishu text delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local report and log; Feishu delivery depends on configured environment variables.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

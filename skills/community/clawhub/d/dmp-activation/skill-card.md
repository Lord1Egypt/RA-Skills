## Description: <br>
基于明日DMP开放平台API，提供RTQ投放订单管理功能，支持创建、查询、修改投放订单。采用10步标准化工作流程，包含请求类型识别、凭证检查、参数引导、格式校验、参数确认、任务记录等完整流程。适用于精准广告投放、人群包投放、属性定向投放等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advertising operators and developers use this skill to manage Mingri DMP RTQ activation orders, including creating, querying, and modifying audience-targeted delivery orders after configuring API and RTQ credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RTQ and API credentials may appear in console output, terminal transcripts, or plaintext local credential files. <br>
Mitigation: Run the skill only in protected environments, redact logs before sharing them, restrict credential file access, and rotate credentials if they may have been captured. <br>
Risk: Order data and RTQ access details may be retained in local order caches. <br>
Mitigation: Limit access to local workspace files, remove cached order data when it is no longer needed, and avoid storing unnecessary credential fields in cache records. <br>
Risk: Authenticated API calls depend on locally discovered helper code. <br>
Mitigation: Review the installed authentication helper before use and keep helper discovery scoped to trusted skill installation paths. <br>
Risk: Incorrect audience IDs or order parameters can affect live advertising delivery. <br>
Mitigation: Use the skill's confirmation step, verify audience validation results, and require explicit user approval before creating or modifying orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingri26/dmp-activation) <br>
- [Mingri DMP authentication skill](https://clawhub.ai/mingri26/dmp-auth) <br>
- [Task logger skill](https://clawhub.ai/mingri26/dmp-skill-logger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style guidance with parameter confirmation tables, inline shell commands, and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mingri DMP API and RTQ credentials and may create local credential and order-cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

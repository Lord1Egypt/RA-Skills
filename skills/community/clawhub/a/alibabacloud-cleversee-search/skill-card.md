## Description: <br>
Alibaba Cloud cleversee CLI skill for AI-powered web search and web content retrieval through the cleversee CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Alibaba Cloud CleverSee web searches, confirm search parameters, parse JSON results, and manage credential checks for the cleversee CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential setup can configure local Alibaba Cloud profiles. <br>
Mitigation: Use existing scoped profiles where possible, confirm every profile and authentication parameter before use, and avoid exposing access keys in chat, shell output, or logs. <br>
Risk: Search or authentication commands may run with unintended user-customizable parameters. <br>
Mitigation: Confirm query, limit, search type, region, date ranges, domain filters, profile, and output mode with the user before executing cleversee commands. <br>
Risk: The skill requires Alibaba Cloud RAM permission to execute CleverSee searches. <br>
Mitigation: Grant only the documented AliyunCleverSeeAISearchPlatformUserAccess permission, and pause for permission remediation if CleverSee reports authorization errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cleversee-search) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud RAM Console](https://ram.console.aliyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation for customizable search, authentication, profile, date range, domain, and output parameters before command execution.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

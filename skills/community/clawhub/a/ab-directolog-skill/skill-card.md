## Description: <br>
A Yandex.Direct automation skill that helps an agent manage campaigns, retrieve advertising data, generate reports, analyze performance, and suggest bid or campaign optimizations through the Yandex.Direct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexburrstudio](https://clawhub.ai/user/alexburrstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advertising operators, marketers, and developers use this skill to connect an agent to Yandex.Direct, inspect campaigns and keywords, create or edit campaigns, request reports, and produce optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority over advertising campaigns, including campaign creation and bid or budget changes. <br>
Mitigation: Require explicit human approval or a dry-run review before any campaign, budget, bid, ad, or keyword mutation is executed. <br>
Risk: OAuth client secrets, access tokens, and refresh tokens are required and may be retained in memory or printed by example token-refresh behavior. <br>
Mitigation: Use a dedicated revocable Yandex application and token, keep secrets out of agent memory and logs, remove token printing, and redact diagnostics before use. <br>
Risk: Advertising reports and account data may include sensitive business performance information. <br>
Mitigation: Limit account scope, store reports only where authorized, and review generated summaries before sharing them outside the operational team. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexburrstudio/ab-directolog-skill) <br>
- [Publisher profile](https://clawhub.ai/user/alexburrstudio) <br>
- [Yandex.Direct token documentation](https://yandex.ru/dev/direct/doc/ru/token) <br>
- [Yandex OAuth application portal](https://oauth.yandex.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Yandex.Direct API endpoints using OAuth credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

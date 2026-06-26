## Description: <br>
帮助法律从业者和普通用户通过得理法律开放平台检索公开裁判文书、匹配类案并整理案例要点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal professionals and users seeking case references use this skill to search public Chinese court judgments by keyword, cause of action, court, date, document type, case number, or long-form case materials. It presents results as case lists, case details, similar-case comparisons, and concise ruling-point summaries rather than legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API keys and potentially sensitive legal case text to Delilegal's external API. <br>
Mitigation: Use only with an approved Delilegal account, avoid confidential, privileged, personal, or unredacted case materials, and review what will be sent before executing a search. <br>
Risk: The API script disables HTTPS certificate verification while transmitting credentials and search content. <br>
Mitigation: Fix TLS certificate verification before relying on the skill with real API keys or sensitive legal data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/case-retrieval) <br>
- [Search examples](references/search-examples.md) <br>
- [Delilegal case search API endpoint](https://platform.delilegal.com/api/v1/generice/case/list) <br>
- [Delilegal API key console](https://open.delilegal.com/personal/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, tables, and command or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paginated case lists, case details, similar-case comparison tables, ruling-point summaries, and retrieval caveats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Automates Founder-HongYun academic publishing workflows, including journal switching, review reminders, DOI registration, task summaries, and optional WeChat article publishing through browser-based platform interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[behurry](https://clawhub.ai/user/behurry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Journal editors, publishing operators, and developers use this skill to operate the Founder-HongYun publishing platform, review overdue manuscripts, register DOI records, and publish selected article content to WeChat when authorized credentials are supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use authenticated Founder-HongYun sessions and WeChat credentials to make public or official publishing changes without strong final confirmation safeguards. <br>
Mitigation: Require the assistant to show the exact article, account, preview, DOI targets, and API action, then obtain explicit user approval before any publish, register, reminder, or submission step. <br>
Risk: Cookies, AppIDs, and AppSecrets may grant access to publishing accounts if exposed during a session. <br>
Mitigation: Use least-privileged accounts, enter secrets only when needed, avoid displaying or logging raw cookies and AppSecrets, and clear session credentials after sensitive workflows. <br>
Risk: The optional WeChat workflow uses shell curl commands against external API endpoints. <br>
Mitigation: Inspect the exact command and target endpoint before execution, keep requests limited to documented WeChat API endpoints, and supervise returned publish identifiers and article URLs. <br>
Risk: Automated manuscript, DOI, and reminder workflows can act on the wrong article, journal, issue, or reviewer if search results or session state are stale. <br>
Mitigation: Confirm the current journal, organization code, article title, article ID, issue, reviewer targets, and returned API status before continuing with high-impact actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/behurry/founder-hy-editor-browser) <br>
- [Setup guide](artifact/setup.md) <br>
- [Founder-HongYun platform](http://journal.portal.founderss.cn/) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with browser action guidance, JSON/API summaries, status messages, URLs, identifiers, and inline shell curl commands when WeChat publishing is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may rely on authenticated browser sessions and user-provided Founder-HongYun or WeChat credentials; public publishing and DOI operations should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

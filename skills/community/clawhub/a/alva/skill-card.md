## Description: <br>
Alva helps agents fetch financial data, research markets, backtest strategies, and build live dashboards and playbooks on the Alva platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaxxjj](https://clawhub.ai/user/jaxxjj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance-focused users use this skill to ask agents for current financial data, market research, strategy backtests, and hosted playbooks or dashboards that run on Alva Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to authenticate with an Alva account, manage credentials, and install or upgrade a global npm CLI. <br>
Mitigation: Ask for explicit approval before running setup scripts, changing global tools, logging in, or handling account-linked credentials. <br>
Risk: The skill can create persistent cloud automations, push notifications, and trading-related workflows. <br>
Mitigation: Require user confirmation before deploying automations, enabling notifications, starting paper trading, or executing any trading action. <br>
Risk: Playbooks and feeds may be released or shared publicly. <br>
Mitigation: Review visibility, data sources, and generated content before granting public access or releasing a playbook. <br>
Risk: Memory-based personalization may read or store user investment preferences and related context. <br>
Mitigation: Review what memory is read or saved, keep secrets out of memory, and confirm updates before persisting sensitive preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaxxjj/alva) <br>
- [Feed SDK Guide](references/feed-sdk.md) <br>
- [Altra Trading Engine](references/altra-trading.md) <br>
- [Deployment Guide](references/deployment.md) <br>
- [Secret Manager](references/secret-manager.md) <br>
- [Release API](references/api/release.md) <br>
- [Trading API](references/api/trading.md) <br>
- [Push Subscriptions API](references/api/push-subscriptions.md) <br>
- [AI Digest Template](templates/ai-digest/template.md) <br>
- [Ranked-List Screener Template](templates/screener/template.md) <br>
- [Thesis Tracking Template](templates/thesis/template.md) <br>
- [What-If Playbook Template](templates/what-if/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with code blocks, CLI commands, JavaScript feed and playbook code, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hosted playbook links, financial analyses, generated scripts, and deployment guidance.] <br>

## Skill Version(s): <br>
1.7.1 (source: server release metadata; artifact frontmatter says v1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

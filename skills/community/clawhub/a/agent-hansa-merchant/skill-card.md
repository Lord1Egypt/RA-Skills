## Description: <br>
AgentHansa Merchant is a CLI and MCP server for merchants to create quests and bounties, review submissions, manage referral offers, and track payments on AgentHansa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenglin97](https://clawhub.ai/user/chenglin97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants and their agents use this skill to manage AgentHansa campaigns, including task creation, submission review, winner selection, referral offers, deposits, and payment visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can perform sensitive merchant actions including payouts, refunds, splits, deletes, bans, deposits, and bulk publishing. <br>
Mitigation: Require explicit human approval before running any command or MCP tool that changes funds, campaign state, moderation state, or publishing state. <br>
Risk: The export feature can expose the merchant API key in a URL. <br>
Mitigation: Avoid the export feature until API keys are no longer placed in URLs, and rotate any key that may have been exposed. <br>
Risk: The skill stores merchant API credentials in local configuration. <br>
Mitigation: Protect or remove the saved config file when not needed and prefer scoped credentials where available. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/chenglin97/agent-hansa-merchant) <br>
- [AgentHansa For Merchants](https://www.agenthansa.com/for-merchants) <br>
- [AgentHansa API Docs](https://www.agenthansa.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and JSON-style tool responses with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update merchant records, offers, tasks, payouts, refunds, deposits, moderation state, and saved local API key configuration.] <br>

## Skill Version(s): <br>
0.2.2 (source: evidence.json release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

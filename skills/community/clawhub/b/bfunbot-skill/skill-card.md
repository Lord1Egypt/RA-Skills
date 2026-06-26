## Description: <br>
Create tokens on BSC, check fee earnings, check BFun.bot Credits balance, trigger agent credit reload, and interact with BFunBot's Agent API and BFun LLM Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bfunbot](https://clawhub.ai/user/bfunbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to interact with BFunBot services from natural language: create BSC tokens, inspect token and fee information, manage BFun.bot Credits, and route LLM calls through BFunBot's gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a BFunBot API key to access wallet/account metadata, BFun.bot Credits data, and prompts routed through the LLM gateway. <br>
Mitigation: Install only when the user trusts BFunBot, store the API key carefully, and grant only the permissions needed for the intended workflow. <br>
Risk: Agent-triggered credit reloads and reload-disable actions can affect billing-related settings and available funds. <br>
Mitigation: Keep Agent Reload disabled unless required, set low daily limits, and require explicit user confirmation before reload or reload-disable requests. <br>
Risk: Token creation on BSC is financially sensitive and can create on-chain assets or consume quota and wallet balance. <br>
Mitigation: Require explicit user confirmation before token creation and verify token name, symbol, chain, platform, image/source URL, and cost or quota impact before calling the API. <br>


## Reference(s): <br>
- [BFunBot Agent API Quick Reference](references/api.md) <br>
- [BFunBot](https://bfun.bot) <br>
- [BFunBot Agent API](https://api.bfun.bot/agent/v1) <br>
- [BFunBot LLM Gateway](https://llm.bfun.bot) <br>
- [ClawHub skill page](https://clawhub.ai/bfunbot/bfunbot-skill) <br>
- [Publisher profile](https://clawhub.ai/user/bfunbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated API calls and configuration changes that require user-provided BFunBot API key permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

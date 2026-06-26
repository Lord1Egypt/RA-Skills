## Description: <br>
Gate welfare center and new-user task skill for answering welfare, reward, and task-claiming questions using real Gate MCP data only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users and support agents use this skill to check welfare eligibility, retrieve new-user onboarding tasks, and provide fallback guidance for existing or restricted accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad welfare, task, or reward triggers may route generic user questions into the Gate welfare workflow. <br>
Mitigation: Ask for clarification when intent is ambiguous and route trading, asset, funding, or KYC completion intents to the appropriate skill or official Gate surface. <br>
Risk: The skill requires a Gate MCP session with API credentials. <br>
Mitigation: Use an API key restricted to Welfare:Read and never ask users to paste secrets into chat. <br>
Risk: Reward or task responses could mislead users if example values are used as live data. <br>
Mitigation: Call the identity endpoint first, render only fields returned by the beginner task list endpoint, and fall back to the official rewards hub when live data is unavailable. <br>


## Reference(s): <br>
- [Gate skills homepage](https://github.com/gate/gate-skills) <br>
- [Gate rewards hub](https://www.gate.com/rewards_hub) <br>
- [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate welfare MCP specification](references/mcp.md) <br>
- [Gate welfare runtime rules](references/gate-runtime-rules.md) <br>
- [MCP data usage examples](references/mcp-data-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted user guidance with task lists and fallback messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only real MCP-returned task and reward fields; does not claim rewards or perform writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

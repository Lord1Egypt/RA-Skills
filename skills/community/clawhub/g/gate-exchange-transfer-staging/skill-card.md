## Description: <br>
Gate Exchange same-UID internal transfer skill. Use when the user asks to move funds between their own Gate accounts. Triggers on 'transfer funds', 'move USDT to futures', 'internal transfer'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to prepare and execute same-UID internal transfers between their own Gate spot, isolated margin, perpetual, delivery, and options accounts through a configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Gate Internal Transfer Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Exchange Transfer MCP Specification](references/mcp.md) <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/gate-exchange-transfer-staging) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown transfer drafts, confirmation prompts, API-call results, and ledger verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Gate API credentials, balance pre-checks, explicit immediate confirmation before writes, and post-transfer ledger verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Gate Exchange same-UID internal transfer skill. Use when the user asks to move funds between their own Gate accounts. Triggers on 'transfer funds', 'move USDT to futures', 'internal transfer'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with configured Gate MCP credentials use this skill to move funds between their own Gate account types under the same UID. The skill drafts, confirms, executes, and verifies internal transfers across supported account categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate internal fund transfers between Gate account types when connected to a configured Gate MCP session. <br>
Mitigation: Use a dedicated least-privilege Gate API key and require the user to confirm the source, destination, currency, amount, and risk note before any transfer is executed. <br>
Risk: Incorrect account, currency, amount, or route selection could move funds to an unintended account type. <br>
Mitigation: Present a transfer draft, block ambiguous requests, verify source balance where available, and execute only after explicit confirmation in the immediately following user turn. <br>


## Reference(s): <br>
- [Gate Skills Repository](https://github.com/gate/gate-skills) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate Internal Transfer Runtime Rules](artifact/references/gate-runtime-rules.md) <br>
- [Gate Exchange Transfer MCP Specification](artifact/references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown transfer drafts, confirmation prompts, execution results, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit confirmation gate before write operations and uses configured Gate MCP credentials rather than chat-provided secrets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

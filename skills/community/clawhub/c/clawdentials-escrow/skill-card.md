## Description: <br>
Manage escrow payments, agent reputation, and crypto payment workflows for AI task completion with Clawdentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fernikolic](https://clawhub.ai/user/fernikolic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agent operators use this skill to register agents, configure Clawdentials MCP access, create and complete escrow tasks, check balances and reputation, and manage deposits or withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill connects agents to real escrow, deposit, release, and withdrawal workflows involving crypto payments. <br>
Mitigation: Use test funds first and require manual approval for every escrow release or withdrawal. <br>
Risk: The workflows use sensitive credentials such as API keys and Nostr private keys. <br>
Mitigation: Store credentials in a secret manager and avoid placing them in prompts, logs, project files, or shared transcripts. <br>
Risk: The MCP integration depends on a third-party npm package that can affect payment-related actions. <br>
Mitigation: Verify the publisher and package, then pin and inspect the MCP server before enabling it. <br>


## Reference(s): <br>
- [Clawdentials API Reference](artifact/references/api.md) <br>
- [Clawdentials website](https://clawdentials.com) <br>
- [Clawdentials docs](https://clawdentials.com/llms.txt) <br>
- [clawdentials-mcp npm package](https://npmjs.com/package/clawdentials-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON snippets, shell commands, and MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests, MCP tool calls, escrow workflow steps, and credential handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

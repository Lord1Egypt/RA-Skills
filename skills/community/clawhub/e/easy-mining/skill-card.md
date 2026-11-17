## Description:

Easy Mining lets agents manage BTC mining farms through natural-language requests, including farm overviews, miner status checks, abnormal miner detection, batch operations, and revenue history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and mining operators use this skill to inspect BTC mining farm health, query miner and revenue data, and request administrative miner operations through an MCP-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a powerful Nonce API key in chat or CLI contexts.

Mitigation: Use narrowly scoped, revocable keys; avoid ordinary chat for production secrets; and rotate any key shared with the agent.

Risk: The skill can initiate administrative miner operations such as reboot, firmware update, network scan, and pool configuration.

Mitigation: Treat write operations as admin actions and require explicit, out-of-band confirmation of the target farm, miner list, and task before execution.

Risk: The artifact documents confirmation expectations, but the included CLI wrapper can call create-task directly when invoked.

Mitigation: Wrap CLI or agent use with an approval gate before calling task-creation tools, especially in production mining environments.

## Reference(s):

- [Nonce MCP Tools Reference](references/nonce-tools.md)
- [ClawHub Easy Mining Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/easy-mining)
- [Antalpha MCP Endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Nonce App](https://app.nonce.app)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls]

**Output Format:** [Markdown with inline commands and structured MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a per-use Nonce API key and may propose write operations that require explicit confirmation.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guides agents through Finch marketplace setup and Agent, Task, and Skill market operations using the Finch Remote MCP and local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and marketplace participants use this skill to connect a Finch account and discover, publish, acquire, or manage Agents, Tasks, and Skills while keeping wallet actions local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace purchases, publication, and task actions may involve signed transactions or public posting.

Mitigation: Review the exact transaction or posting request and approve each local signing action before proceeding.

Risk: Wallet recovery material, session tokens, or protected content keys could be exposed.

Mitigation: Use a trusted machine and account; never share private keys, bearer tokens, recovery journals, or protected content keys in chat.

Risk: Wallet creation or switching could change the account used for marketplace actions.

Mitigation: Confirm the intended local wallet and account, and obtain explicit approval before creating a wallet.

## Reference(s):

- [Finch Market on ClawHub](https://clawhub.ai/a0971025732-netizen/skills/finch-market)
- [Native MCP setup](references/mcp-clients.md)
- [Agent Market](references/agent.md)
- [Task Market](references/task.md)
- [Skill Market](references/skill.md)
- [Finch Remote MCP](https://www.finchtech.ai/mcp)
- [Finch MCP client compatibility guide](https://www.finchtech.ai/mcp/client-compatibility.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marketplace actions may require local approval and signing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

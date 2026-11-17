## Description:

Ava lets coding agents operate human-bounded DeFi lending workflows with sessions, mandates, two-phase previews, execution, and receipts with chain proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamalbuilds](https://clawhub.ai/user/kamalbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and coding-agent users use Ava to let an agent prepare and execute human-approved DeFi lending within a mandate, with a receipt that records chain proof. The packaged workflow distinguishes live USDC lending from testnet-only copilot tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged CLI exposes broader financial authority than the agent instructions describe.

Mitigation: Review the skill before deployment and restrict use to the dedicated two-phase lend flow for live capital.

Risk: Generic tool calls or live-mode settings could trigger state-changing financial behavior outside the expected path.

Mitigation: Avoid the generic call command for state-changing tools and do not set AVA_ENABLE_LIVE unless live execution is intentional and understood.

Risk: Stored bearer tokens can authorize later Ava requests if exposed.

Mitigation: Protect the stored Ava token, avoid printing it, and use the official API endpoint unless intentionally developing locally.

## Reference(s):

- [Ava homepage](https://getava.xyz)
- [Ava MCP endpoint](https://www.getava.xyz/mcp)
- [ClawHub Ava skill page](https://clawhub.ai/kamalbuilds/skills/ava)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON MCP or CLI responses, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-finance preview and receipt data; human confirmation is required before the execute flow.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Gate welfare center and new-user task skill for checking welfare rewards, tasks, and claim guidance using real Gate MCP data only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and support agents use this skill to check whether an authenticated account qualifies for new-user welfare tasks and to display eligible task status, rewards, or fallback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may invoke authenticated Gate welfare checks for generic task or reward questions.

Mitigation: Limit activation to explicit Gate welfare, new-user benefit, or reward-center requests and avoid using the skill for ordinary trading, deposit, or account-balance questions.

Risk: The skill uses configured Gate MCP credentials to retrieve account-specific welfare eligibility and task status.

Mitigation: Use only read-only Welfare:Read credentials through the local MCP session and never ask users to paste API keys or secrets into chat.

Risk: Displayed reward information could mislead users if example or stale task data is used.

Mitigation: Render only live fields returned by the approved Gate welfare MCP tools and fall back to the official rewards hub when data is unavailable.

## Reference(s):

- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate Rewards Hub](https://www.gate.com/rewards_hub)
- [Gate Welfare MCP Specification](references/mcp.md)
- [Gate Welfare Runtime Rules](references/gate-runtime-rules.md)
- [Proper MCP Data Usage Examples](references/mcp-data-usage.md)
- [Scenarios and Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with task lists, status summaries, links, and fallback guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated read-only Gate welfare data and should not fabricate task names, reward amounts, or task status.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

DEX代币分析 helps an agent analyze DEX token holder clusters, advanced trader activity, liquidity, tokenomics, and on-chain events for structured cryptocurrency market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading analysts use this skill to structure DEX token analysis around holder clusters, whale or advanced trader behavior, liquidity pools, tokenomics, and chain events. The skill can produce analysis workflows, configuration guidance, and structured outputs for market review, but its findings should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command-execution authority.

Mitigation: Run it only in a controlled agent environment and require explicit confirmation before any command, export, monitoring job, or scheduled task.

Risk: The skill may access financial APIs or cryptocurrency data without clearly stated privacy boundaries.

Mitigation: Use limited-scope API keys, avoid wallet private keys, and provide sensitive portfolio data only when necessary.

Risk: DEX token analysis can produce misleading or incomplete market conclusions.

Mitigation: Treat outputs as decision support, verify data sources independently, and do not rely on the skill as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dex-token)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON examples and command or configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve financial API access and command execution; review outputs before using them for trading or investment decisions.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

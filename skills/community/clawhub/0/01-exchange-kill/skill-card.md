## Description:

AI-powered 01.xyz exchange development skill for monitoring, trading strategies, and N1 blockchain integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bouncyknighter](https://clawhub.ai/user/bouncyknighter)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to build 01.xyz exchange monitoring, SDK integration, risk analysis, and trading workflow guidance. It is best suited for read-only market and account monitoring unless trading actions are separately audited and gated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live financial examples can place orders, move collateral, or close positions without reliable confirmation controls.

Mitigation: Use the skill for read-only market monitoring unless trading flows are audited and wrapped with explicit confirmation, hard limits, and independent checks.

Risk: Mainnet use can expose real funds to trading, leverage, liquidation, or stale-order failures.

Mitigation: Validate on devnet first, use low-value dedicated wallets, pin dependency versions, and require review before enabling mainnet actions.

## Reference(s):

- [01.xyz](https://01.xyz)
- [01.xyz Developer Docs](https://docs.01.xyz)
- [01.xyz API Reference](https://api.01.xyz)
- [N1 Blockchain Docs](https://docs.n1.xyz)
- [Nord TypeScript SDK](https://www.npmjs.com/package/@n1xyz/nord-ts)
- [Monitoring Guide](artifact/01xyz-developer-monitoring-guide.md)
- [Risk Management](artifact/01xyz-developer-risk-management.md)
- [Safety First](artifact/01xyz-developer-safety-first.md)
- [SDK Reference](artifact/01xyz-developer-sdk-reference.md)
- [Trading Basics](artifact/01xyz-developer-trading-basics.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial workflow guidance that requires human review before use with real funds.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

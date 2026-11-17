## Description:

CLAWP Agent - AI token creation advisor powered by OpenClaw

This skill is ready for commercial/non-commercial use.

## Publisher:

[iclawn](https://clawhub.ai/user/iclawn)

### License/Terms of Use:


## Use Case:

External users use this agent to turn a short meme-token idea into a structured launch blueprint with naming, narrative, visual direction, launch guidance, and buyback-and-burn planning. The skill is intended for the ClawPad/OpenClaw flow and should be reviewed before any real token launch or spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users toward real Solana spending and irreversible token-launch actions.

Mitigation: Require explicit confirmation outside the skill for wallet addresses, network, fees, automation rules, buyback-and-burn behavior, and loss risks before deposit or deployment.

Risk: Launch advice and buyback planning may be mistaken for investment advice or a promise of token performance.

Mitigation: Keep disclaimers visible, prohibit price predictions and profit promises, and require human review before acting on any launch or buyback plan.

Risk: Execution details are described as controlled or predefined, but the artifact does not expose enough operational controls for a reviewer to validate them.

Mitigation: Document and review the exact execution mechanics, custody boundaries, spending limits, and cancellation behavior before enabling production use.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [CLAWP ClawHub listing](https://clawhub.ai/iclawn/skills/clawp)
- [Publisher profile](https://clawhub.ai/user/iclawn)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with fenced JSON blueprint output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Blueprints include token name, symbol, description, narrative, visual direction, logo prompt, theme tags, buyback plan, and disclaimer fields.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Generate a daily priority leaderboard for 5 crypto tokens, with per-token fundamentals, liquidity, and risk summaries plus ready-to-publish drafts for X posts, group updates, and quick briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2663629531](https://clawhub.ai/user/2663629531)

### License/Terms of Use:


## Use Case:

External operators and agents use this skill to generate a daily crypto research pack from Binance Web3 market signals. It ranks five tokens, summarizes fundamentals, liquidity, and risk, and drafts publish-ready social and brief copy without providing investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid rank runs can create SkillPay charges when billing is enabled.

Mitigation: Only run rank when billing is intended, and use --skip-billing or SKILLPAY_BILLING_MODE=noop for testing.

Risk: Proxy diagnostics and custom proxy inputs can expose credential-bearing proxy URLs in output.

Mitigation: Avoid credential-bearing proxy URLs for proxy-check, or keep diagnostic output private.

Risk: Overridable SkillPay endpoints can route billing calls to unintended services.

Mitigation: Lock SkillPay endpoint configuration to the real HTTPS service in paid or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2663629531/skills/alpha-copilot-skill)
- [Binance Web3](https://web3.binance.com)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON or Markdown research report with ranked token summaries, risk notes, and publish-ready drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes billing status for rank runs and proxy diagnostics when requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

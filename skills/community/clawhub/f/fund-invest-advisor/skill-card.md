## Description:

Fund Invest Advisor helps with fund screening, dollar-cost averaging simulations, return calculations, asset allocation, risk assessment, and rebalancing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate educational fund-investment calculations, dollar-cost averaging scenarios, allocation suggestions, portfolio checks, and rebalancing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an under-documented portfolio script with command-injection and local code-execution risk.

Mitigation: Review and fix script.sh before use; do not run it with untrusted arguments or FUND_DIR values.

Risk: Portfolio commands may create or modify local portfolio data with data-integrity risk.

Mitigation: Back up local portfolio data and validate file paths and imported data before relying on portfolio outputs.

Risk: Investment outputs may be incorrect, incomplete, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as educational only and require qualified human review before making investment decisions.

## Reference(s):

- [Fund Invest Advisor on ClawHub](https://clawhub.ai/ckchzh/skills/fund-invest-advisor)
- [Fund Investment Practical Guide](tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with shell command examples and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are educational and may include local portfolio data written by the bundled shell scripts.]

## Skill Version(s):

2.3.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

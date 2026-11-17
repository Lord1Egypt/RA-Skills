## Description:

Provides a Howard Marks-style market-cycle score from 0 to 100 by blending VIX, SPY IV Rank, put/call ratio, and valuation percentile into an offense-versus-defense posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market-research agents use this skill to request a market-level cycle read and translate sentiment and valuation signals into a concise offensive/defensive posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce direct market posture suggestions that may be mistaken for personalized trading instructions.

Mitigation: Treat outputs as an informational market-sentiment framework and require human review before making investment or options-trading decisions.

Risk: The score is a simplified blend of market indicators and may omit context needed for a specific portfolio, objective, or risk tolerance.

Mitigation: Use the component breakdown as a starting point for analysis rather than as a standalone decision rule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-marks-cycle)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with structured market-cycle fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No input parameters; returns a 0-100 cycle score, posture label, English and Chinese posture text, per-signal components, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

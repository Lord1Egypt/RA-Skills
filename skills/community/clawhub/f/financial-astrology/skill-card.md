## Description:

Analyzes Vedic sidereal astrology indicators, including planetary positions, Nakshatra, houses, aspects, combustion, and market sentiment, for supplemental Gold, Bitcoin, and short-term trading analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimminhpro](https://clawhub.ai/user/kimminhpro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-tool developers use this skill to generate supplemental financial astrology analysis for Gold, Bitcoin, stocks, and short-term M15/H1 market review. It supports human analysis only and should not replace technical or fundamental analysis, financial advice, or automated trading controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Astrology-based market signals may be interpreted as financial advice or reliable price prediction.

Mitigation: Present outputs as supplemental analysis only; require human review and independent technical or fundamental analysis before trading decisions.

Risk: Automating trades from speculative signals could cause financial loss.

Mitigation: Do not connect outputs directly to trade execution; keep stop-loss, position sizing, and approval controls outside the skill.

Risk: Time-sensitive calculations can be misleading when timezone, date, latitude, or longitude are wrong.

Mitigation: Use explicit date, timezone, latitude, and longitude for any time-sensitive analysis and review the assumptions shown in the output.

Risk: Dependency changes in pyswisseph could alter astronomical calculations.

Mitigation: Install dependencies in an isolated environment and prefer a pinned, reviewed pyswisseph version.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kimminhpro/skills/financial-astrology)
- [README](artifact/README.md)
- [Skill Documentation](artifact/DOCUMENTATION.md)
- [Swiss Ephemeris](https://www.astro.com/swisseph)
- [pyswisseph](https://github.com/aloistr/pyswisseph)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or Markdown analysis, with optional JSON output from the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline execution; results depend on supplied date, timezone, latitude, longitude, and selected asset.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

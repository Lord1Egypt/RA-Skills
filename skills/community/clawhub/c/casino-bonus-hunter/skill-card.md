## Description:

Ranks a static set of online casino welcome, reload, and cashback bonuses by estimated expected value and reputation-adjusted score, then writes the results as JSON with a console table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this automaton to evaluate sample casino bonus data and generate a ranked shortlist for independent review. Results should not be treated as live offer scanning or financial, legal, or gambling advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ranking can be mistaken for current casino-offer intelligence even though the evaluated data is static and unverified.

Mitigation: Treat the output as a sample calculation and independently verify bonus terms, wagering rules, reputation, and availability before acting on any result.

Risk: The output can influence gambling or financial decisions in jurisdictions or situations where use may be inappropriate.

Mitigation: Use the results only for informational review, comply with applicable law, and do not treat the ranking as financial, legal, or gambling advice.

Risk: The managed schedule writes refreshed rankings to a configurable output path.

Mitigation: Keep the scheduled run and BONUS_OUTPUT_FILE destination under user control, and review the skill before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/casino-bonus-hunter)
- [Mibayy publisher profile](https://clawhub.ai/user/mibayy)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [JSON file plus console table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ranked bonus details to BONUS_OUTPUT_FILE, defaulting to /tmp/casino_bonuses.json; filters can be set with BONUS_MIN_REP, BONUS_MIN_EV, and BONUS_TOP_N.]

## Skill Version(s):

1.0.0 (source: evidence release, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

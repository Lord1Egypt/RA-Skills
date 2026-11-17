## Description:

Use when the user wants BaZi-based baby naming, asks you to calculate a child's chart from raw birth data, already has a detailed four-pillar chart and wants naming analysis, or wants to judge one or more existing names against a verified chart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billin9](https://clawhub.ai/user/billin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to collect birth and naming constraints, calculate or verify a BaZi chart, analyze favorable naming directions, and evaluate candidate Chinese names against the verified chart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process sensitive birth and family naming details.

Mitigation: Install and use only when users are comfortable sharing those details with the agent workflow; collect only the fields needed for chart verification and naming analysis.

Risk: The BaZi calculation script depends on lunar-python and the evidence notes dependency and localization caveats.

Mitigation: Run the script in a restricted environment and pin lunar-python to a reviewed exact version before relying on production results.

Risk: The artifact references an absolute local script path in examples, which may not resolve in another environment.

Mitigation: Fix or remap the script path to the installed skill artifact before using the calculation workflow.

Risk: Trend and popularity guidance can be incomplete when online research is unavailable.

Mitigation: Disclose when current trend sampling was not performed and treat trend observations as supplemental rather than deterministic.

## Reference(s):

- [Naming Principles](references/naming-principles.md)
- [Bazi Name Master on ClawHub](https://clawhub.ai/billin9/skills/bazi-name-master)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with structured analysis, scoring tables, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a supporting Python script that returns JSON-formatted BaZi calculation results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

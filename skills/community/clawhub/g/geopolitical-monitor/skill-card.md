## Description:

Monitors geopolitical news themes and generates stock-sector impact analysis with investment recommendation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrisingz-crypto](https://clawhub.ai/user/zrisingz-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can use this skill to review simulated geopolitical event monitoring, assess potential impacts on sectors such as energy, gold, defense, shipping, consumer, technology, and finance, and produce local report artifacts for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated sector analysis and investment recommendations may be based on simulated or incomplete news data.

Mitigation: Review the report against current trusted news and market sources before using it for investment or operational decisions.

Risk: The bundled script may need maintenance before execution because security guidance reports escaped comparison and arrow characters that can cause a Python syntax error.

Mitigation: Review and fix the script syntax in a controlled environment before deployment or scheduled use.

Risk: The skill writes local JSON reports to the user's home directory.

Mitigation: Run it only where local report creation under ~/shared_memory/geopolitical is acceptable and review generated files for sensitive content before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrisingz-crypto/skills/geopolitical-monitor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text plus saved JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ~/shared_memory/geopolitical and currently uses bundled simulated news unless extended with real RSS or news API sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

AION Skill Builder helps agents generate AION and ClawHub trading skill projects from natural language strategy descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-skill authors use this skill to scaffold AION-powered prediction-market trading skills, including metadata, ClawHub configuration, and Python trading logic that they can review, customize, test, and publish.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading skills may contain unreviewed model-generated Python that can later be run or scheduled.

Mitigation: Generate into an empty disposable directory, inspect generated skill.py and configuration before execution, and disable any generated schedule until reviewed.

Risk: Trading execution can require AION credentials and may optionally use a wallet private key.

Mitigation: Use test credentials when evaluating, avoid providing wallet private keys unless necessary, and keep generated skills in dry-run mode until audited.

Risk: The release security verdict is suspicious because packaging partly describes the skill as a trader while it acts as a generator.

Mitigation: Review generated output and advertised behavior before publishing or deploying derived skills.

## Reference(s):

- [AION Skill Builder on ClawHub](https://clawhub.ai/ssj124/skills/aion-skill-builder)
- [AION agents API credentials](https://www.aionmarket.com/agents)
- [AION building skills documentation](https://docs.aion.market/essentials/building-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration]

**Output Format:** [Markdown, JSON configuration, Python code, and shell commands written into a generated skill folder]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a complete skill folder; artifact documentation says generated trading logic should default to dry-run.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

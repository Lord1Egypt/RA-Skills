## Description:

Cyber I Ching Master provides Chinese I Ching divination, hexagram interpretation, and BaZi chart generation for reflective guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent4quant](https://clawhub.ai/user/agent4quant)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to generate I Ching readings, three-layer hexagram explanations, and BaZi charts in zh-CN. It is suited for reflective or cultural exploration, not for professional medical, legal, financial, or life-critical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat divination or BaZi outputs as professional advice.

Mitigation: Present outputs as reflective guidance and direct users to qualified professionals for medical, legal, financial, or similarly high-stakes decisions.

Risk: Birth details used for BaZi readings may be sensitive personal information.

Mitigation: Ask only for details needed for the requested chart and avoid retaining or sharing them outside the local interaction.

Risk: The hexagram data generation helper can attempt to overwrite a data file when imported or run.

Mitigation: Review scripts/data/generate_hexagrams.py before developer use and avoid importing it in normal agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agent4quant/skills/cyber-iching-master)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [SOUL.md](artifact/SOUL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [zh-CN text or Markdown, often with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local execution with no network or credential access reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

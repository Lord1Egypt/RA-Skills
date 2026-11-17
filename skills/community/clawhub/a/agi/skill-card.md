## Description:

Think like a human. Reason, plan, adapt, create, and know your limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill as a broad reasoning layer for agent interactions, adding structured planning, calibrated uncertainty, communication adaptation, and reflection habits across tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to influence future interactions broadly, especially if MEMORY.md integration is enabled.

Mitigation: Enable the MEMORY.md activation line only with explicit user consent, and remove that line if the reasoning layer should not activate automatically.

Risk: The skill stores interaction-derived notes, reflections, and knowledge-gap records under ~/agi/.

Mitigation: Review the files under ~/agi/ periodically and delete them if the stored style notes or reflections are no longer wanted.

Risk: A broad reasoning layer can affect tone, confidence calibration, and task planning across unrelated work.

Mitigation: Inspect memory.md, reflections.md, and limits.md for unwanted patterns, and pause or remove the skill if its behavior does not match the user's preferences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/agi)
- [Skill Homepage](https://clawic.com/skills/agi)
- [Setup](artifact/setup.md)
- [Reasoning Protocols](artifact/reasoning.md)
- [Memory Template](artifact/memory-template.md)
- [Common Blind Spots](artifact/blindspots.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain-text agent responses, with optional Markdown memory files and a MEMORY.md activation line when the user consents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can store interaction-derived notes under ~/agi/ and can add one activation line to the user's MEMORY.md only with explicit consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

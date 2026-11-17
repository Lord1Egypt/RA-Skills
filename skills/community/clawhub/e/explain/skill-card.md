## Description:

Learns how to explain things to your human. Adapts format, depth, and style by topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent produce human-facing explanations that adapt to observed preferences for format, depth, examples, jargon, pacing, and tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed explanation preferences may persist on the local machine in ~/explain/memory.md.

Mitigation: Review or delete ~/explain/memory.md before or after installation if preference history should not be retained.

## Reference(s):

- [Explain skill overview](artifact/SKILL.md)
- [Format Patterns](artifact/formats.md)
- [Depth Calibration](artifact/depth.md)
- [Analogies](artifact/analogies.md)
- [Domain-Specific Explanation Patterns](artifact/domains.md)
- [Explanation Dimensions](artifact/dimensions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses adapted to the user's explanation preferences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store confirmed explanation preferences locally in ~/explain/memory.md.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

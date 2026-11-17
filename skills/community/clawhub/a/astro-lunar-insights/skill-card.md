## Description:

Lunar phase analysis and Moon influence on a person using Swiss Ephemeris (pyswisseph), producing bilingual astrological analysis, structured lunar metrics, and rendered charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamicsalex](https://clawhub.ai/user/dynamicsalex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to calculate personal lunar astrology metrics from birth details and a target date, then generate text, JSON, or chart outputs for entertainment and educational interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies and runs bundled executable dependency files, including a Windows Swiss Ephemeris binary.

Mitigation: Run it only in an isolated Python environment and use the bundled native binary only when the publisher and package source are trusted.

Risk: The chart renderer may install Pillow automatically at runtime.

Mitigation: Preinstall a pinned Pillow version in the environment before running the skill.

Risk: Birth details can be written to temporary JSON files and generated chart files.

Mitigation: Avoid using sensitive personal data unless needed, restrict access to the workspace and temp directory, and remove generated files after use.

Risk: Generated charts include donation or promotional QR content by default.

Mitigation: Inspect generated images before sharing and override or remove the frame asset when promotional content is not appropriate.

Risk: Astrological output may be mistaken for decision-grade advice.

Mitigation: Present results as entertainment or educational interpretation and do not rely on them for medical, financial, or other high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dynamicsalex/skills/astro-lunar-insights)

## Skill Output:

**Output Type(s):** [Text, JSON, Image files, Guidance]

**Output Format:** [Plain text analysis, structured JSON lunar metrics, and PNG chart files with optional AI conclusion JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Russian and English output; chart renderer produces a 5760x2880 PNG.]

## Skill Version(s):

1.3.3 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

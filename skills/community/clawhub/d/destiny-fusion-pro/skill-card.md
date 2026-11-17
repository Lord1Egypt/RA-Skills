## Description:

Premium destiny consultation skill combining Ziwei Doushu and Bazi in one offline workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation builders use this skill to generate consultation-style Ziwei Doushu and Bazi reports from birth date, birth time, gender, and forecast-year inputs. It supports human-readable destiny analysis, structured JSON output, and optional chart image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local dependency execution may inherit risk from Python or JavaScript astrology and image-rendering packages.

Mitigation: Use a virtual environment and pin, review, and scan dependencies before installing iztro-py, cairosvg, pillow, lunar-python, or iztro.

Risk: Optional chart generation can write SVG or JPG files to local disk.

Mitigation: Run the skill in a controlled working directory and review chart output paths before sharing or publishing generated files.

Risk: Destiny or astrology-style analysis can be mistaken for professional advice.

Mitigation: Present results as interpretive guidance only and preserve the skill's stated boundary that it is not medical, legal, or investment advice.

## Reference(s):

- [Ziwei Doushu Methodology](references/ziwei-methodology.md)
- [Market Positioning](references/positioning.md)
- [ClawHub Skill Page](https://clawhub.ai/spyfree/skills/destiny-fusion-pro)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON consultation report, with optional SVG or JPG chart file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline workflow; chart rendering is optional and should not block text output.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

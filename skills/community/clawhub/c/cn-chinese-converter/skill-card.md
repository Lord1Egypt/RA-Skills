## Description:

Converts Chinese text between Simplified and Traditional variants, including Taiwan and Hong Kong forms, using local OpenCC-based processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to convert Chinese text between Simplified, Traditional, Taiwan, and Hong Kong variants for localization and regional content adaptation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires the external opencc-python-reimplemented dependency, and an unconstrained install can create supply-chain drift.

Mitigation: Install in a dedicated virtual environment and pin a reviewed dependency version before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-chinese-converter)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples; runtime script can emit plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes provided text locally and depends on opencc-python-reimplemented.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

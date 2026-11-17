## Description:

Helps home brewers calculate recipes for six coffee methods, diagnose taste defects, and compare logged brews to refine their settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home coffee brewers use this skill to calculate doses and water amounts, troubleshoot taste, and track which brew settings produce their preferred cups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brew settings and scores entered in log commands are saved in a local JSON file.

Mitigation: Use the documented --store option to choose where the log is kept and review that location before logging.

## Reference(s):

- [Coffee Brew Lab on ClawHub](https://clawhub.ai/voronindenis5/skills/coffee-brew-lab)
- [Brewing science reference](references/brew-science.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown and plain text; optional local JSON brew log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes brew quantities, method steps, taste-based adjustments, and comparisons of logged scores.]

## Skill Version(s):

1.0.1 (source: ClawHub release; bundled SKILL.md states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Astrological transit calculator with natal chart support. Daily transits, weekly forecasts, void-of-course Moon, aspects, stations, and ingresses. Uses Swiss Ephemeris.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mizukaizen](https://clawhub.ai/user/mizukaizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate local astrological transit context from natal chart data, including daily and weekly forecasts, Moon phase, void-of-course status, stations, and ingresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved natal chart JSON contains birth date, birth time, timezone, and location coordinates.

Mitigation: Store generated chart files in an appropriate local location and avoid sharing them unless intended.

Risk: The skill requires installing the `pyswisseph` Python package before use.

Mitigation: Install dependencies in a virtual environment and consider pinning the package version before deployment.

## Reference(s):

- [Astro Transits on ClawHub](https://clawhub.ai/mizukaizen/skills/astro-transits)
- [Homepage listed in skill metadata](https://github.com/mizukaizen/openclaw-skills-public)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples plus JSON and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts; generated natal chart files include birth date, time, timezone, and location coordinates.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

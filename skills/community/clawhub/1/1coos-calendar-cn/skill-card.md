## Description:

Provides local Chinese traditional calendar and almanac lookups for Gregorian or lunar dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1coos](https://clawhub.ai/user/1coos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese calendar, lunar date, almanac, solar term, festival, and auspicious-day questions from a date input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar and almanac results are generated from bundled data and library logic, so users may treat culturally specific or auspicious-day guidance as authoritative beyond its intended context.

Mitigation: Present results as calendar and almanac information and have users verify high-impact scheduling, legal, medical, financial, or religious decisions with appropriate sources.

Risk: The skill requires Bun and includes a large bundled JavaScript file with embedded calendar data tables.

Mitigation: Install only in environments where Bun is approved, and rely on the clean clawscan verdict plus normal review and scanning before deployment.

Risk: English language mode may still include some Chinese section labels.

Mitigation: Tell non-Chinese readers that output localization is partial and confirm important terms before acting on the result.

## Reference(s):

- [Module configuration reference](references/modules.md)
- [lunar-typescript](https://github.com/6tail/lunar-typescript)
- [ClawHub skill page](https://clawhub.ai/1coos/skills/1coos-calendar-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style formatted calendar report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output; requires Bun; optional local config can enable or disable output modules.]

## Skill Version(s):

1.0.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

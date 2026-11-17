## Description:

Chinese mainland calendar service that identifies statutory holidays, weekends, makeup workdays, and city-specific vacation periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manucode2000-max](https://clawhub.ai/user/manucode2000-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer China mainland holiday, workday, and school vacation calendar questions from dates, years, or supported city names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the unpinned third-party chinese-calendar Python package.

Mitigation: Install it in a low-privilege Python environment and pin or review the dependency before use.

Risk: Holiday and vacation logic is specific to mainland China and includes Chinese-language CLI output.

Mitigation: Use it for China-specific calendar questions and review outputs before applying them to other regions or user-facing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manucode2000-max/skills/china-holiday-calc)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text, JSON-like Python dictionaries, and Markdown with inline shell or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language date labels and CLI output; uses the chinese-calendar Python package.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

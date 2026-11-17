## Description:

Converts Chinese natural-language event descriptions into importable .ics calendar files for Google Calendar, Apple Calendar, and Outlook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to turn Chinese scheduling text into calendar events that can be imported into common calendar applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .ics files are written to the user's home directory.

Mitigation: Review the output path before importing or sharing generated calendar files.

Risk: Crafted event text could alter fields inside an imported calendar event because ICS values are not escaped.

Mitigation: Use trusted event text and inspect generated .ics files before importing until ICS escaping is fixed.

Risk: The artifact install command includes an unnecessary unpinned Python package.

Mitigation: Avoid running the install command unless the dependency is required and pin or review the package before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated .ics files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates calendar files in the user's home directory.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata; artifact body declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

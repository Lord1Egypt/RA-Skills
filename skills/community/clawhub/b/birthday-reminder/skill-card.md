## Description:

Birthday Reminder helps agents add, query, list, and remind users about birthdays using natural language while storing records locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manantra](https://clawhub.ai/user/manantra)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to remember birthdays, answer birthday and age questions, list upcoming birthdays, and produce reminder messages for stored contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores names and birth years locally, which can be personal information.

Mitigation: Use it only where local persistence of this information is acceptable, and review retention and access controls for the birthday data file before deployment.

Risk: The documentation describes birthdays.md storage while the scripts use birthdays.json, which can cause confusion about where records are retained.

Mitigation: Confirm and standardize the expected storage file before relying on reminders or auditing stored birthday records.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-style text and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on local birthday records and date calculations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Validate date strings and check formats. Support YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY. Pure Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to validate date strings locally and return parsed date details for supported formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous slash-form dates can be interpreted in multiple ways because the script accepts both day/month/year and month/day/year inputs.

Mitigation: Prefer YYYY-MM-DD inputs or review slash-form dates before relying on the result.

Risk: The skill documentation contains promotional links unrelated to local date validation.

Mitigation: Review linked pages separately before following them; they are not required for local execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and JSON command output from the validator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local validator emits JSON with validity, parsed format, date parts, and weekday when a date is valid.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Error Analysis helps learners analyze incorrect answers, identify related knowledge points, and generate similar practice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and educators use this skill to review wrong answers, categorize mistakes, locate weak knowledge areas, and create follow-up practice or review recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store study questions, wrong answers, and correct answers in local records.

Mitigation: Avoid entering sensitive personal information and periodically review or delete saved records such as artifact/data/errors.json.

Risk: The bundled sample data includes an existing mistake record.

Mitigation: Review bundled data before use and clear records that are not needed for the deployment.

Risk: The extra scripts/script.sh utility is not part of the documented error-analysis workflow and writes local logs or datastore entries.

Mitigation: Use the documented scripts/error.sh workflow unless the local logging behavior of scripts/script.sh has been reviewed and is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/error-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-style text with shell command examples and local JSON data records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save study mistake records locally in data/errors.json or the configured local data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

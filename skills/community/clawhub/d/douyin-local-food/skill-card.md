## Description:

Douyin Local Food is a restaurant operations helper for Douyin Local Life that supports store diagnosis, popular dish planning, group-buying package design, content operations, data analysis, and customer-service scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronnee520](https://clawhub.ai/user/aaronnee520)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant operators and marketing teams use this skill to draft Douyin Local Life plans for store launch diagnosis, dish promotion, group-buying offers, content calendars, performance review, and customer-service replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised data-analysis command may produce hard-coded metrics instead of analyzing the user's data file.

Mitigation: Use the analysis output only as a template unless the command is updated and reviewed to parse actual business data.

Risk: Generated report output paths could overwrite existing workspace files.

Mitigation: Run the tool in a controlled workspace and choose output paths that do not conflict with important files.

## Reference(s):

- [Douyin Local Food release page](https://clawhub.ai/aaronnee520/skills/douyin-local-food)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with example shell commands and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI writes JSON output files for generated reports and plans.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

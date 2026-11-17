## Description:

Orchestrates a full content workflow from planning through writing, design, publishing, and tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Content operators and agents use this skill to coordinate an end-to-end content pipeline, including SEO planning, draft writing, card news design, social publishing, and performance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline can automatically publish generated content to social accounts without review.

Mitigation: Use stage-by-stage mode, review generated content and destination accounts before publishing, and avoid --auto or --skip-review unless separate publishing safeguards are in place.

Risk: Stage outputs are chained through dated event files, so stale or unintended event data could influence later content or publishing steps.

Mitigation: Review the relevant event files before continuing to later stages, especially before design and publish steps.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and event-file conventions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates stage outputs through dated event files and may prepare social publishing steps for review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

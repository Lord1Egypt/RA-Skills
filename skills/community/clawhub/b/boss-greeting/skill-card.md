## Description:

This skill helps agents generate personalized BOSS Zhipin outreach messages, compare job descriptions against a user's profile, rank multiple roles, and handle screenshot-based job description extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagurananaga](https://clawhub.ai/user/kagurananaga)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and their agents use this skill to maintain a structured job-search profile, evaluate BOSS Zhipin job descriptions, and draft concise personalized greeting messages for selected roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a detailed job-search profile locally, which may include resume history, job preferences, salary expectations, and sensitive career context.

Mitigation: Confirm where the profile is stored and how to delete it before use, and avoid adding highly sensitive identifiers or confidential employer information.

Risk: The skill requests Bash access even though its normal workflow is profile management, job description analysis, and message drafting.

Mitigation: Prefer a version that removes shell access or review any shell activity before execution and keep file operations limited to the intended profile data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagurananaga/skills/boss-greeting)
- [Greeting examples](references/examples.md)
- [Profile template](references/profile-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Greeting drafts are intended to be 200-250 Chinese characters, with word counts included after generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

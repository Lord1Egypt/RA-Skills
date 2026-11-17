## Description:

Collect structured Indeed job-posting data from a known Indeed job URL. Do not use for company profiles or broad job discovery without an Indeed URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect structured job listing data from explicit Indeed job URLs through Dataify and retrieve the final JSON result when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Dataify API tokens and can accept a token on the command line.

Mitigation: Avoid passing tokens with --token; use a session-scoped environment variable or credential manager and never print token values.

Risk: The skill loads sibling dataify-task-operations code at runtime to monitor and download task results.

Mitigation: Install only after reviewing and trusting the sibling dataify-task-operations code that will run in the same environment.

Risk: Persistent shell-profile token setup may leave credentials stored longer than intended.

Mitigation: If a token was saved persistently, remove it from the shell profile, rotate the token, and prefer session-scoped setup for future use.

Risk: Using the skill for broad discovery or non-job URLs can produce unsuitable or costly collection tasks.

Mitigation: Use the skill only with explicit Indeed job URLs and confirm high-volume or ambiguous requests before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-indeed-job-listings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a summarized result for large payloads while preserving access to the raw JSON result.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

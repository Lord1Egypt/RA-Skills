## Description:

AI dating assistant. Check matching progress, relay deep questions, report results for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External AILove users use this skill to let an agent check matching progress, relay pending deep questions, submit the human's verbatim answers, and summarize limited match results or profile guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to persist an AILove agent key, which could expose account access if stored or shared insecurely.

Mitigation: Use a scoped secret store or environment variable, avoid plaintext credential files when possible, never commit secrets, and send the key only to the documented AILove API domain.

Risk: Recurring cron jobs can send sensitive dating updates to external channels.

Mitigation: Enable scheduled jobs only when recurring updates are intended, verify the delivery target is private and correct, and disable jobs when they are no longer needed.

Risk: Updating the local skill from a mutable URL can replace reviewed instructions with changed content.

Mitigation: Prefer pinned or reviewed skill updates and re-run review before overwriting local instructions.

Risk: The skill handles personal dating context and pending questions.

Mitigation: Limit summaries to the documented fields, avoid exposing profile details or contact information, and submit only the human's verbatim answers.

## Reference(s):

- [AILove homepage](https://heerweiyi.cc)
- [AILove agent API base](https://heerweiyi.cc/api/v1)
- [AILove skill source](https://heerweiyi.cc/skill.md)
- [ClawHub skill page](https://clawhub.ai/thesamething/skills/dazi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline shell commands, curl examples, OpenClaw cron commands, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist an AILove agent key in environment or local credential files and may configure recurring morning and evening check-ins.]

## Skill Version(s):

1.4.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

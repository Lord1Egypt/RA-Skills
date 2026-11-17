## Description:

AI-powered email triage that syncs with calendars and drafts responses for inbox management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Employees and developers use this skill to categorize inbox messages, identify urgent or action-required email, extract meeting details, and draft response suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email and calendar data may include sensitive personal or business content, and the remote OpenAI backend can receive email content for classification and drafting.

Mitigation: Use only with mailboxes where sending content to OpenAI is acceptable, or configure a local-only backend for sensitive email.

Risk: The MCP pipeline exposes an HTTP endpoint that can be reachable beyond the local machine if network binding is not restricted.

Mitigation: Bind the MCP server to localhost or add authentication before exposing it on a network.

Risk: Calendar creation and mailbox archiving can change user data if enabled without review.

Mitigation: Keep archiving disabled and review proposed calendar or mailbox changes before enabling automatic actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-email-triage)
- [Expanso pipeline schema](https://docs.expanso.io/schemas/pipeline.schema.json)
- [Expanso Cloud deployment pipeline](https://skills.expanso.io/email-triage/pipeline-cli.yaml)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [JSON object with triage summary, categorized emails, calendar events, draft responses, and processing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email categories, priorities, recommended actions, extracted calendar event details, and suggested response drafts.]

## Skill Version(s):

1.0.0 (source: skill.yaml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

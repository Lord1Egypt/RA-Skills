## Description:

CreBee helps an agent publish videos, image posts, and articles across multiple connected content-platform accounts through the user's local CreBee desktop client, with platform parameter preparation, user confirmation, scheduled publishing, and status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8spxd](https://clawhub.ai/user/n8spxd)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media operators use this skill to prepare, validate, confirm, publish, schedule, and track content across their connected CreBee platform accounts. It is intended for normal ClawHub release use where the user already controls the relevant CreBee account, platform accounts, and API-call budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause external publishing through the user's logged-in platform accounts.

Mitigation: Review the selected accounts, content, schedule, platform parameters, and publish plan before confirming any publish action.

Risk: Dynamic parameter queries and publishing consume CreBee API calls.

Mitigation: Check the estimated and actual CreBee call counts surfaced by the workflow, and confirm the plan only when the expected cost is acceptable.

Risk: Credential handling mistakes could expose account access or route requests outside the intended local client.

Mitigation: Use the local CreBee desktop client workflow, do not paste tokens into chat, and keep the service endpoint on localhost.

Risk: Platform validation, authorization, copyright, or upload failures may require user action and are not always safely retryable.

Mitigation: Follow the structured troubleshooting guidance, avoid blind retries, and require user reauthorization or clarification when the evidence indicates it is needed.

## Reference(s):

- [CreBee Publish Skill on ClawHub](https://clawhub.ai/n8spxd/skills/crebee-publish)
- [CreBee Website](https://www.crebee.cn)
- [Publishing Workflow Reference](references/publishing.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline CLI commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local CreBee desktop client, connected platform accounts, available CreBee API calls, and user confirmation before publish actions.]

## Skill Version(s):

1.9.13 (source: server release evidence and crebee-skill-version marker)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

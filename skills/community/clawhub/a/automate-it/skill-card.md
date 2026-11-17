## Description:

Create and manage Automate It content tasks and automations, prepare or delegate content, monitor human review and publishing, and manage related workspace resources within API-key scopes and role limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workingdevshero](https://clawhub.ai/user/workingdevshero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft or delegate social and other publishing content, manage review and publishing tasks, schedule recurring automations, and check task or publication status in an Automate It workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is a bearer credential for workspace operations, including publishing.

Mitigation: Store it as a secret, use the narrowest required scopes, and configure only a trusted HTTPS API endpoint.

Risk: Content may publish automatically if review safeguards are disabled.

Mitigation: Keep human review enabled unless automatic publishing is deliberately authorized.

Risk: Workspace deletions are permanent, and recurring automations continue until paused or changed.

Mitigation: Require explicit operator authorization for destructive actions, and pause or update an automation when the intent is to stop future runs.

## Reference(s):

- [Automate It agent documentation](https://automate.it.com/agents)
- [ClawHub release](https://clawhub.ai/workingdevshero/skills/automate-it)
- [Publisher profile](https://clawhub.ai/user/workingdevshero)

## Skill Output:

**Output Type(s):** [Text, Markdown, Status information, Published-content links]

**Output Format:** [Text and Markdown content, task status, and links; CLI results can be returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content may be prepared by the agent or delegated to the built-in worker; publication is subject to workspace permissions and review settings.]

## Skill Version(s):

0.5.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

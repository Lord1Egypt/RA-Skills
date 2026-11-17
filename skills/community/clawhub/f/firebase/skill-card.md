## Description:

Helps agents manage Firebase projects and web, Android, and iOS apps through a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to list and manage Firebase projects and apps, retrieve app configuration, and manage Google Analytics links. Optional hosted functions and triggers support user-requested automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing a connection grants Maton access to the selected Firebase account.

Mitigation: Confirm the intended account and authorization before connecting; use only the access needed for the task.

Risk: Writes, deletions, and hosted automations can change Firebase resources or run beyond a single request.

Mitigation: Confirm each write, deletion, function deployment, trigger, and persistent destination before execution.

Risk: Cross-app trigger examples could be mistaken for part of the Firebase workflow.

Mitigation: Use HubSpot, Gmail, Stripe, Slack, and other cross-app triggers only when separately requested.

## Reference(s):

- [Firebase skill release](https://clawhub.ai/byungkyu/skills/firebase)
- [Maton](https://maton.ai)
- [Firebase Management API overview](https://firebase.google.com/docs/projects/api/workflow_set-up-and-manage-project)
- [Firebase Management REST API reference](https://firebase.google.com/docs/reference/firebase-management/rest)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and authorization for the intended Firebase connection.]

## Skill Version(s):

1.2.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

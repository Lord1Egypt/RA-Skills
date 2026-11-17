## Description:

Get things done in the real world - pickups, deliveries, errands, and gifts handled by a human tasker in San Francisco.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjmaxwell4](https://clawhub.ai/user/jjmaxwell4)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Doorstep to request real-world pickups, deliveries, errands, purchases, and gifts performed by a human tasker. The skill is limited to tasks in San Francisco and supports quote review, approval, tracking, messaging, cancellation, receipts, and account setup.

### Deployment Geography for Use:

San Francisco, CA

## Known Risks and Mitigations:

Risk: The default npx bridge setup may execute an unpinned local npm package.

Mitigation: Prefer the HTTP/OAuth connection when supported, or pin and verify the npm bridge package before using npx.

Risk: Doorstep requests can include sensitive addresses, contact details, preferences, and notes shared with the service operator and human taskers.

Mitigation: Provide only the details needed for the task and avoid unnecessary sensitive information.

Risk: Real-world tasks can create charges or non-refundable work after approval.

Mitigation: Keep manual quote approval enabled unless the user sets an explicit budget limit, and present plan and pricing before calling approve_task.

Risk: The service only supports San Francisco tasks.

Mitigation: Decline or clearly caveat requests for locations outside San Francisco.

## Reference(s):

- [Doorstep website](https://trydoorstep.app)
- [Doorstep API keys](https://trydoorstep.app/dashboard/api-keys)
- [Doorstep ClawHub listing](https://clawhub.ai/jjmaxwell4/skills/doorstep)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task descriptions, quotes, status updates, tasker messages, receipts, account setup instructions, and MCP configuration.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

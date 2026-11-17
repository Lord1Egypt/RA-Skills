## Description:

Guides agents through Capgo CLI commands and routes requests to the appropriate Capgo workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riderx](https://clawhub.ai/user/riderx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find Capgo CLI commands for setup and diagnostics and to route OTA, native build, and organization requests to focused workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capgo tools can change or delete apps and other resources.

Mitigation: Review and explicitly confirm deletions, uploads, rollouts, native builds, webhooks, and push notification changes before execution.

Risk: Overprivileged credentials could expand the impact of tool actions.

Mitigation: Connect with the least-privileged account or API key needed for the task; use read-only access for reporting.

Risk: Using the latest CLI version can make runs less repeatable.

Mitigation: Pin a Capgo CLI version when supply-chain repeatability matters.

## Reference(s):

- [Capgo MCP documentation](https://capgo.app/docs/ai/mcp/)
- [Capgo](https://capgo.app)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes specialized requests to Capgo workflow skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

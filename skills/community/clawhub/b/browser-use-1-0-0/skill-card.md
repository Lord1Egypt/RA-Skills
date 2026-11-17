## Description:

Browser Use 1.0.0 helps agents create Browser Use cloud browser sessions, attach persisted profiles, and run autonomous browser tasks through the Browser Use API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makforce](https://clawhub.ai/user/makforce)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to configure Browser Use API credentials, create cloud browser sessions, persist browser profiles, connect those sessions to Clawdbot, and launch autonomous browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted browser profiles can carry authenticated sessions into a cloud browser.

Mitigation: Use dedicated, low-privilege profiles; avoid personal, banking, admin, email, and work sessions; delete profiles when no longer needed.

Risk: A Browser Use API key can create browser sessions and run tasks if exposed.

Mitigation: Store the API key only in the agent configuration, restrict access to that configuration, and rotate the key if exposure is suspected.

Risk: Autonomous tasks using an authenticated profile may act inside signed-in accounts.

Mitigation: Review tasks before execution, scope them to low-risk accounts, and stop browser sessions when the task is complete.

## Reference(s):

- [Browser Use documentation](https://docs.browser-use.com)
- [Browser Use Cloud API documentation](https://docs.cloud.browser-use.com)
- [ClawHub release page](https://clawhub.ai/makforce/skills/browser-use-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Browser Use API key and may use persisted browser profiles.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

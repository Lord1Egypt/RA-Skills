## Description:

This skill helps agents configure ClawHub CLI to use a domestic mirror for faster skill downloads, including persistent shell environment variables, temporary registry use, and verification commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger0808](https://clawhub.ai/user/roger0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers who use ClawHub in China or constrained network environments use this skill to route ClawHub downloads and API requests through a domestic mirror and verify connectivity before installs or updates.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can persistently route ClawHub registry and site traffic through a specific mirror.

Mitigation: Install only when that routing is intentional, and verify the configured CLAWHUB_REGISTRY and CLAWHUB_SITE values before relying on the setup.

Risk: The shipped script appends environment variables to shell startup files, which affects future terminal sessions.

Mitigation: Prefer a temporary export for evaluation, review the exact shell file changes, and keep an undo step for removing CLAWHUB_REGISTRY and CLAWHUB_SITE.

Risk: The artifact contains unrelated persistent agent and workspace task-record content.

Mitigation: Review and remove unrelated task-record material before deploying or adapting the skill.

## Reference(s):

- [ClawHub Mirror Verification](references/clawhub-mirror-verification.md)
- [ClawHub Skill Page](https://clawhub.ai/roger0808/skills/configure-clawhub-domestic-mirror)
- [Publisher Profile](https://clawhub.ai/user/roger0808)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and environment variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include persistent shell startup configuration and verification commands for ClawHub CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

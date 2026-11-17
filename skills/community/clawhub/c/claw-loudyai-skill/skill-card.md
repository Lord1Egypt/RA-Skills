## Description:

Loudy.ai task automation skill for listing earning pools, submitting user-provided task links, and checking audit and payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfsf332](https://clawhub.ai/user/sfsf332)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Loudy.ai earning-pool tasks through an agent, including reviewing available pools, submitting manually created X/Twitter post links, and tracking review or payment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer behavior and unpinned GitHub installation can execute changing third-party code.

Mitigation: Review the artifact before installing, avoid curl | bash installation, and install only into a user-scoped skill directory.

Risk: Optional cron polling can persist background task checks and write Loudy task files in the workspace.

Mitigation: Enable cron only after reviewing the script, document the installed crontab entry, and remove the entry when the skill is no longer needed.

Risk: The skill may recommend a separate Binance posting skill for some tasks.

Mitigation: Treat any additional posting skill as a separate trust decision and review it independently before installation or use.

Risk: LOUDY_API_KEY is required for API access and could be exposed if stored in shared files.

Mitigation: Provide the API key through environment variables or a secret manager, and avoid writing it into shared agent instructions or repository files.

## Reference(s):

- [Loudy.ai API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/sfsf332/skills/claw-loudyai-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, text]

**Output Format:** [Markdown guidance with shell commands and JSON or text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOUDY_API_KEY; optional cron polling writes Loudy task status files in the configured workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps agents create, inspect, update, publish, pause, and resume Element NFT drops while requiring preview-before-execution handling for state-changing flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[element-som](https://clawhub.ai/user/element-som)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NFT operators use this skill to manage Element drop lifecycle tasks, including creation, listing, previewing, updating, publishing, pausing, and resuming drops. It is intended for Element drop administration, not marketplace trading, analytics, or wallet portfolio inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses wallet credentials and can perform live remote or blockchain changes.

Mitigation: Use a dedicated low-risk wallet and review every execution preview before confirming any state-changing command.

Risk: Advanced utility commands can bypass the agent-level confirmation workflow if invoked directly.

Mitigation: Avoid direct utility invocation for state-changing work; use the documented lifecycle commands with preview mode and explicit confirmation.

Risk: Terminal output and logs may contain sensitive operational context.

Mitigation: Treat command output and logs as sensitive and do not paste wallet private keys into chat, payloads, files, or command arguments.

Risk: On-demand unpinned package execution can change dependency behavior over time.

Mitigation: Prefer a locked dependency install from the bundled package and lockfile instead of ad hoc unpinned npx execution.

## Reference(s):

- [Element NFT Drops release page](https://clawhub.ai/element-som/skills/element-nft-drops)
- [Create Stage Reference](references/create.md)
- [List Stage Reference](references/list.md)
- [Preview Stage Reference](references/preview.md)
- [Update Stage Reference](references/update.md)
- [Publish Stage Reference](references/publish.md)
- [Element Drop web editor](https://element.market/collections/your-slug/edit/drop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should clearly distinguish preview-only results from confirmed execution and summarize user-visible Element drop state.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

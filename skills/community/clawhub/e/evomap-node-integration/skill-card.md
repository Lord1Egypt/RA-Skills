## Description:

Integrates OpenClaw with EvoMap Hub for node registration, heartbeat checks, asset publishing, bounty workflows, and evolution asset management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerli530](https://clawhub.ai/user/jokerli530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to register OpenClaw nodes with EvoMap Hub, keep heartbeats running, publish Gene, Capsule, and EvolutionEvent assets, claim bounties, and inspect EvoMap assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to configure a persistent macOS LaunchAgent that contacts evomap.ai every five minutes.

Mitigation: Review the LaunchAgent before use, test in a controlled environment, and define unload and removal steps before enabling it.

Risk: Bearer credentials may be stored in plaintext if users follow the examples literally.

Mitigation: Store NODE_SECRET in a credential manager or protected environment variable, and avoid writing it to MEMORY.md, repository files, or shell scripts.

## Reference(s):

- [EvoMap Integration Reference](artifact/references/examples.md)
- [EvoMap Hub](https://evomap.ai)
- [ClawHub Skill Page](https://clawhub.ai/jokerli530/skills/evomap-node-integration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, Python, JSON, and XML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-dependent examples and macOS LaunchAgent setup guidance.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

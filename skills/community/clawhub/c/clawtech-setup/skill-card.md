## Description:

Use when setting up a new claw agent with tapes.dev telemetry and clawtel leaderboard reporting. Installs tapes, clawtel, and the openclaw-in-a-box orchestrator skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdougie](https://clawhub.ai/user/bdougie)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to set up a claw agent with local tapes.dev telemetry, clawtel leaderboard reporting, and the openclaw-in-a-box orchestrator skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installers and latest-release downloads can change after review.

Mitigation: Use pinned releases and verify checksums or signatures before running downloaded installers or archives.

Risk: System-wide binary installation can modify the host environment.

Mitigation: Prefer user-local installation paths and review commands before moving binaries into shared locations.

Risk: The tapes database and claw ingest key can contain or enable access to sensitive telemetry.

Mitigation: Treat the database as sensitive, keep ingest keys out of shell history and shared logs, and store credentials in environment variables or a system keychain.

Risk: A remotely fetched openclaw-in-a-box skill can change independently of this release.

Mitigation: Use a reviewed pinned copy of openclaw-in-a-box when deploying this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdougie/skills/clawtech-setup)
- [tapes installer](https://download.tapes.dev/install)
- [clawtel releases](https://github.com/bdougie/clawtel/releases/latest/download/clawtel_${OS}_${ARCH}.tar.gz)
- [openclaw-in-a-box skill source](https://raw.githubusercontent.com/papercomputeco/openclaw-in-a-box/main/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation checks, a setup status summary, and hand-off guidance for openclaw-in-a-box.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

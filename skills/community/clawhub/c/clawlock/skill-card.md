## Description:

ClawLock is a comprehensive security scanner, red-team testing, and hardening toolkit for Claw environments across Linux, macOS, Windows, and Android Termux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1at](https://clawhub.ai/user/g1at)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to run Claw environment security scans, audit skills before installation, check configuration drift, and guide hardening work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run a third-party CLI with broad local security-inspection authority.

Mitigation: Review the target path and requested scan scope before execution, and run scans only against systems and files the user controls.

Risk: Hardening workflows can modify agent configuration and local security settings.

Mitigation: Confirm user approval for changes, prefer documented rollback paths, and review generated diffs before treating hardening as applied.

Risk: The release supports mutable remote installs and self-updates from PyPI or GitHub.

Mitigation: Prefer pinned package versions and verify the installed binary before running scans or updates.

Risk: Optional red-team and LLM assessment features may contact external services or execute promptfoo through Node.js.

Mitigation: Use offline flags when needed and run optional red-team tests only against authorized targets.

Risk: Scan history can store device fingerprinting information.

Mitigation: Disable or clear local scan history if persistent device fingerprints are not acceptable.

## Reference(s):

- [ClawLock ClawHub release](https://clawhub.ai/g1at/skills/clawlock)
- [ClawLock metadata homepage](https://github.com/g1at/ClawLock)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON or HTML reports from the ClawLock CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local scan results, skipped online checks, and hardening actions depending on the requested feature.]

## Skill Version(s):

2.5.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

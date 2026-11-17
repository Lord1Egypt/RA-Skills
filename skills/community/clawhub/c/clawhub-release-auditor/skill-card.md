## Description:

Validate, package, and verify ClawHub skills before and after publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to preflight ClawHub skill releases, diagnose repeated publish failures, compare local and published versions, and verify post-publish state before relying on a release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local skill folders and run ClawHub or OpenClaw release commands.

Mitigation: Install and invoke it only for intended release-audit work, and review the target skill path and command output before acting.

Risk: Publishing changes public release state.

Mitigation: Require explicit user confirmation for the exact version, warnings, and publish command before publishing.

## Reference(s):

- [ClawHub Publisher Checklist](references/checklist.md)
- [ClawHub Publishing Research Notes](references/research-notes.md)
- [ClawHub Homepage](https://clawhub.ai)
- [Clawhub Release Auditor Skill Page](https://clawhub.ai/daowuu/skills/clawhub-release-auditor)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with command output summaries and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ClawHub and OpenClaw command-line tools for full release verification.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Cross-device sync for OpenClaw workspace skills, memory, and settings via GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imink](https://clawhub.ai/user/imink)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to keep workspace skills, memory, and selected configuration files synchronized across devices through a configured GitHub repository. It provides setup, pull, push, status, reset, and session lifecycle sync workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move sensitive OpenClaw workspace data, including memory and settings, to and from GitHub.

Mitigation: Use a private, least-privilege repository, review generated sync mappings before enabling auto-sync, and avoid syncing secrets or private memory.

Risk: The artifact relies on mutable package execution for the any-sync CLI.

Mitigation: Prefer a pinned and reviewed version of the any-sync CLI before running sync commands in sensitive environments.

Risk: Automatic pull and push hooks can change workspace files at session start or session end with limited review.

Mitigation: Disable autoSync until the repository, branch, mappings, and expected file changes have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imink/skills/any-sync)
- [Publisher profile](https://clawhub.ai/user/imink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Any Sync configuration and lock files and may synchronize selected OpenClaw workspace files with the configured GitHub repository.]

## Skill Version(s):

0.2.10 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

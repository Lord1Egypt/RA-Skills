## Description:

Autonomously discovers, ranks, and installs high-value ClawHub skills from unresolved user problems, profile signals, and capability gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to find, rank, preview, and optionally install ClawHub skills that address unresolved tasks or recurring capability gaps. It is suited to controlled skill-discovery workflows where recommendations and installation outcomes are reviewed before adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads prior chats, task memory, user profile data, personality state, and installed-skill cache data to infer unresolved needs.

Mitigation: Run it only in a controlled workspace after reviewing what local memory files are available, and prefer targeted queries or dry-run mode when sensitive chat history may be present.

Risk: Live mode can clone or scaffold new skills into the local skills directory and execute a downloaded index.js self-test.

Mitigation: Avoid --auto and scheduled runs until reviewed; use --dry-run first, keep --max-install low, inspect each repository and destination path manually, and do not execute downloaded skill code without separate approval.

Risk: Recommendation reports may be sent through an external reporting wrapper and could include selected problem summaries or skill choices.

Mitigation: Set SKILL_HUNTER_NO_REPORT=1 for local tests or sensitive workspaces, and review any outbound report payload before enabling reporting.

## Reference(s):

- [Auto Skill Hunter - ClawHub](https://clawhub.ai/wanng-ide/skills/auto-skill-hunter)
- [Memory Mesh Core - ClawHub](https://clawhub.ai/wanng-ide/memory-mesh-core)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with installation metadata and generated skill files when live installation is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run preview, configurable per-run install limits, and disabled outbound reporting with SKILL_HUNTER_NO_REPORT=1.]

## Skill Version(s):

1.0.3 (source: evidence.release.version and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

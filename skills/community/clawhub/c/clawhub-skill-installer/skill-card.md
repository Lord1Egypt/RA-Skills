## Description:

ClawHub Skill Installer helps agents search ClawHub and install one or more skills from downloadable packages with retry behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to search ClawHub and install single or multiple skills into an OpenClaw skills directory while managing retries and batch delays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can change the active OpenClaw skills directory and overwrite existing skills.

Mitigation: Review the target skills directory before use, keep backups of important skills, and avoid elevated privileges.

Risk: The installer can download and install code from remote archives that are not cryptographically verified.

Mitigation: Prefer pinned sources with verified package identity and hashes, and install only trusted skills.

Risk: Fallback paths may run unpinned external commands or install unverified GitHub search results.

Mitigation: Inspect proposed commands before execution and avoid relying on fallback installation for sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/skills/clawhub-skill-installer)
- [OpenClaw](https://openclaw.ai)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented instructions with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install, remove, or overwrite local skill files when its commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

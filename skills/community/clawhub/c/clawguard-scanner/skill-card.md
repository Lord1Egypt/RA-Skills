## Description:

ClawGuard Scanner helps agents scan OpenClaw skills for prompt injection, data exfiltration, permission overreach, suspicious URLs, dangerous commands, and metadata mismatches before installation or audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frrrrrrrrank](https://clawhub.ai/user/frrrrrrrrank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skill directories before installation or during audits, then interpret findings and decide whether installation should proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned npm package.

Mitigation: Use a pinned, verified ClawGuard package version and run it in a sandbox with read-only access to the target skill directory.

Risk: The fallback global install path can persist tooling on the host.

Mitigation: Avoid global installation unless the package source is trusted and the user accepts persistent host changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frrrrrrrrank/skills/clawguard-scanner)
- [Declared project homepage](https://github.com/Frrrrrrrrank/clawguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke npx to run ClawGuard against a target skill directory.]

## Skill Version(s):

0.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

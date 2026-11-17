## Description:

ECC essentials bundle - install 23 core skills (agentic-engineering, security-review, deployment-patterns, docker-patterns, git-workflow, search-first, safety-guard) in one shot. Use when user asks to install ECC essentials, bootstrap OpenClaw with extended capabilities, or set up a full ECC workflow bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18816478335q-pixel](https://clawhub.ai/user/18816478335q-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install a curated bundle of 23 ECC skills for agentic engineering, security review, deployment workflows, Git practices, search-first development, and tool-enhancement workflows. The bundled installer can preview, install, overwrite with backup, or uninstall the included skills in an agents skills directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and bundled skills can persistently change local agent behavior by writing skill files into an agents skills directory.

Mitigation: Review the bundle before installing, run the installer with --dry-run first, and choose an explicit --target when validating the destination.

Risk: --force can replace existing skills, and --uninstall removes skill directories matching the bundled skill names.

Mitigation: Avoid --force unless replacement is intended, keep backups enabled for overwrites, and confirm target directories do not contain custom files before uninstalling.

Risk: Some bundled workflows involve autonomous loops, model routing, GitHub access, memory indexes, or npm/npx tools that can affect cost, data exposure, and repository scope.

Mitigation: Set explicit cost, data, and repository boundaries before use, and pin npm/npx tools before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18816478335q-pixel/skills/ecc-bundle-2026-07-08)
- [ClawHub publisher profile](https://clawhub.ai/user/18816478335q-pixel)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [AgentShield package](https://www.npmjs.com/package/ecc-agentshield)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files with Python installer terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; installer defaults to ~/.agents/skills and supports --target, --dry-run, --force, --backup, --no-backup, and --uninstall.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

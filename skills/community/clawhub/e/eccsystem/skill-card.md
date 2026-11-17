## Description:

ECCSystem installs a bundled set of 23 ECC skills for agentic engineering, security review, deployment, Docker, Git workflow, search-first, safety, and related engineering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18816478335q-pixel](https://clawhub.ai/user/18816478335q-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ECCSystem to bootstrap an OpenClaw or local agent-skills environment with 23 bundled ECC skills covering planning, security, deployment, Docker, Git workflow, research, prompt optimization, and safety practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes local agent skill directories and can overwrite same-named skills when force mode is used.

Mitigation: Review the bundled skill list, run with dry-run first, use an explicit test target when evaluating, and use force mode only when replacement is intended.

Risk: Uninstall mode can remove whole same-named skill directories, including extra files the bundle may not own.

Mitigation: Inspect or back up target skill directories before uninstalling and prefer manual removal when directories contain local changes.

Risk: Bundled security-scan guidance can lead agents to run npm or npx tooling.

Mitigation: Prefer pinned package versions and review generated commands before execution.

## Reference(s):

- [ECCSystem ClawHub skill page](https://clawhub.ai/18816478335q-pixel/skills/eccsystem)
- [Publisher profile](https://clawhub.ai/user/18816478335q-pixel)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python installer actions that create local SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; installer supports dry-run, custom target, force, backup/no-backup, and uninstall modes.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Resolve a dependency or version conflict (npm, pip, yarn, pnpm, Maven, Go modules) step by step. Use when an install fails with peer-dependency or version-conflict errors, packages won't co-exist, or a lockfile is fighting you. Produces the conflict explained, the resolution options ranked by safety, exact commands, and how to keep it from recurring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose package-manager dependency conflicts and choose a ranked resolution path with commands, manifest edits, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested package-manager commands or manifest edits can change dependency resolution, especially last-resort force-install options.

Mitigation: Review proposed commands and edits before applying them; treat force-install options as last-resort workarounds and verify with a clean install and build.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/dependency-conflict-resolver)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/dependency-conflict-resolver.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with plain-language analysis and inline commands or snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked safety trade-offs, recommended fixes, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

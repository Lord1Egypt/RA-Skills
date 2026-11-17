## Description:

Systematic debugging and problem-solving methodology for unexpected errors, service failures, regression bugs, deployment issues, and failed fix attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and coding agents use this skill to follow a root-cause debugging process before changing code, restarting services, or deploying fixes. It helps avoid patch-chaining, wrong-environment restarts, and temporary workarounds that do not address the underlying failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for server deployment, backups, pushes, and restarts that could affect production systems if applied without approval.

Mitigation: Keep normal approval boundaries for real production changes, backups, pushes, and restarts.

Risk: Debugging guidance may lead an agent to propose code or operational changes that are incorrect for the actual environment.

Mitigation: Require root-cause confirmation, one-change-at-a-time testing, syntax checks, health checks, and rollback readiness before deployment.

## Reference(s):

- [Debug Methodology ClawHub Skill Page](https://clawhub.ai/abczsl520/skills/debug-methodology)
- [OpenClaw Agent Skill Project](https://github.com/openclaw/openclaw)
- [bug-audit](https://github.com/abczsl520/bug-audit-skill)
- [codex-review](https://github.com/abczsl520/codex-review)
- [nodejs-project-arch](https://github.com/abczsl520/nodejs-project-arch)
- [game-quality-gates](https://github.com/abczsl520/game-quality-gates)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with checklists, decision trees, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces process guidance for debugging and deployment verification; it does not execute commands by itself.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

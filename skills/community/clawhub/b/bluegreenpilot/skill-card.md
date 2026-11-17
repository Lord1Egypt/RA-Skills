## Description:

Guide safe blue-green deployments with persistent repo config, environment state, health checks, explicit switch confirmation, and rollback discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thiagocaltoe](https://clawhub.ai/user/thiagocaltoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to configure, plan, verify, switch, promote, and roll back blue-green deployment workflows. It focuses on preserving deployment state, separating environments from slots, checking health and rollback paths, and requiring explicit confirmation before production traffic changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production deployment, rollback, or traffic-switch guidance could affect live service availability if acted on without review.

Mitigation: Require a clear human approval before any deploy, rollback, or production traffic switch, and review the generated plan before execution.

Risk: Incorrect or stale environment state could lead the agent to target the wrong blue-green slot.

Mitigation: Read the configured state source before planning, verify active and inactive slots, and stop when the state cannot be retrieved or trusted.

Risk: Secrets or sensitive deployment values could be placed in generated configuration by mistake.

Mitigation: Keep secrets in a dedicated secret store or environment variables, and review generated .bluegreenpilot files before committing them.

Risk: Database changes during deployment may create rollback risk when snapshot or migration policy is unknown.

Mitigation: Block production deployment planning until database policy, snapshot handling, and rollback procedure are known.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/ThiagoCAltoe/bluegreenpilot/tree/main/skills/bluegreenpilot)
- [BlueGreenPilot source repository](https://github.com/ThiagoCAltoe/bluegreenpilot)
- [ClawHub skill page](https://clawhub.ai/thiagocaltoe/skills/bluegreenpilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured plans, inline commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .bluegreenpilot configuration, state, and history files when the user approves state-changing work.]

## Skill Version(s):

2026.6.6 (source: server release metadata; artifact frontmatter reports 2026.6.4 and release changelog says this version is identical to 2026.6.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates Git project deployment by pulling code, building Node.js, Java, or Vue/Java projects, and deploying to Linux servers over SSH with backup, restart, rollback, and health-check steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjm1226](https://clawhub.ai/user/zjm1226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate deployment of Git-based Node.js, Java, or Vue/Java applications to Linux servers after code changes. It supports build, SSH transfer or server-side build, backup, service restart, health checks, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports embedded credentials and server connection details.

Mitigation: Rotate exposed Git and SSH or root passwords, remove real credentials from the package and history, and store secrets outside the skill configuration.

Risk: The security evidence reports root-level deployment scripts and elevated server actions.

Mitigation: Use a non-root deploy account with least-privilege permissions and require explicit approval before deploy, rollback, or environment installation.

Risk: The security guidance calls for verified host keys and safer Git transport.

Mitigation: Require verified SSH host keys and use HTTPS or SSH Git transport instead of embedding credentials in HTTP clone URLs.

Risk: Deployment and rollback behavior can delete or overwrite configured paths.

Mitigation: Validate deploy paths, backup paths, branch names, and rollback targets before execution, and confirm backups exist before destructive changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjm1226/skills/auto-deploy)
- [README.md](artifact/README.md)
- [DEPLOY_CONFIG.md](artifact/DEPLOY_CONFIG.md)
- [SSH_SETUP.md](artifact/SSH_SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment, rollback, SSH setup, connection testing, and server environment installation command sequences.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

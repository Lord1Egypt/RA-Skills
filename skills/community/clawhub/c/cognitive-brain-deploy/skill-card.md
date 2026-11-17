## Description:

Automates setup guidance for OpenClaw Cognitive Brain by configuring PostgreSQL with pgvector, Redis, Node.js, scheduled jobs, and OpenClaw hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and verify an OpenClaw semantic memory system on Ubuntu or Debian hosts. It helps install required services, create the cognitive_brain database schema, configure the Cognitive Brain skill, add cron tasks, and enable the OpenClaw recall hook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment flow makes privileged and persistent system changes, including package installation, service enablement, cron jobs, and OpenClaw hook setup.

Mitigation: Review the deployment script first and run it only on a non-sensitive test machine or container unless those host changes are acceptable.

Risk: The deployment materials use a plaintext default PostgreSQL password.

Mitigation: Replace the default password before use and update configuration with environment-appropriate credential handling.

Risk: The installation guidance includes pipe-to-sudo-bash setup and an unresolved repository placeholder for the Cognitive Brain skill.

Mitigation: Avoid pipe-to-sudo-bash installation where possible, and pin and verify the Cognitive Brain repository before installing dependencies.

Risk: Troubleshooting guidance includes destructive database recovery steps.

Mitigation: Back up memory data and review the effect of table recreation before following destructive troubleshooting steps.

## Reference(s):

- [Cognitive Brain Deploy on ClawHub](https://clawhub.ai/hongjiahao371-pixel/skills/cognitive-brain-deploy)
- [Cognitive Brain deployment guide](references/deploy-guide.md)
- [Cognitive Brain troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, SQL, cron, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment verification and troubleshooting guidance for local OpenClaw environments.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

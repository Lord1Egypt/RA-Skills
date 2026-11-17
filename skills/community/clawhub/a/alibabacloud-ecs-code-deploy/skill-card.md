## Description:

Deploys application and AI agent projects to Alibaba Cloud ECS with aliyun appmanager, including environment checks, pricing, initialization, deployment, verification, and retry guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy local projects or cloned repositories as Alibaba Cloud ECS applications or AI agents. It guides the agent through CLI checks, credential setup, configuration generation, cost confirmation, deployment, verification, and operational follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can deploy projects to Alibaba Cloud ECS and create or modify paid cloud resources.

Mitigation: Require explicit user approval before deployment, price acceptance, existing-ECS use, group overwrite, or resource deletion.

Risk: Cloud credentials and model API keys could be exposed if users paste secrets into chat or command arguments.

Mitigation: Use OAuth, RAM roles, environment variables, or a secrets manager, and keep AccessKeys and model API keys out of chat and command examples.

Risk: CLI installation, appmanager environment repair, Docker configuration, and root-runtime actions can change local or remote system state.

Mitigation: Ask for approval before upgrades, virtual environment deletion, Docker or system configuration changes, and destructive .appmanager operations.

## Reference(s):

- [Deploy Output & Management Reference](references/deploy-output-and-management.md)
- [Init & Credentials Reference](references/init-and-credentials.md)
- [RAM Policies Reference](references/ram-policies.md)
- [Script Templates & Language Reference](references/script-templates.md)
- [Skill Directory Resolution Reference](references/skill-dir-resolution.md)
- [Deployment Failure Lessons](references/lessons-learned.md)
- [Step-by-Step Flask Deployment Tutorial](references/tutorial-flask-app.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands and YAML or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify .appmanager/config.yaml and deployment start/stop scripts during use.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

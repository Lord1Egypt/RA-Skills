## Description:

Guides agents through guarded creation of Ark inference Endpoints, including live model selection, confirmation for billable actions, and post-creation examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select a current model and create a guarded Ark inference Endpoint, with explicit confirmation before billable deployment. It also guides agents to the appropriate workflow for automation, existing Endpoint management, and unsupported speech deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint creation and model activation can create billable resources, and scanner coverage was incomplete because one referenced path could not be resolved.

Mitigation: Review the skill and target model, confirm the final creation parameters before deployment, and hand off model activation to a human in non-interactive environments.

## Reference(s):

- [arkcli-deploy reference](artifact/references/arkcli-deploy.md)
- [arkcli-deploy evaluation cases](artifact/references/evals.md)
- [ClawHub skill page](https://clawhub.ai/jasonstarlight/skills/arkcli-deploy)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint creation can incur charges; example files are generated on a best-effort basis after successful creation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

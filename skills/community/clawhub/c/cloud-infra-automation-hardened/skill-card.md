## Description:

Automate cloud infrastructure provisioning and management via IaC tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to provision, manage, and review multi-cloud infrastructure with Terraform, Ansible, CloudFormation, and cloud provider CLIs. It is intended for real cloud infrastructure work where plans, target scope, and destructive operations need careful confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Infrastructure changes can destroy or replace cloud resources if a plan is skipped or destructive changes are buried in output.

Mitigation: Require a plan or dry run before apply, explicitly summarize resources to be destroyed or replaced, and wait for user confirmation before proceeding.

Risk: The agent could affect the wrong cloud account, project, subscription, or environment.

Mitigation: Verify the exact account, project, subscription, credentials, and environment name before cross-account or high-impact cloud actions.

Risk: Terraform state, cloud CLI output, and resource metadata can contain secrets or sensitive infrastructure details.

Mitigation: Do not send raw state or cloud metadata to external endpoints; share only sanitized summaries when explicitly requested.

Risk: Vague or stale approval can be mistaken for consent to run destructive commands.

Mitigation: Require fresh explicit confirmation naming the target environment before destroy, force-apply, delete-stack, or similar destructive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/cloud-infra-automation-hardened)
- [Safety evaluation](artifact/SAFETY.md)
- [Faberlens cloud infrastructure guardrails](https://faberlens.ai/explore/cloud-infra-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IaC plans, command recommendations, cloud scope checks, and confirmation prompts before high-impact actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

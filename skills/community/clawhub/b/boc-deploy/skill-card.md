## Description:

Automates BOC container platform deployment by generating deployment configuration, running bocctl install commands, monitoring progress, and validating node and pod status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongruiji](https://clawhub.ai/user/hongruiji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to deploy a BOC container platform from planned node, network, Kubernetes, and credential inputs. It helps generate config.yaml, launch the bocctl installation, monitor deployment logs, and check Kubernetes readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root SSH passwords and generated deployment configuration may expose reusable infrastructure credentials.

Mitigation: Use a dedicated least-privilege deployment account where supported, avoid reusable root passwords, protect generated config files with mode 600, keep credentials out of logs and support bundles, and rotate any exposed credentials.

Risk: The skill launches long-running infrastructure deployment changes that may be difficult to interrupt or roll back.

Mitigation: Review the generated configuration before execution, confirm rollback or cancellation steps, monitor the background install, and remove local and remote configuration copies after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongruiji/skills/boc-deploy)
- [Publisher profile](https://clawhub.ai/user/hongruiji)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with configuration details, shell commands, deployment status, log excerpts, and validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment guidance and status summaries for long-running infrastructure changes.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

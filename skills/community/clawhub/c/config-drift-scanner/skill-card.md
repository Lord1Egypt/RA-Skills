## Description:

Detect configuration drift across environments (dev, staging, production). Compare config files, environment variables, feature flags, and secrets across deployments to find dangerous inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and platform teams use this skill to compare configuration files, environment variables, feature flags, secrets, and deployment settings across development, staging, and production environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration comparison examples can expose secrets or infrastructure values in logs, temporary files, CI output, or agent responses.

Mitigation: Run only in controlled environments; compare redacted values or key names when possible; avoid raw production secrets; scrub temporary files and reports before sharing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, Python, and report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce drift findings, config parity checklists, CI snippets, secret-rotation review guidance, and remediation recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyzes codebase-auditor file inventories and generates optimized deployment packaging plans for critical environment, configuration, CI/CD, credential, and database files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to convert a codebase auditor's critical_files inventory into a JSON deployment packaging plan for environment, configuration, CI/CD, credential, and database configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated packaging plan can include raw secrets such as private keys, service-account credentials, and .env files in deployment artifacts.

Mitigation: Review and change the workflow before use so raw secrets are excluded by default and supplied through a secret manager or runtime injection.

## Reference(s):


## Skill Output:

**Output Type(s):** [Configuration, JSON, Shell commands, Guidance]

**Output Format:** [JSON file plus concise console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads a JSON inventory and writes packaging_plan.json under the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

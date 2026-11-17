## Description:

Manage environment promotions from dev to staging to production by comparing configurations, detecting drift, generating promotion plans, validating prerequisites, and preparing rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and release managers use this skill to compare environment configuration, detect drift, build promotion plans, validate readiness, and prepare rollback steps before promoting changes across environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The compare workflow can expose secrets from .env files.

Mitigation: Review before installing and avoid running the compare command on production .env files until redaction is fixed.

Risk: Unsafe command patterns and untrusted file paths may create installation or execution risk.

Mitigation: Use only trusted local paths and manually review commands before execution.

Risk: Validation may contact endpoints discovered in configuration files.

Mitigation: Require explicit approval before any validation command contacts endpoints found in config files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text reports, inline shell commands, and optional JSON-shaped examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces environment comparison reports, drift summaries, promotion plans, validation checks, history summaries, and environment matrices; it does not execute deployments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

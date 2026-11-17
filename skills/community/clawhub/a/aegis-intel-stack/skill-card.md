## Description:

Aegis Intel Stack provides pre- and post-execution utility micro-skills for EVM gas snapshots, transaction explanation, intel manifests, and delta update triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kankinku](https://clawhub.ai/user/kankinku)

### License/Terms of Use:


## Use Case:

Developers and agents can use this skill bundle to run local utility calls for EVM gas and transaction workflows, including health checks, gas snapshots, transaction explanation, manifest generation, and delta update triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install dependencies and run package scripts in a referenced aegis-suite project that is not included in the artifact.

Mitigation: Inspect the trusted project source and package scripts before running them, use a disposable local environment, and avoid placing real secrets in the copied .env unless the underlying project is trusted.

Risk: Gas and transaction guidance can become inaccurate when network conditions or transaction context change.

Mitigation: Treat outputs as advisory and verify current chain state, gas quotes, and transaction details before taking action.

## Reference(s):

- [Aegis Intel Stack on ClawHub](https://clawhub.ai/kankinku/skills/aegis-intel-stack)
- [Publisher profile: kankinku](https://clawhub.ai/user/kankinku)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local utility-server workflow with API call examples and launch automation outputs.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

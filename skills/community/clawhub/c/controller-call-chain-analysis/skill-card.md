## Description:

Analyzes Java microservice Controller call chains through Service, Mapper, and Repository layers, extracts SQL statements, and writes structured JSON for documentation, code audit, or architecture review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[14686039](https://clawhub.ai/user/14686039)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a Java Spring microservice Controller and understand the downstream Service, Mapper, Repository, and SQL behavior behind each API method.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Java project source files to build the call-chain analysis.

Mitigation: Run it only on repositories whose source files the agent is permitted to inspect.

Risk: The skill writes generated JSON under the configured output path, which may be committed if placed inside the repository.

Mitigation: Choose the output path deliberately and review generated files before committing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/14686039/skills/controller-call-chain-analysis)
- [Publisher Profile](https://clawhub.ai/user/14686039)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON file with agent guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local JSON analysis file under the configured output path, defaulting to docs/api_analysis/.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Operate Blocknative gas intelligence APIs through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover supported chains and read Blocknative gas price, base fee, blob fee, and pending gas distribution data through UXC. It supports authenticated, read-only gas intelligence workflows and excludes transaction submission, write operations, and mempool event streaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some Blocknative gas endpoints require API-key authentication, and reused or overly broad secrets could expose unrelated access.

Mitigation: Use a Blocknative-specific API key through the documented Authorization header credential binding and review or remove the UXC binding when access is no longer needed.

Risk: The linked CLI setup references a remote OpenAPI schema URL that can change over time.

Mitigation: Use a pinned or packaged schema for stable automation and review schema changes before relying on newly exposed operations.

Risk: Gas data freshness and endpoint availability can vary by plan and endpoint.

Mitigation: Poll conservatively, keep confidence levels narrow, and inspect the UXC JSON envelope fields such as ok, data, and error before acting on results.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/blocknative-gas.openapi.json)
- [Blocknative Gas Price API docs](https://docs.blocknative.com/gas-prediction/gas-platform)
- [Blocknative Base Fee API docs](https://docs.blocknative.com/gas-prediction/prediction-api-base-fee-and-blob-fee)
- [Blocknative Gas Distribution API docs](https://docs.blocknative.com/gas-prediction/gas-distribution-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON-oriented API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workflows using the UXC JSON output envelope; operations may require a Blocknative API key.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

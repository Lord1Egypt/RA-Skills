## Description: <br>
Operate Blocknative gas intelligence APIs through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure authenticated, read-only Blocknative gas intelligence calls and inspect supported chains, gas price estimates, base fee and blob fee predictions, and pending gas distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Blocknative API key is required for the full v1 gas API surface. <br>
Mitigation: Configure the key through UXC using the BLOCKNATIVE_API_KEY environment variable and bind it only to api.blocknative.com. <br>
Risk: Using an unpinned remote OpenAPI schema can reduce reproducibility if the schema changes. <br>
Mitigation: Use the bundled schema or a pinned schema URL when repeatable behavior matters. <br>
Risk: Polling gas endpoints too frequently can create unstable or plan-inappropriate automation. <br>
Mitigation: Start around one request every 5 to 10 seconds and only reduce the interval when the plan and workflow require fresher data. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/blocknative-gas.openapi.json) <br>
- [Blocknative Gas Price API Docs](https://docs.blocknative.com/gas-prediction/gas-platform) <br>
- [Blocknative Base Fee and Blob Fee API Docs](https://docs.blocknative.com/gas-prediction/prediction-api-base-fee-and-blob-fee) <br>
- [Blocknative Gas Distribution API Docs](https://docs.blocknative.com/gas-prediction/gas-distribution-api) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/blocknative-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API guidance; automation should parse JSON response envelopes and avoid transaction submission claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

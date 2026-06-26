## Description: <br>
Operate DefiLlama Pro analytics APIs through UXC with a curated OpenAPI schema, path-templated API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to configure UXC access to DefiLlama Pro and run read-only analytics queries for protocol TVL, chain metrics, current prices, yield pools, yield history, and stablecoin dominance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The DefiLlama Pro API key is included in the request path and may appear in raw commands or daemon logs. <br>
Mitigation: Store the key through UXC secret-backed credentials, sanitize logs before sharing, and rotate or delete exposed logs after debugging. <br>
Risk: The curated schema exposes only a read-only subset of the DefiLlama Pro API surface. <br>
Mitigation: Keep use to the documented analytics reads and inspect operation help before extending or binding credentials to a different path shape. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/defillama-pro.openapi.json) <br>
- [DefiLlama API Docs](https://defillama.com/docs/api) <br>
- [DefiLlama Pro Docs](https://defillama.com/pro-api/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/defillama-pro-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only UXC command guidance and expects JSON API responses from DefiLlama Pro.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

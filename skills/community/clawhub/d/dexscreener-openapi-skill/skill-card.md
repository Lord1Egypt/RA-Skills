## Description: <br>
Operate DexScreener public market data APIs through UXC with a curated OpenAPI schema, no-auth setup, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect DexScreener public market data, including token profiles, boosts, pair search, pair lookup, and token market rows, through read-only OpenAPI-backed CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the local uxc tool and an OpenAPI schema source to issue DexScreener requests. <br>
Mitigation: Use a trusted uxc installation and prefer the bundled schema or a reviewed, pinned schema URL for stricter reproducibility. <br>
Risk: DexScreener market data can be noisy for long-tail tokens and should not be treated as trading execution or investment advice. <br>
Mitigation: Use results as market-observation data, verify important findings against other sources, and keep workflows read-only. <br>
Risk: Endpoint-specific rate limits can affect polling and broad discovery workflows. <br>
Mitigation: Start with narrow lookups, cache repeated reads, and poll discovery feeds conservatively. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/dexscreener-public.openapi.json) <br>
- [DexScreener API reference](https://docs.dexscreener.com/api/reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market-data operations; no credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

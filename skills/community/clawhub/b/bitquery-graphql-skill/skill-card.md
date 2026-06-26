## Description: <br>
Use Bitquery GraphQL through UXC for onchain trades, transfers, token holder analysis, balances, and market structure queries across supported networks, with OAuth client_credentials authentication and query-first execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate to Bitquery, inspect GraphQL operations, and run focused onchain queries or live subscriptions for trades, transfers, holder analysis, balances, and market structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bitquery OAuth client secrets could be exposed in shared terminals, logs, or copied command history. <br>
Mitigation: Use least-privileged Bitquery application credentials and avoid pasting real client secrets into shared terminals or logs. <br>
Risk: Live subscriptions may consume API quota or grow local output files unexpectedly. <br>
Mitigation: Monitor running subscriptions, use narrow `_select` shapes, and stop streams when they are no longer needed. <br>
Risk: The skill depends on the local `uxc` tool for authentication, endpoint binding, and GraphQL execution. <br>
Mitigation: Install only when the local `uxc` tool is trusted and verify auth bindings before running authenticated Bitquery operations. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Bitquery GraphQL Endpoint](https://streaming.bitquery.io/graphql) <br>
- [Bitquery OAuth Token Endpoint](https://oauth2.bitquery.io/oauth2/token) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON GraphQL arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize help-first schema inspection, OAuth setup, explicit GraphQL selection sets, and JSON response parsing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

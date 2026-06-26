## Description: <br>
Read-only CoinFound RWA data skill backed by a bundled endpoint catalog and schema snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darrenluo](https://clawhub.ai/user/darrenluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch CoinFound real-world-asset data through supported read-only GET endpoints, using the bundled endpoint catalog and schema snapshots to choose routes and interpret responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use makes live GET requests to CoinFound's API. <br>
Mitigation: Run it only where outbound CoinFound API access is expected, and avoid placing sensitive values in query parameters. <br>
Risk: The optional schema probe can write refreshed schema snapshots and retain small excerpts of live API responses. <br>
Mitigation: Use snapshot writing only when intentionally refreshing local schema evidence, and review retained response excerpts before redistribution. <br>
Risk: Bundled schema snapshots may differ from live CoinFound responses. <br>
Mitigation: Prefer bundled snapshots for planning, trust live responses when a conflict is observed, and schedule a schema refresh for unresolved structures. <br>


## Reference(s): <br>
- [RWA Read Workflow](references/rwa-read-workflow.md) <br>
- [RWA Read Capabilities](references/rwa-read-capabilities.md) <br>
- [RWA Read Integration Notes](references/rwa-read-integration-notes.md) <br>
- [CoinFound API Base](https://api.coinfound.org/api/kakyoin) <br>
- [ClawHub Release Page](https://clawhub.ai/darrenluo/coinfound-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON payloads and Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns request context, response envelope, normalized data, display data, shape family, and schema source.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

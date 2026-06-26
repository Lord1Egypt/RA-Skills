## Description: <br>
Bilibili garb (个性装扮) data collection and management for searching garb items, querying suit/collection details, scanning benefit data for owned items (including discontinued), and determining scarcity tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuangzhanzhiwang](https://clawhub.ai/user/kuangzhanzhiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Bilibili collectors use this skill to search garb items, inspect suit and collection details, recover discontinued-item benefit data, and determine scarcity tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to capture and store powerful Bilibili account session credentials. <br>
Mitigation: Use a limited or throwaway account when possible, keep credentials out of shared workspaces and logs, and rotate or revoke tokens after use. <br>
Risk: Traffic-capture instructions for obtaining Bilibili credentials may create account or platform-policy risk. <br>
Mitigation: Proceed only when the user understands the account risk and has confirmed that credential capture is acceptable for their own account and environment. <br>
Risk: Debug output or command history can expose access keys, cookies, CSRF tokens, or user identifiers. <br>
Mitigation: Prefer config files or environment variables over inline command tokens, avoid debug mode with real credentials unless necessary, and review logs before sharing. <br>


## Reference(s): <br>
- [Bilibili Garb API Reference](references/bilibili-garb-api-reference.md) <br>
- [Bilibili Garb SOP](references/bilibili-garb-sop.md) <br>
- [ClawHub skill page](https://clawhub.ai/kuangzhanzhiwang/bilibili-garb) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown command output, shell command examples, configuration snippets, and NDJSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and detail commands print Markdown; the benefit scanner appends records to data/garb-benefit-results.ndjson.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

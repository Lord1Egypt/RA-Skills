## Description: <br>
AdMapix raw data layer for ad creatives, apps, rankings, downloads/revenue, and market metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly0pants](https://clawhub.ai/user/fly0pants) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to query AdMapix for raw ad creative, app intelligence, ranking, download, revenue, distribution, and market metadata. It is intended as a composable data layer where the calling agent handles any analysis or presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-authenticated requests send search terms, app identifiers, company identifiers, and related query data to AdMapix. <br>
Mitigation: Use the skill only when sharing those query terms with AdMapix is acceptable for the task and organization. <br>
Risk: The skill requires an AdMapix API key. <br>
Mitigation: Store the key in the host secret or configuration store and do not paste it into chat, logs, generated output, or links. <br>
Risk: Download and revenue figures are third-party estimates rather than official app-store values. <br>
Mitigation: Present those values as estimates and avoid treating them as authoritative financial or store-reported metrics. <br>


## Reference(s): <br>
- [AdMapix Skill Page](https://clawhub.ai/fly0pants/admapix) <br>
- [AdMapix Website](https://www.admapix.com) <br>
- [AdMapix API](https://api.admapix.com) <br>
- [Creative Search API](references/api-creative.md) <br>
- [Product API](references/api-product.md) <br>
- [Ranking API](references/api-ranking.md) <br>
- [Download and Revenue API](references/api-download-revenue.md) <br>
- [Distribution API](references/api-distribution.md) <br>
- [Market API](references/api-market.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Raw structured JSON with occasional Markdown setup guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves API field names and returns third-party download and revenue estimates without analysis or summarization.] <br>

## Skill Version(s): <br>
1.0.30 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

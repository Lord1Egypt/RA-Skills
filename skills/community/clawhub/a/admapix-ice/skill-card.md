## Description: <br>
Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, exploring rankings, tracking download and revenue estimates, and reviewing market insights through AdMapix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BKMCICE](https://clawhub.ai/user/BKMCICE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ad analysts, growth teams, app publishers, and market researchers use this skill to query AdMapix for ad creative discovery, competitor app analysis, rankings, estimated downloads and revenue, and market-level advertising insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep research mode may send the user's AdMapix API key, prompt, and business context to deepresearch.admapix.com without clear user-facing disclosure or consent. <br>
Mitigation: Use a scoped or easily revocable API key, avoid sensitive business context, and confirm the publisher's key handling, retention, and consent practices before enabling deep research. <br>
Risk: Download and revenue figures are third-party estimates and may be unsuitable as sole evidence for business decisions. <br>
Mitigation: Present estimated metrics with the skill's disclaimer and validate important conclusions against additional data sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BKMCICE/admapix-ice) <br>
- [AdMapix website](https://www.admapix.com) <br>
- [Creative API reference](references/api-creative.md) <br>
- [Product API reference](references/api-product.md) <br>
- [Ranking API reference](references/api-ranking.md) <br>
- [Download and revenue API reference](references/api-download-revenue.md) <br>
- [Distribution API reference](references/api-distribution.md) <br>
- [Market API reference](references/api-market.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries, tables, links, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include H5 result links, bilingual English or Chinese responses, and disclaimers for third-party estimated download and revenue data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

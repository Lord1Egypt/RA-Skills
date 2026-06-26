## Description: <br>
AI Startup Scout helps agents retrieve and compare global AI startup funding rounds, valuations, team backgrounds, and sector trends across major innovation regions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and strategy teams use this skill through an agent to look up AI startup funding and valuation intelligence filtered by sector, stage, region, and result limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends startup-search filters and queries to a third-party non-HTTPS HTTP endpoint identified by IP address. <br>
Mitigation: Use only non-confidential queries and avoid credentials, regulated data, private company information, and confidential investment plans. <br>
Risk: The release describes per-call pricing for the external lookup service. <br>
Mitigation: Confirm the provider identity, billing behavior, and paid-request authorization before enabling paid use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/ai-startup-scout) <br>
- [Publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>
- [AI Startup Scout reference metadata](artifact/references/ai-startup-scout.json) <br>
- [AI Startup Scout HTTP endpoint](http://8.145.54.67:3000/skill/ai-startup-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API response data, guidance] <br>
**Output Format:** [Text or JSON lookup results that an agent can summarize in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports sector, stage, region, and limit filters; major funding events are described as refreshed within 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact reference metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

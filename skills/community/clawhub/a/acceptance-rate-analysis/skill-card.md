## Description: <br>
Analyzes declines in acceptance rate through staged attribution, locating anomalous slices and escalating through capital, asset, and sensitive-funding checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzhou1982](https://clawhub.ai/user/mzhou1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operations teams, and data engineers use this skill to investigate why acceptance rate declined over a day or week. It guides the agent through a scripted, staged workflow that compares periods, identifies affected customer/product slices, and presents markdown evidence for the attribution path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a browser-derived DataWorks access token and may persist it in user-level environment variables. <br>
Mitigation: Use a short-lived or least-privilege token, avoid shared machines, pass credentials explicitly when possible, and remove BIGDATA_ACCESS_TOKEN after use when persistence is not intended. <br>
Risk: Debug or verbose query logging could expose sensitive query or account context if enabled. <br>
Mitigation: Keep debug logging disabled unless troubleshooting, disable verbose query logging, and review generated logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzhou1982/acceptance-rate-analysis) <br>
- [DataWorks access-token source page](https://data.jirongyunke.net/data-pc-bdopr-fe/hoc-inquiry/index) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with tables, status blocks, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIGDATA_ACCESS_TOKEN to query DataWorks; debug output is disabled by default unless explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

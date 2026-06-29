## Description: <br>
Provides statistics, rankings, and analysis for the Fantasy NBA Israel league through an API-backed MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fantasy NBA league participants and analysts use this skill to retrieve team lists, standings, rotisserie ranking points, shooting stats, and detailed team and player statistics from the XiaoBenYang-backed service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the supplied XBY API key in a local .env file. <br>
Mitigation: Treat the .env file as sensitive, avoid committing it, and remove XBY_APIKEY from .env when the skill is no longer used. <br>
Risk: Minor leftover labels from another template may confuse setup or review. <br>
Mitigation: Review configuration labels and user-facing guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/alinklab/fantasynbaleague) <br>
- [XiaoBenYang service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries of API-backed league statistics, rankings, and team details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY API key; responses depend on xiaobenyang.com API availability and returned data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

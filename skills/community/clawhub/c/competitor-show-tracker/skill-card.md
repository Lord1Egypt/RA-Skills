## Description: <br>
Ranks upcoming trade shows by how many selected competitors are confirmed as exhibitors, then summarizes overlaps and follow-up actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business development, marketing, and competitive-intelligence teams use this skill before a trade show cycle to compare competitor attendance, prioritize events, and decide where to investigate or invest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends competitor company names to Lensmor's external service. <br>
Mitigation: Confirm trust in Lensmor and its terms before use, and avoid submitting highly confidential internal labels. <br>
Risk: The skill depends on a bearer API key for Lensmor access. <br>
Mitigation: Use a dedicated revocable API key where possible and do not include the key in prompts, outputs, logs, or shared artifacts. <br>


## Reference(s): <br>
- [Competitor Show Tracker on ClawHub](https://clawhub.ai/weilun88313/competitor-show-tracker) <br>
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=competitor-show-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with summary fields, ranked tables, event detail sections, insights, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; outputs should not reveal the key and should state when Lensmor results may be incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
futurespro-panda helps agents look up futures fees, margins, special product account requirements, trading announcements, trading calendars, and futures-company lists through an external HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mabtush13](https://clawhub.ai/user/mabtush13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query futures fee, margin, special-product, announcement, calendar, and company-list data and summarize the returned results for user questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Futures lookup terms are sent to the listed external API or to an alternate endpoint explicitly provided by the user. <br>
Mitigation: Use only non-sensitive lookup terms, avoid account numbers, private positions, and trading strategy details, and confirm that any alternate endpoint is trusted before querying it. <br>
Risk: Fee, margin, and announcement data may be incomplete, stale, or unsuitable for trading decisions. <br>
Mitigation: Verify important fee or margin data with official exchange or broker sources before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mabtush13/futurespro-panda) <br>
- [Default futures API endpoint](https://124.221.52.208) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional tables and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live API results; users should verify important fee or margin data with official exchange or broker sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

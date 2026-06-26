## Description: <br>
Football transfer intelligence for real-time rumour tracking, AI Truth Meter credibility scores, and multi-source verification across 137,000+ transfer events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeleon](https://clawhub.ai/user/leeleon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and football analysts use this skill to retrieve trending transfer rumours, inspect player-specific rumour profiles, and request credibility scores for player-to-club links. The skill helps an agent summarize source signals, transfer likelihood, sentiment, and relevant error or credit guidance from the Rising Transfers API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Football player and club search terms are sent to Rising Transfers for API-backed lookups. <br>
Mitigation: Install only if that data sharing is acceptable, and use hot topics mode when detailed search terms do not need to be sent. <br>
Risk: Authenticated detailed lookups can consume Rising Transfers credits. <br>
Mitigation: Use a limited or dedicated RT_API_KEY and monitor credit usage for transfer detail and Truth Meter queries. <br>
Risk: The skill may be invoked automatically for football transfer questions. <br>
Mitigation: Disable automatic skill discovery or approve API-backed queries manually when stricter control is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leeleon/football-transfer-intel) <br>
- [Rising Transfers API](https://api.risingtransfers.com) <br>
- [Hot topics endpoint](https://api.risingtransfers.com/api/v1/intelligence/hot-topics) <br>
- [Transfer intelligence endpoint](https://api.risingtransfers.com/api/v1/intelligence/transfer) <br>
- [Truth Meter verification endpoint](https://api.risingtransfers.com/api/v1/intel/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown transfer summaries with credibility scores, source lists, API-derived fields, and concise setup or error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RT_API_KEY for authenticated detailed lookups; hot topics can run without an API key. Detailed calls may consume Rising Transfers credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

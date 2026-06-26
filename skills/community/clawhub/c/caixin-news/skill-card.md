## Description: <br>
Fetch and summarize Chinese tech news from 财新网 (caixin.com) when users ask for Caixin technology updates or news from caixin.com/tech/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent Caixin technology articles and present concise Chinese summaries with dates, titles, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Results depend on outbound access to Caixin and may be affected by site availability, access restrictions, or paywall behavior. <br>
Mitigation: Confirm that the agent is allowed to make outbound web requests to Caixin and treat unavailable or restricted content as a retrieval limitation. <br>
Risk: News summaries may omit context or become stale as Caixin updates its technology channel. <br>
Mitigation: Include source links and dates with summaries so readers can verify current details against the original articles. <br>


## Reference(s): <br>
- [Caixin Technology Channel](https://www.caixin.com/tech/) <br>
- [ClawHub skill page](https://clawhub.ai/goog/caixin-news) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain Chinese text with dated article summaries and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Articles are presented in reverse chronological order and filtered for duplicates, stock-code-only entries, and irrelevant noise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

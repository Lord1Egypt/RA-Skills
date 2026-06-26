## Description: <br>
Queries Douyin daily like-surge rankings, returning TOP50 works ranked by single-day new likes with category filtering and up to 30 days of historical lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, short-video creators, MCN agencies, and data analysts use this skill to find Douyin works with rapid daily like growth, filter rankings by content category, and review recent historical trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires REDFOX_API_KEY for RedFoxHub API access, so accidental disclosure could expose the user's account or quota. <br>
Mitigation: Store REDFOX_API_KEY only as a secret or environment variable, avoid pasting real keys into chats, files, or logs, and rotate the key if exposure is suspected. <br>
Risk: Daily subscription or push behavior may create recurring automated delivery that users did not intend to enable. <br>
Mitigation: Confirm the selected category, schedule, and subscription preference before enabling any recurring daily push. <br>
Risk: The ranking data is a daily ingestion snapshot and may differ from cumulative public engagement counts. <br>
Mitigation: Present the data as single-day new interaction counts and include the update time and lookback limits when reporting results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-content-surge) <br>
- [API configuration](references/api-config.md) <br>
- [Interaction guide](references/interaction-guide.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Douyin hot content rank API](https://redfox.hk/story/api/dy/search/hotContentRank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown ranking tables with clickable Douyin links, plus concise configuration and error-handling guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to TOP20 results; can return up to 50 entries per category; uses yesterday's data by default, updates daily at 17:00, and supports a 30-day lookback.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

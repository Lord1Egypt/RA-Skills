## Description: <br>
Searches Douyin for high-engagement videos by keyword, optionally filters by date range, and returns structured trend results with engagement metrics and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, and marketing teams use this skill to research Douyin topics, compare high-engagement works, and monitor trends by keyword or date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to RedFox using a user-provided REDFOX_API_KEY. <br>
Mitigation: Use the platform's normal secret or configuration mechanism, avoid pasting the key into chat or logs, and confirm the key can be reset or revoked. <br>
Risk: The subscription workflow can create recurring daily Douyin searches and notifications. <br>
Mitigation: Only confirm a subscription after understanding how to disable the recurring task later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/douyin-search-pro) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown tables with links, concise setup guidance, and optional subscription instructions; the helper script returns JSON for agent processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; result tables include title, author, engagement counts, source link, and publish time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

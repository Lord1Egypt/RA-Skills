## Description: <br>
抖音账号订阅追踪 lets an agent subscribe to Douyin account IDs, fetch recent works on a daily 9:00 schedule, and produce Markdown tables plus HTML reports with collection, comment, share, like, and publish-time data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, short-video creators, brands, and MCNs use this skill to monitor specified Douyin account IDs, receive daily content digests, and review account-level performance trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redfox API key and sends monitored Douyin account IDs to Redfox, which may expose business or competitor-tracking interests. <br>
Mitigation: Use a scoped and revocable API key where possible, verify the key source before use, and avoid monitoring account IDs that should not be shared with the service. <br>
Risk: The skill can create or update recurring daily monitoring tasks. <br>
Mitigation: Confirm each subscription and automation change with the user, and review created scheduled tasks after setup. <br>
Risk: Release evidence states that local subscription storage under ~/.qoder/douyin_subscriptions.json is under-disclosed relative to the no-local-storage wording. <br>
Mitigation: Review and clear that local subscription file when subscriptions should no longer persist on the machine. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/redfox-data/douyin-subscribe) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>
- [Douyin data API endpoint](https://redfox.hk/story/api/dyData/searchWorkList) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal output, shell commands, and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update recurring daily automation tasks and may generate local HTML report files when fetched works are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

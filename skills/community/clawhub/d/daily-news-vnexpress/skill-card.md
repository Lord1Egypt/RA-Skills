## Description: <br>
Fetches the latest trending VNExpress RSS news for selected topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrNquyen](https://clawhub.ai/user/MrNquyen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to fetch current VNExpress RSS headlines for supported topics and summarize relevant items for users asking for latest news or trending events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to record user behavior in a local USERS.md file without clear notice, limits, or consent. <br>
Mitigation: Remove or ignore local behavior logging unless the user explicitly wants it, and review any retained local files. <br>
Risk: The skill fetches live RSS content and installs unpinned Python dependencies. <br>
Mitigation: Run it in an isolated environment, review fetched news before relying on it, and prefer pinned dependency versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrNquyen/daily-news-vnexpress) <br>
- [VNExpress RSS feeds](https://vnexpress.net/rss/tin-moi-nhat.rss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown summaries with news titles, links, summaries, and published dates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses topic and count arguments to select VNExpress RSS feeds and item limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

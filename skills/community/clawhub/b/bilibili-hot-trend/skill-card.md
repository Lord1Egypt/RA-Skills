## Description: <br>
Bilibili helps agents summarize public Bilibili video, article, livestream, creator, search, and ranking data without downloads or bulk collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather lightweight summaries of public Bilibili trends, creator performance, search results, and ranking pages for internal analysis and reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill while logged in may include information visible in that session. <br>
Mitigation: Prefer public pages, avoid sensitive account or personal-page content, and review summaries before sharing. <br>
Risk: Requests for downloads, bulk scraping, account actions, or bypass attempts would exceed the skill's intended read-only posture. <br>
Mitigation: Decline those requests, keep collection lightweight, and follow Bilibili platform rules. <br>
Risk: Dynamic rendering and human verification flows can make extracted metrics incomplete or stale. <br>
Mitigation: Have a human open or verify pages when needed and confirm important metrics before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeKungfu/bilibili-hot-trend) <br>
- [Bilibili Home](https://www.bilibili.com/) <br>
- [Bilibili Ranking](https://www.bilibili.com/v/popular/rank) <br>
- [Bilibili Search](https://search.bilibili.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only summaries from public Bilibili pages; no downloads, account actions, bypass attempts, or bulk collection.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

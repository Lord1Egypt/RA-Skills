## Description: <br>
Monitor Fox News sections and breaking updates with official RSS routes, live-event tracking, and optional outside verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Readers and agents use this skill to monitor Fox News sections, official RSS feeds, live pages, clips, and opinion surfaces while keeping source boundaries, timestamps, and optional outside verification explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawScan verdict is suspicious and says the bundle includes maintainer/developer-skill behavior that warrants trust review. <br>
Mitigation: Install only if the publisher is trusted, review the skill text before use, and keep execution constrained to the disclosed Fox News workflows. <br>
Risk: The skill can fetch public news pages and RSS feeds and may save durable preferences or archived briefings under ~/fox-news/. <br>
Mitigation: Confirm broad fetches before opening multiple links, avoid sharing credentials, and save local preferences or archives only after explicit user approval. <br>
Risk: Fox News reporting, live pages, and opinion content may reflect editorial framing or become stale during breaking events. <br>
Mitigation: Label opinion separately from straight reporting, timestamp freshness claims, and add outside verification when the user asks for credibility checks or contested-story context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/fox-news) <br>
- [Skill homepage](https://clawic.com/skills/fox-news) <br>
- [Fox News](https://www.foxnews.com) <br>
- [Fox News latest RSS feed](https://moxie.foxnews.com/google-publisher/latest.xml) <br>
- [Fox News help](https://help.foxnews.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings with source labels, timestamps, optional shell commands, and local preference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local notes under ~/fox-news/ only with user permission; uses public Fox News web pages, RSS feeds, and help pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

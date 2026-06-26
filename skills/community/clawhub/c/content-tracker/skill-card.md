## Description: <br>
Tracks timely topics, monitors public webpage updates, aggregates third-party hot-news sources, and saves Markdown briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changsheng0804](https://clawhub.ai/user/changsheng0804) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track industry or news topics, monitor public links for updates, aggregate hot-news sources, and generate recurring Markdown briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill on private or login-required URLs could expose sensitive content to the agent workflow or fail in unsupported ways. <br>
Mitigation: Use it for public news and public webpage updates only, and avoid private, authenticated, or access-controlled sources. <br>
Risk: Generated Markdown reports are saved locally and may contain summaries or links that should not be broadly shared. <br>
Mitigation: Review the report destination and generated briefings before sharing or retaining them. <br>
Risk: Recurring schedules can create ongoing monitoring beyond the user's immediate request. <br>
Mitigation: Enable recurring runs only when ongoing monitoring is intended, and periodically review the cadence and tracked topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changsheng0804/content-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefings with source links, summaries, and freshness notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under ./我的追踪/{yyyy_mm_dd}/{topic}.md when tracking runs produce results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

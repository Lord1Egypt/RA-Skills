## Description: <br>
AI industry news aggregation from curated RSS feeds. Catches model releases from major labs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justintieu](https://clawhub.ai/user/justintieu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and AI practitioners use this skill to generate concise daily or weekly AI news briefings from curated RSS feeds, with emphasis on model releases, research, industry news, product updates, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings depend on public RSS feeds that may fail, become stale, or omit major sources. <br>
Mitigation: Continue with available feeds, note failed sources or coverage gaps, and manually check known missing labs for major releases. <br>
Risk: Optional saved briefings or automated delivery could write or send content to unintended locations. <br>
Mitigation: Use the explicit /ai-news command where possible, save only to a dedicated folder, and configure cron or messaging delivery only for non-sensitive destinations you control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justintieu/ai-news-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/justintieu) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Olshansk RSS Feeds](https://github.com/Olshansk/rss-feeds) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing with categorized news items and optional saved Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source links, failed-feed notes, cached briefing reuse, and coverage-gap reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

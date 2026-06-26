## Description: <br>
Personalized news briefings from your chosen sources, delivered morning or evening, with voice option and smart filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to receive personalized news briefings, current-event updates, deeper follow-up summaries, and optional scheduled delivery based on their preferred topics, sources, geography, and format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News interests, region, delivery schedule, source preferences, and optional briefing archives may be saved locally in ~/daily-news-digest/. <br>
Mitigation: Review what the skill will save before installation and edit or remove local memory and archive files when preferences change. <br>
Risk: Scheduled delivery can send news briefings to configured channels if the user enables automation. <br>
Mitigation: Confirm the exact schedule, timezone, and delivery channel before enabling or changing automated briefings. <br>
Risk: Search queries or briefing text may be sent to configured third-party services when news discovery or voice synthesis is enabled. <br>
Mitigation: Use only trusted service configurations and enable voice synthesis only when briefing text may be shared with the TTS provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/daily-news-digest) <br>
- [Skill Homepage](https://clawic.com/skills/daily-news-digest) <br>
- [Briefing Formats](formats.md) <br>
- [Memory Template](memory-template.md) <br>
- [Scheduling Guide](scheduling.md) <br>
- [Setup Guide](setup.md) <br>
- [Source Configuration](sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain-text news briefings, optional archive files, and scheduling configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local preference files under ~/daily-news-digest/ and optional scheduled delivery or voice synthesis when the user enables them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

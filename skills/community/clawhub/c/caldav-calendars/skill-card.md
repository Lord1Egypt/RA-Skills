## Description: <br>
Sync and query CalDAV calendars using vdirsyncer and khal, while also documenting broad SkillBoss API access for model routing, media generation, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobeyRebecca](https://clawhub.ai/user/TobeyRebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to discover and call SkillBoss-hosted models for chat, media generation, audio, search, scraping, document processing, email, and SMS workflows. The release is presented as a CalDAV calendar skill, so users should confirm the intended API gateway behavior before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as a CalDAV calendar skill but primarily enables broad SkillBoss API gateway actions. <br>
Mitigation: Install only when broad model routing, media generation, search, scraping, document processing, email, SMS, and OTP workflows are intended. <br>
Risk: The skill can send sensitive content, contact details, calendar data, or outbound messages through external APIs. <br>
Mitigation: Require explicit user approval before sending sensitive data or initiating email, SMS, OTP, scraping, or generation actions. <br>
Risk: A single SKILLBOSS_API_KEY authorizes access across many model and messaging capabilities. <br>
Mitigation: Scope, store, and rotate the API key according to the user's credential policy, and avoid exposing it in prompts, logs, or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TobeyRebecca/caldav-calendars) <br>
- [SkillBoss API Base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Audio Models](audio-models.md) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Search and Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

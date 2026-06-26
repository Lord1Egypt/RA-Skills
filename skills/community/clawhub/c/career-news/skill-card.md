## Description: <br>
Aggregates profession-targeted news from X (Twitter), Google News, Grok, and global media into bilingual daily or on-demand career briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals and individual users use this skill to register career interests, manage multi-profession subscriptions, and generate concise bilingual news prompts or briefs for daily and on-demand reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local user preference files that may contain profession, region, language, and keyword interests. <br>
Mitigation: Avoid sensitive keywords, treat data/users/*.json as personal preference data, and delete those files when the stored profile is no longer needed. <br>
Risk: Scheduled daily runs can generate recurring prompts even after setup is complete. <br>
Mitigation: Only add the cron job when scheduled daily prompt generation is intended, and disable or remove it when no longer needed. <br>


## Reference(s): <br>
- [Career News on ClawHub](https://clawhub.ai/cosmofang/career-news) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown-style briefs with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Registration and subscription scripts may create local JSON preference files under data/users.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

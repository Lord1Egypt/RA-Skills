## Description: <br>
Family Cultivation Coach helps parents collect child profiles, family constraints, goals, and execution preferences to generate practical weekly cultivation schedules, review templates, and incremental updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangchao228](https://clawhub.ai/user/yangchao228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and family caregivers use this skill to turn child information, school schedules, family routines, and goals into weekly plans, daily records, and review guidance. It also supports Feishu or Notion-backed record keeping when the user configures those integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive child and family records through Feishu or Notion. <br>
Mitigation: Use a dedicated workspace or database, limit access to necessary users, test with dummy data first, and confirm retention and deletion procedures before storing real records. <br>
Risk: The skill may require Feishu or Notion credentials for storage integrations. <br>
Mitigation: Use a least-privilege integration, avoid pasting production secrets into ordinary chat, and revoke or rotate credentials when access is no longer needed. <br>
Risk: The skill can push or write family records to connected services. <br>
Mitigation: Confirm recipients, destination tables or databases, and notification behavior before enabling ongoing record writes or pushes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangchao228/family-cultivation-coach) <br>
- [Publisher profile](https://clawhub.ai/user/yangchao228) <br>
- [Project homepage](https://github.com/yangchao228/family-baby-asistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown schedules, review templates, structured records, and concise configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured schedule data for future reminders when requested by the user.] <br>

## Skill Version(s): <br>
1.6.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

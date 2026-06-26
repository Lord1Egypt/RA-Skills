## Description: <br>
Autonomous lead generation skill that finds freshly funded companies matching an ideal customer profile, researches them, and delivers qualified leads with personalized outreach drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zich-agent](https://clawhub.ai/user/zich-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales teams, founders, agencies, recruiters, consultants, and developers use Lead Hunter to set up and run recurring lead generation. It configures an ICP, gathers startup funding signals, researches prospects, scores fit, and drafts outreach without automatically sending messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scrape websites and install scraping dependencies such as crawl4ai and Chromium. <br>
Mitigation: Review configured sources before first use and approve any dependency or browser installation before running the scraper fallback. <br>
Risk: The skill can store lead data, seen-company state, and run logs locally. <br>
Mitigation: Choose an appropriate output location, avoid storing unnecessary personal data, and review generated lead files and memory logs. <br>
Risk: The skill can optionally create recurring runs through cron scheduling. <br>
Mitigation: Enable scheduling only when recurring prospecting is intended, and verify the schedule and timezone before activation. <br>
Risk: Asana output may require workspace and parent task identifiers or credentials from another skill. <br>
Mitigation: Confirm whether Asana integration is needed and use the minimum required access for task creation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zich-agent/agitech-lead-hunter) <br>
- [Lead Hunter - Onboarding Interview](references/onboarding.md) <br>
- [Lead Sources by Industry](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, CSV rows, Asana task command notes, configuration JSON, and outreach draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits full research to 5 leads per run; drafts outreach but does not send messages automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

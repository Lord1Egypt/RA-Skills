## Description: <br>
AI dating assistant. Check matching progress, relay deep questions, report results for your human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to check AILove matching progress, relay pending questions to the human, submit the human's verbatim answers, and summarize match results or scheduled updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to store an AILove account key locally. <br>
Mitigation: Use a secret manager or private environment file, never commit the key, send it only to the documented AILove API domain, and rotate it when access is no longer needed. <br>
Risk: Recurring scheduled updates can expose sensitive dating-status information in messaging channels. <br>
Mitigation: Choose a private delivery target, confirm cron jobs before adding them, and remove scheduled jobs when the service is no longer in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/aidating) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove skill file](https://heerweiyi.cc/skill.md) <br>
- [AILove agent API base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with curl examples, OpenClaw cron commands, configuration snippets, and human-facing status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AILove agent key and may set up twice-daily scheduled check-ins to a selected messaging target.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

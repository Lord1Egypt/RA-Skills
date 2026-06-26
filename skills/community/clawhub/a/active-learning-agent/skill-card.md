## Description: <br>
Active Learning Agent continuously reviews Feishu workplace context, builds topic timelines, and proactively delivers analyses, summaries, risk alerts, or drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cscguochang](https://clawhub.ai/user/cscguochang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees using Feishu use this recurring assistant to connect messages, documents, meetings, recordings, and calendars into accurate work timelines. It helps produce concise cross-source summaries, risk alerts, analyses, and draft documents while recording long-term insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant can continuously inspect private Feishu chats, documents, meetings, recordings, calendars, and long-term memory files. <br>
Mitigation: Restrict the Feishu sources it may inspect, review retained memory and log files, and define redaction and deletion procedures before enabling recurring scans. <br>
Risk: The assistant can send messages or create documents without clear approval controls. <br>
Mitigation: Require user approval before sending messages or creating Feishu documents, especially for summaries, alerts, or drafts based on private workplace data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cscguochang/active-learning-agent) <br>
- [Publisher profile](https://clawhub.ai/user/cscguochang) <br>
- [MIT-0 license](https://spdx.org/licenses/MIT-0.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown messages, Feishu document drafts, action logs, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory files and Feishu documents when the configured tools permit it.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

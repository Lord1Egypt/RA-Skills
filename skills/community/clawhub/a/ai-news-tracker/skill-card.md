## Description: <br>
AI News Tracker monitors AI and technology industry updates across multilingual sources, prepares structured summaries, and can push major events to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billxfan](https://clawhub.ai/user/billxfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users who follow AI and technology news use this skill to collect recent multilingual sources, deduplicate events, prepare daily summaries, and send urgent updates to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled Feishu sending could deliver summaries to the wrong recipient or expose unrelated notes if the workspace memory contains sensitive content. <br>
Mitigation: Verify the Feishu recipient before enabling cron and keep unrelated sensitive notes out of MEMORY.md. <br>
Risk: Automated news collection can include stale, duplicate, or incorrectly timed items. <br>
Mitigation: Review important summaries before relying on them and preserve the required event time, source time, and original link for each item. <br>
Risk: Draft cleanup after sending can remove the local copy users may expect to retain. <br>
Mitigation: Decide whether retained copies or a send-confirmation step are required before enabling scheduled delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billxfan/ai-news-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and Feishu message text with source links and event-time labels.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an intermediate Markdown draft before sending and cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

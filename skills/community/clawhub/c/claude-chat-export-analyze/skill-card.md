## Description: <br>
Guides agents through exporting, validating, searching, summarizing, and reporting on Claude.ai web chat history from a local conversations.json file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoqing404](https://clawhub.ai/user/shaoqing404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and Claude.ai users use this skill to inspect local Claude.ai web chat exports, find prior conversations, build timelines, summarize themes, and prepare readable reports while avoiding full-file disclosure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude.ai export files can contain sensitive personal data, credentials, or private work content. <br>
Mitigation: Analyze the local file selectively, avoid echoing full contents, redact sensitive fields in reports by default, and advise the user to remove the export from the workspace after use. <br>
Risk: Large conversations.json files can exceed context or terminal output limits if read or printed wholesale. <br>
Mitigation: Use targeted jq queries, validate the top-level structure first, and summarize or page long sessions instead of reading or printing the full export. <br>
Risk: The guidance includes shell commands that operate on user-provided file paths. <br>
Mitigation: Confirm the path and export source before running commands, and stop if the file shape suggests Claude Code, API, or another unsupported format. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/shaoqing404/ai-chat-timeline-skills/tree/main/skills/claude-chat-export-analyze) <br>
- [Claude.ai](https://claude.ai) <br>
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/claude-chat-export-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, text] <br>
**Output Format:** [Markdown guidance with jq command examples and concise analysis outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local summaries, timelines, selected excerpts, and redacted reports from user-provided Claude.ai export files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

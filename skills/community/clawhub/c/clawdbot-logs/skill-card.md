## Description: <br>
Analyze Clawdbot logs and diagnostics. Use when the user asks about bot performance, response times, errors, session stats, token usage, API costs, or wants to debug slow responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satriapamudji](https://clawhub.ai/user/satriapamudji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect local Clawdbot logs, session files, token usage, costs, response times, and service errors while troubleshooting bot performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Clawdbot session files and logs can contain private conversation content, token usage, costs, and operational details. <br>
Mitigation: Use aggregate diagnostics for routine troubleshooting and avoid printing raw recent messages unless the conversation content is necessary for the diagnosis. <br>
Risk: The diagnostic scripts read local journal entries and Clawdbot session files from the user's machine. <br>
Mitigation: Install and run the skill only in environments where local Clawdbot log and session-file access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satriapamudji/clawdbot-logs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local log excerpts, session statistics, token usage, cost summaries, service status, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Flowforge Builder Free helps agents define automation workflows as JSON, including scheduled, file-watch, and manual triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to create, review, and run JSON-based automation workflows for file operations, network requests, command execution, variable passing, basic conditions, retries, and logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow examples may read or write files, monitor directories, send network requests, execute shell commands, or run on schedules. <br>
Mitigation: Review every workflow before execution, keep watched directories narrow, avoid sending sensitive file contents to external APIs, and treat shell commands and cron entries as privileged actions. <br>


## Reference(s): <br>
- [Flowforge Builder Free on ClawHub](https://clawhub.ai/thcjp/skills/flowforge-builder-free) <br>
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow definitions and operational guidance for agent-assisted automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Alpha Feed Creator helps content and operations teams collect AI-related content from multiple platforms, rank it by semantic quality and engagement, and generate scheduled reports or team-channel updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, brand operations teams, and research teams use this skill to gather AI-related posts from configured sources, rank the results, and produce recurring daily or weekly reports. It supports scheduled collection, structured report output, and optional delivery to team channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect content from external sources and send reports to team channels. <br>
Mitigation: Review configured sources, push targets, and report destinations before enabling delivery. <br>
Risk: Recurring schedules can repeatedly publish incorrect or unwanted reports if configured too broadly. <br>
Mitigation: Use dry-run or test modes before enabling cron or recurring delivery. <br>
Risk: API keys and webhook tokens are required for some integrations. <br>
Mitigation: Keep credentials in environment variables or a secrets manager and avoid hardcoding them in configuration files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command, YAML configuration, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce report files or push summaries to configured team channels when the user enables those integrations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

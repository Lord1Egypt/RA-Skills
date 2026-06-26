## Description: <br>
Agent Job connects an AI agent to lobsterjob.com to start or stop task hosting, claim tasks, view earnings, and request withdrawals through /lobster commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liushuangfa666](https://clawhub.ai/user/liushuangfa666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to automate lobsterjob.com task claiming, polling, earnings checks, and withdrawal requests from an agent chat workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stored lobsterjob.com token for account actions, including task claiming, earnings checks, and withdrawal requests. <br>
Mitigation: Install only if you trust lobsterjob.com with the token, keep the token scoped and private, and require manual confirmation before any withdrawal. <br>
Risk: Starting hosting can create a recurring polling job that performs account actions without continuous user presence. <br>
Mitigation: Use explicit /lobster commands, disable or closely monitor the cron polling job when it is not needed, and verify job status with OpenClaw cron commands. <br>
Risk: The skill discovers local scripts and uploads metadata about installed skills to lobsterjob.com. <br>
Mitigation: Verify the script path before execution and install only if sharing installed-skill metadata with lobsterjob.com is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liushuangfa666/agent-job) <br>
- [lobsterjob.com](https://lobsterjob.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs command results from lobsterjob.com actions and local OpenClaw cron management.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

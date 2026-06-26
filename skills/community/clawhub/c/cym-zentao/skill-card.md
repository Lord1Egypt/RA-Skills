## Description: <br>
ZenTao project management CLI tool for creating tasks, batch-creating tasks, listing executions, and listing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15334615152](https://clawhub.ai/user/15334615152) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to connect an agent to ZenTao so it can inspect executions and tasks, then create individual or batch tasks from structured inputs or natural-language task requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stored ZenTao account credentials and can expose authentication tokens through the login command output. <br>
Mitigation: Use a least-privileged ZenTao account, avoid running login where command output may be logged, and review terminal or agent logs for accidental token exposure. <br>
Risk: The skill can create live ZenTao tasks, including batch task creation, without an additional confirmation step. <br>
Mitigation: Manually review execution IDs, fuzzy execution-name matches, assignees, dates, and task lists before allowing create-task or create-tasks-batch commands. <br>
Risk: A misconfigured API URL or credential source can send requests to the wrong ZenTao instance. <br>
Mitigation: Verify the ZenTao API URL in TOOLS.md before use and limit credentials to the intended project workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15334615152/cym-zentao) <br>
- [Publisher profile](https://clawhub.ai/user/15334615152) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [CLI package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and ZenTao API credentials configured in the local OpenClaw TOOLS.md file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact package.json reports 2.1.0 and artifact _meta.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

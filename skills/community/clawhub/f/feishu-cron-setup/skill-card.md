## Description: <br>
帮助用户创建、修复和验证飞书频道的 OpenClaw cron 定时任务投递，尤其适用于 isolated session 需要显式指定 --account 的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nicccmy](https://clawhub.ai/user/Nicccmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Feishu delivery for OpenClaw cron jobs, troubleshoot failed announce delivery, and verify that scheduled task results reach the intended Feishu recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent cron job could send the wrong message, run at the wrong time, or deliver to the wrong Feishu account or recipient. <br>
Mitigation: Confirm the cron schedule, timezone, message, Feishu account, and recipient open_id before creating or manually running the job. <br>
Risk: Inspecting local OpenClaw configuration can expose tokens or unrelated account configuration. <br>
Mitigation: Share only the account key required for --account and avoid exposing tokens or unrelated configuration from ~/.openclaw/openclaw.json. <br>
Risk: Created cron jobs continue to exist after setup and may keep delivering messages. <br>
Mitigation: List, disable, or delete scheduled jobs that are no longer needed after validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nicccmy/feishu-cron-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron creation examples, Feishu account and open_id checks, and delivery verification commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

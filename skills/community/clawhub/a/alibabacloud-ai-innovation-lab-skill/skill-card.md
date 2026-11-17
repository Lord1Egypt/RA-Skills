## Description: <br>
Helps users discover and one-click deploy popular AI open-source projects from Alibaba Cloud's AI Innovation Lab using current project data and a fixed Markdown recommendation template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, students, and AI practitioners use this skill to find recent AI open-source projects and start them quickly on Alibaba Cloud through one-click deployment links. The skill also guides explicit opt-in setup for recurring weekly recommendations when the runtime supports scheduling and memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches Aliyun project data and falls back to an OSS snapshot, so recommendations may depend on external content availability and parsing behavior. <br>
Mitigation: Review the fetch and fallback behavior before use, and rely on the documented statistics fallback when live or snapshot data is unavailable. <br>
Risk: Recurring recommendation jobs and persistent subscription memory can create ongoing user-facing actions. <br>
Mitigation: Only enable scheduling after explicit user opt-in, confirm memory support first, and provide clear modification and cancellation guidance. <br>
Risk: Cron setup guidance discusses environment-token handling across agent platforms. <br>
Mitigation: Do not pass plaintext tokens in commands; use environment variables only when the user explicitly needs authenticated runtime behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ai-innovation-lab-skill) <br>
- [Alibaba Cloud AI Innovation Lab](https://www.aliyun.com/daily-act/ecs/ai-innovation-lab) <br>
- [AI Innovation Lab OSS snapshot](https://ai-innovation-lab.oss-cn-beijing.aliyuncs.com/ai-innovation-lab.json) <br>
- [Output Format Reference](references/output-format.md) <br>
- [Scheduled Task Scheduler Implementation](references/cron-platforms.md) <br>
- [OSS Snapshot JSON Structure](references/json-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, preserved deployment links, and optional shell command or cron configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed 1-5 response structure, fetches live project data with OSS fallback, and only adds subscription guidance after explicit user intent and memory availability checks.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

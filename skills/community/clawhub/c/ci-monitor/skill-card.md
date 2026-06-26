## Description: <br>
Monitor and interact with CI/CD pipelines for Jenkins, GitHub Actions, and GitLab CI by checking build status, triggering builds, analyzing failed jobs, and viewing logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect CI/CD status, review failed job logs, summarize pipeline failures, and trigger or retry builds when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CI credentials and job logs can expose sensitive project or deployment information. <br>
Mitigation: Use least-privilege or temporary CI tokens and avoid pasting real tokens into shared chats or logs. <br>
Risk: Build triggers, workflow reruns, and pipeline retries are operational actions. <br>
Mitigation: Require explicit user confirmation before triggering builds, rerunning workflows, or retrying pipelines. <br>
Risk: Failure summaries based on logs may be incomplete or misleading. <br>
Mitigation: Confirm conclusions against the CI platform's source logs and test reports before taking corrective action. <br>


## Reference(s): <br>
- [CI Monitor on ClawHub](https://clawhub.ai/zhanghengyi1986-afk/ci-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/zhanghengyi1986-afk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CI status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests against Jenkins, GitHub Actions, or GitLab CI when credentials and user authorization are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Monitors Feishu task messages, starts isolated processing jobs, and sends task confirmation, progress, completion, and failure feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlzhao007](https://clawhub.ai/user/carlzhao007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a Feishu background listener that recognizes task-like chat messages and returns progress updates while independent Node.js worker processes handle each task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat message text can reach shell commands and background workers with weak scoping. <br>
Mitigation: Install only after review; avoid sensitive machines or production Feishu workspaces until shell-based feedback sending is replaced with argument-array execution or direct API calls and message sources are allowlisted. <br>
Risk: The listener and workers write local log and state files that may contain task text or operational details. <br>
Mitigation: Avoid placing secrets in task messages, and review or rotate .listener.log, .tasks.log, and .listener_state.json during operation. <br>
Risk: A background polling process can continue processing messages until it is stopped. <br>
Mitigation: Run the listener under supervision with a clear stop procedure and keep the process easy to terminate during review or incident response. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/carlzhao007/feishu-process-feedback) <br>
- [Feishu message API](https://open.feishu.cn/open-apis/im/v1/messages) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Feishu chat feedback messages, local log/state files, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a background Node.js listener with configurable polling interval, retry count, concurrency, timeout, and verbosity.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

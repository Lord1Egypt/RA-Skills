## Description: <br>
Persistent task memory and keep-alive loop for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techieter](https://clawhub.ai/user/techieter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to keep task state across restarts, context loss, and long-running work by maintaining local task notes and optional monitoring jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task records are stored as plaintext local notes under ~/.openclaw/memory/ and may contain sensitive work details. <br>
Mitigation: Avoid using the skill for secrets or highly confidential work unless local plaintext storage is acceptable. <br>
Risk: The installer configures recurring OpenClaw jobs, including monitoring jobs for long-running tasks and always-on validation and smoke-test jobs. <br>
Mitigation: Use /loop-stop when monitoring is not needed, and remove the listed cron jobs plus the skill directory during uninstall. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/techieter/agent-memory-boost) <br>
- [Memory Boost repository homepage](https://github.com/TechieTer/openclaw-memory-boost) <br>
- [INSTALL.md](INSTALL.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown prompts, local note templates, and installation shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local task-memory files under ~/.openclaw/memory/ and configures recurring OpenClaw jobs when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Clever Compact restores OpenClaw session continuity by saving local compact-state files and injecting the latest recent state at session start. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfulmines-star](https://clawhub.ai/user/jfulmines-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to preserve working context across new sessions, compaction, and overnight restarts. It is intended for local cross-session memory workflows where restored state helps an agent resume prior work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restored local memory can influence future agent behavior. <br>
Mitigation: Review or delete memory/compact-state files when needed, and keep secrets out of state summaries. <br>
Risk: Prompts or documents could ask the agent to flush unwanted or sensitive information into memory. <br>
Mitigation: Treat memory flush requests as state-changing actions and review the summary content before relying on it in later sessions. <br>


## Reference(s): <br>
- [Clever Compact on ClawHub](https://clawhub.ai/jfulmines-star/clever-compact) <br>
- [SECURITY.md](SECURITY.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown state summaries and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and restores local compact-state markdown files for OpenClaw sessions.] <br>

## Skill Version(s): <br>
2.2.5 (source: server release evidence, openclaw.plugin.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

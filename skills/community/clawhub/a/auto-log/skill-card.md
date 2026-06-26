## Description: <br>
Automatically creates daily activity logs for AI agents, including events, tasks, todos, and short summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socneo](https://clawhub.ai/user/socneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep persistent daily records of an AI agent's activity, task outcomes, todo items, and same-day summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local activity logs may retain sensitive work details, secrets, or personal data. <br>
Mitigation: Review the configured memory directory, avoid using the skill around secrets or sensitive personal data, and periodically delete or redact logs that should not be retained. <br>


## Reference(s): <br>
- [Auto Log ClawHub Page](https://clawhub.ai/socneo/auto-log) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Example Configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown log files, plain-text summaries, Python API calls, CLI commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local daily log files in the configured memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Feedback Learning helps OpenClaw agents detect feedback, log events, identify recurring patterns, promote repeated corrections into persistent rules, and produce weekly learning reports without LLM or API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Surdeddd](https://clawhub.ai/user/Surdeddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local feedback memory to OpenClaw agents, including manual or automatic event logging, pattern analysis, and weekly review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw feedback and context can be written to persistent local event logs and reports. <br>
Mitigation: Scope the learning directory per project or agent, avoid logging secrets or sensitive user text, and define expiry or deletion for old events. <br>
Risk: Repeated feedback can become active rules that influence future agents. <br>
Mitigation: Review genes.json before agents load it, and edit or remove promoted rules that are stale, unsafe, or unsupported. <br>
Risk: AGENTS.md hooks and scheduled jobs can automate feedback collection, pattern analysis, and rule promotion. <br>
Mitigation: Enable hooks and cron jobs only after confirming the workspace, paths, and human review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Surdeddd/feedback-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python commands, JSON examples, JSONL event records, JSON rule files, and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local feedback logs, grouped pattern data, promoted rule files, and weekly reports under the configured learning directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

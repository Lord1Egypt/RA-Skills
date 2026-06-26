## Description: <br>
Supervise Claude Code sessions running in tmux with Claude Code hooks, bash pre-filtering, and fast LLM triage to detect errors, stuck agents, and task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johba37](https://clawhub.ai/user/johba37) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to monitor long-running Claude Code sessions in tmux, triage stop/error/notification events, and route actionable status updates to an agent harness or notification backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook and watchdog scripts can read terminal output and send configured notifications, which may expose sensitive repository or session context. <br>
Mitigation: Install only in trusted projects and avoid remote LLM or webhook backends for sensitive repositories unless that exposure is acceptable. <br>
Risk: The watchdog can type nudges into live tmux sessions, so poorly scoped automation can approve or trigger unintended actions. <br>
Mitigation: Do not run the watchdog or auto-approve permission prompts until nudges are tightly allowlisted, logged, and reviewed. <br>
Risk: Generated Claude settings and project configuration can change lifecycle hook behavior for a repository. <br>
Mitigation: Review the generated .claude settings and .claude-code-supervisor.yml before enabling hooks. <br>
Risk: A fixed /tmp helper path can be overwritten or reused unexpectedly on shared systems. <br>
Mitigation: Move or remove the fixed /tmp helper before use in sensitive or multi-user environments. <br>


## Reference(s): <br>
- [State Detection Patterns](references/state-patterns.md) <br>
- [Escalation Rules](references/escalation-rules.md) <br>
- [Five Levels of AI-Assisted Programming](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces hook setup guidance, configuration examples, triage classifications, notification payloads, and tmux command patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Agent Guardian helps AI assistants reduce long no-response periods, stuck tasks, mixed-language replies, and opaque status by combining watchdog monitoring, status reporting, instant status queries, language consistency filtering, and message queue tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanxinyun1991](https://clawhub.ai/user/fanxinyun1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add watchdog, status-reporting, status-query, language-filtering, and message-tracking behavior around OpenClaw-based assistants and messaging channels. It is intended for assistant deployments where users need clearer progress feedback and faster visibility when an agent appears stuck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent host-level components can continue running through cron or systemd after installation. <br>
Mitigation: Install only in a controlled single-user environment, review service and cron entries before enabling them, and define an uninstall or rollback path before production use. <br>
Risk: The skill uses /tmp-based state and trigger files for status, queue, and activity tracking. <br>
Mitigation: Move state to a private directory with restrictive permissions before use on shared hosts or sensitive systems. <br>
Risk: Status messages may expose host metrics or operational state to configured messaging targets. <br>
Mitigation: Restrict status-query triggers and report targets to authenticated administrators and review message contents for sensitive deployment details. <br>
Risk: Optional channel patches modify bot message handling and outbound filtering behavior. <br>
Mitigation: Review patches before applying them, test on a staging bot, and disable automatic rewriting unless it is explicitly desired. <br>


## Reference(s): <br>
- [Agent Guardian ClawHub Release](https://clawhub.ai/fanxinyun1991/agent-guardian) <br>
- [Generic Channel Integration Guide](references/patches/generic.md) <br>
- [QQ Bot Channel Integration Guide](references/patches/qqbot.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON cron examples, and code patch snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or configure local scripts, cron entries, systemd service behavior, and channel plugin patches when the user follows the provided commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

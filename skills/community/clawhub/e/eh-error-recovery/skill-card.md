## Description: <br>
Error Recovery helps agents recover from rate limits, crashes, stale sessions, MCP disconnects, and model failures while avoiding generic retry loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to detect common agent failure modes and choose bounded recovery actions for rate limits, crash residue, MCP disconnects, stale sessions, and model failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recovery steps can send Enter to tmux panes after detecting rate-limit text. <br>
Mitigation: Restrict recovery to known agent panes and re-capture the pane before sending Enter; block destructive confirmations such as delete, overwrite, force push, or yes/no prompts. <br>
Risk: Crash recovery and cleanup steps can delete lock files or roll back state incorrectly. <br>
Mitigation: Use dry-run or confirmation for lock cleanup and rollback, scope cleanup paths tightly, and log each recovery action. <br>
Risk: Transcript scavenging can persist sensitive session content. <br>
Mitigation: Enable scavenging only with explicit opt-in, redaction, and retention limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/eh-error-recovery) <br>
- [Rate Limit Detection and Recovery](artifact/references/rate-limit.md) <br>
- [Crash Recovery](artifact/references/crash-recovery.md) <br>
- [Stale Session Daemon](artifact/references/stale-session.md) <br>
- [MCP Reconnection](artifact/references/mcp-reconnection.md) <br>
- [Graceful Degradation](artifact/references/graceful-degradation.md) <br>
- [Model Fallback](artifact/references/model-fallback.md) <br>
- [Anti-Stampede Retry Asymmetry](artifact/references/anti-stampede.md) <br>
- [Extended Error Recovery Patterns](artifact/references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell snippets, JSON hook examples, and supporting script files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe recovery log entries, restored session state, cleaned lock files, and additionalContext guidance.] <br>

## Skill Version(s): <br>
2.4.0 (source: server-resolved release metadata; artifact frontmatter and metadata.json list 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

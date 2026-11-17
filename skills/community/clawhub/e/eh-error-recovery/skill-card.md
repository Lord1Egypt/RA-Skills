## Description:

Provides agent recovery patterns for rate limits, crash state, stale sessions, MCP disconnections, tool degradation, model fallback, and anti-stampede retry handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recover long-running agent sessions when rate limits, crashes, stale tmux sessions, MCP disconnects, tool failures, or model failures interrupt work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation can press Enter in tmux panes that are not confirmed agent rate-limit prompts.

Mitigation: Narrow scanning to known agent panes, recapture pane text immediately before sending input, and refuse to act on confirmation or destructive prompts.

Risk: Recovery routines can write session state and delete stale lock files.

Mitigation: Limit recovery paths to intended session directories, log each mutation, and require manual review when lock ownership or session activity is ambiguous.

Risk: Background retry automation can amplify overload or waste resources.

Mitigation: Use short timeouts, avoid retries in async background hooks, and keep foreground retries bounded while honoring Retry-After guidance.

Risk: Fallback tool or model guidance can reduce capability or change task behavior.

Mitigation: Document capability differences for fallback tools, cap reconnect and model-fallback attempts, and report unresolved failures to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/eh-error-recovery)
- [Rate Limit Recovery](references/rate-limit.md)
- [Crash Recovery](references/crash-recovery.md)
- [Stale Session Daemon](references/stale-session.md)
- [MCP Reconnection](references/mcp-reconnection.md)
- [Graceful Degradation](references/graceful-degradation.md)
- [Model Fallback Advisory](references/model-fallback.md)
- [Anti-Stampede Retry Asymmetry](references/anti-stampede.md)
- [Extended Recovery Patterns](references/extended-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce recovery log entries, restored state descriptions, and lock-cleanup actions when implemented through hooks or scripts.]

## Skill Version(s):

2.4.0 (source: server release metadata; artifact frontmatter and metadata declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

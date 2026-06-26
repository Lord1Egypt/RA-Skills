## Description: <br>
Agent Hooks provides drop-in Claude Code hook scripts that intervene when agents stop early, repeat failing tool calls, complete with speculative language, or need immediate post-edit diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add local Claude Code hooks for persistent execution, tool retry escalation, speculative-completion checks, and edit-time diagnostics in agent coding sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local hooks can actively steer Claude Code behavior and may block completion when Stop hooks are enabled. <br>
Mitigation: Enable only the hooks needed for the workflow, review the scripts before installation, and test with a temporary HOME or session before using them in important repositories. <br>
Risk: Async diagnostics can run local developer tools after file edits and may surface tool output back into the agent session. <br>
Mitigation: Use the diagnostics hook only in repositories where running local linters, type checkers, or build tools is expected, and verify those tools are installed and appropriate for the project. <br>
Risk: A persistent execution loop can keep an agent working longer than intended if configured with an excessive iteration limit. <br>
Mitigation: Set bounded max iterations, use the cancel hook when needed, and rely on the built-in idle timeout, cancel signal, authentication-error, and max-iteration safety checks. <br>


## Reference(s): <br>
- [Pattern 1: Persistent Execution Loop (Ralph Mode)](references/01-ralph.md) <br>
- [Pattern 3: Tool Error Retry Escalation](references/03-tool-error.md) <br>
- [Pattern 7: Cancel Signal with TTL](references/07-cancel-ttl.md) <br>
- [Pattern 13: Doubt Gate](references/13-doubt-gate.md) <br>
- [Pattern 15: Post-Edit Diagnostics](references/15-post-edit-diagnostics.md) <br>
- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks) <br>
- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) <br>
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local hook scripts that emit JSON hook decisions or additional context when configured in Claude Code.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

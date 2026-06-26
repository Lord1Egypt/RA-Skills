## Description: <br>
Delegates coding tasks to Claude Code CLI, captures the result, and reports it back in chat with support for continued sessions in the same workdir. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xManel](https://clawhub.ai/user/0xManel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to delegate code analysis, file edits, test writing, troubleshooting, and follow-up coding tasks to Claude Code from an OpenClaw chat. It is suited for workflows where the agent should run Claude synchronously and summarize the captured result back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated Claude Code sessions run with permission checks bypassed and can broadly edit files or run commands in the selected project. <br>
Mitigation: Install only in trusted repositories, review the helper script before use, and prefer removing `--permission-mode bypassPermissions` unless bypassed permissions are intentionally required. <br>
Risk: Persistent `--continue` sessions reuse prior workdir context, so a follow-up request can act on earlier files, edits, and conversation history. <br>
Mitigation: Use a new session for unrelated tasks or different projects, and confirm the intended workdir before delegating follow-up work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xManel/ask-claude-skill) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown chat response summarizing captured Claude Code CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include files created or edited, captured errors, suggested fixes, and summarized long output with full output available on request.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence; artifact package metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

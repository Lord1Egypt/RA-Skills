## Description: <br>
Delegates coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-backed bash sessions and background process monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickchan0412](https://clawhub.ai/user/nickchan0412) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate larger coding, code review, refactoring, and iterative implementation tasks to installed coding-agent CLIs while monitoring long-running sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runnable artifact can send prompts, code, or other entered text to Google/Gemini using an embedded API key. <br>
Mitigation: Remove or rotate the embedded key, use approved credentials, and avoid entering secrets or private code unless that data transfer is acceptable. <br>
Risk: The skill includes high-authority autonomous agent examples such as unsandboxed or auto-approved execution modes. <br>
Mitigation: Prefer constrained approval modes, use disposable clones or worktrees, and manually review diffs before any commit, push, pull request, or GitHub comment. <br>
Risk: Delegated coding agents may produce incorrect code, shell commands, or review guidance. <br>
Mitigation: Inspect generated output, run relevant tests, and verify file changes before applying or publishing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickchan0412/coding-agent-backup) <br>
- [Gemini generateContent API endpoint used by artifact](https://generativelanguage.googleapis.com/v1/models/gemini-3.1-pro:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; the runnable JavaScript artifact returns generated code or short explanatory text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PTY-capable bash tooling and installed agent CLIs; generated code may depend on a remote model response when using artifact/index.js.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

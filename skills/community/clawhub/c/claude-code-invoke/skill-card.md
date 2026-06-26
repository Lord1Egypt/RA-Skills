## Description: <br>
Invokes Claude Code through `claude -p` for single-prompt tasks in a Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user asks to run a single Claude Code prompt against a local Git repository for analysis, code review, or data-query tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to invoking Claude Code with `--dangerously-skip-permissions`, which can bypass normal local permission prompts. <br>
Mitigation: Use only in trusted repositories with reviewed prompts, prefer removing `--dangerously-skip-permissions`, and keep normal permission prompts enabled when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gold3bear/claude-code-invoke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `claude` binary and a target Git repository; examples use PowerShell and recommend timeouts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

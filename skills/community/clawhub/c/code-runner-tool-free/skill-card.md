## Description:

代码执行工具免费版 runs programming tasks in non-interactive environments through a PTY, with automatic prompt responses and file synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to run code review, refactoring, feature implementation, debugging, testing, and deployment tasks through an agent-controlled code execution workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated command execution and file write-back can modify project files unexpectedly.

Mitigation: Run the skill only in an isolated disposable workspace and review diffs before keeping changes.

Risk: Auto-confirmation and sudo guidance can approve or elevate actions without enough human review.

Mitigation: Avoid sudo/root, use a least-privileged dedicated user, and inspect commands before allowing privileged execution.

Risk: External CLI and API use can expose private source code, prompts, or API keys.

Mitigation: Do not expose sensitive repositories or credentials unless the external CLI and execution environment are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-runner-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with code snippets, shell commands, configuration examples, and execution-result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stdout/stderr-style command output and file-change guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

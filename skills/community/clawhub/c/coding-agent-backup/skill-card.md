## Description:

Delegates coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-backed shell sessions for feature work, PR review, refactoring, and iterative coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickchan0412](https://clawhub.ai/user/nickchan0412)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate larger coding tasks, pull request reviews, refactors, and iterative coding work to local coding-agent CLIs while monitoring PTY sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped runtime sends user prompts to Google Gemini using an embedded API key.

Mitigation: Rotate and remove the exposed key, require user-managed credentials, and avoid entering sensitive prompts until credential handling is corrected.

Risk: The skill examples include unsandboxed agent execution and commit or push workflows.

Mitigation: Use isolated workdirs or worktrees, limit credentials and network access, and require explicit approval before unsandboxed runs or repository publishing.

Risk: Delegated coding agents can modify local files or produce incorrect code without direct review.

Mitigation: Monitor sessions, inspect generated changes, run project tests, and review diffs before applying or merging work.

## Reference(s):

- [Coding Agent Backup ClawHub page](https://clawhub.ai/nickchan0412/skills/coding-agent-backup)
- [Publisher profile](https://clawhub.ai/user/nickchan0412)
- [Gemini Generative Language API endpoint used by runtime](https://generativelanguage.googleapis.com/v1/models/gemini-3.1-pro:generateContent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and runtime-generated text or code responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output depends on installed coding-agent CLIs, PTY-capable shell tooling, and the configured Gemini API request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

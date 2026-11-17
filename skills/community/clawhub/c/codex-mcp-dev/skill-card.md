## Description:

Use the local Codex CLI through mcporter and codex-mcp-server for real coding work in the current project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollywood3](https://clawhub.ai/user/hollywood3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate non-trivial repository work to a local Codex installation through MCP, including feature work, bug fixes, refactors, debugging, tests, and implementation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate real repository work to a local Codex setup, which may modify project files.

Mitigation: Review prompts before full-auto use, set --cwd to the intended project, and inspect diffs and tests after each run.

Risk: Aggressive execution modes can broaden the effect of delegated tasks.

Mitigation: Avoid --yolo or danger-full-access unless explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollywood3/skills/codex-mcp-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed repository changes, command results, test guidance, and review summaries depending on the delegated Codex task.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

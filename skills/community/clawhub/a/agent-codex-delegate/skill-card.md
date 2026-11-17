## Description:

Delegates coding, repository analysis, file edits, test runs, and code review tasks to the local Codex CLI using existing Codex CLI authentication rather than embedded API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to delegate repository analysis, code changes, test debugging, and code review to a locally authenticated Codex CLI. It is intended for trusted local operator setups where Codex is already installed and signed in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can invoke powerful Codex execution modes, including workspace-write and danger-full-access.

Mitigation: Default to read-only for analysis, approve write tasks explicitly, and use danger-full-access only in an isolated environment.

Risk: Caller-provided output and JSON log paths may write outside the intended repository.

Mitigation: Keep all output and log paths inside the target repository and inspect resulting diffs before treating a task as complete.

Risk: Repository contents and supplied context are delegated to the local Codex CLI.

Mitigation: Use the skill only when the local Codex CLI on PATH is trusted and the operator has approved the exact data flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/agent-codex-delegate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text, with optional code blocks and Codex JSONL logs when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a final Markdown response or JSONL event log to caller-provided paths when those options are used.]

## Skill Version(s):

0.1.3 (source: evidence release, SKILL.md frontmatter, clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

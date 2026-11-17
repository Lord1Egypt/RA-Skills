## Description:

Execute codeagent-wrapper for multi-backend AI code tasks. Supports Codex, Claude, Gemini, and OpenCode backends with agent presets, skill injection, file references (@syntax), worktree isolation, parallel execution, and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run codeagent-wrapper for code analysis, refactoring, code generation, and multi-agent orchestration across Codex, Claude, Gemini, and OpenCode backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents defaults that can disable permission and sandbox protections for delegated coding agents.

Mitigation: Review before installing, use it only in repositories and accounts where delegated agents may safely run commands, and prefer CODEAGENT_SKIP_PERMISSIONS=false and CODEX_BYPASS_SANDBOX=false.

Risk: Parallel delegated agents and injected skills or prompts can expand the impact of unsafe commands or untrusted instructions.

Mitigation: Use worktrees for changes, avoid unlimited parallel workers, and do not inject untrusted skills or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/codeagent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe structured JSON output files, progress frames, session IDs, and command-line flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Runs Claude Code tasks in headless mode through a local runner wrapper with model selection, structured output checks, artifact validation, retry/fallback support, and task inspection commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwd0313](https://clawhub.ai/user/zwd0313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run non-interactive Claude Code tasks for coding, review, analysis, report generation, and file-producing workflows that need schema or artifact validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch unattended local Claude Code tasks that write files and run Bash.

Mitigation: Use it only in a dedicated trusted workspace with explicit approval, sandboxing, and validation of expected paths and artifacts.

Risk: The documented bypassPermissions mode can reduce interactive permission checks for unreviewed prompts or repositories.

Mitigation: Avoid bypassPermissions for unreviewed inputs and prefer explicit approval or tighter permission settings unless the workspace and task are trusted.

Risk: A task may claim success while failing to produce required files or structured output.

Mitigation: Use --json-schema-file with --expect-file, --expect-contains, or --expect-glob, and treat validation failures as real task failures.

## Reference(s):

- [Runner Usage Reference](references/runner-usage.md)
- [Task Schema Example](references/task-schema-example.json)
- [Run Task Example Script](scripts/run-task-example.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON schema examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status, logs, result inspection commands, file expectation checks, glob checks, and structured JSON output contracts.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

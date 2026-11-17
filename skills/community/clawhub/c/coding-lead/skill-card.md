## Description:

Coding execution skill for any implementation-focused agent. Current production path is claude-only with simple tasks direct, medium tasks preferring ACP run or direct acpx, and complex tasks handled via existing agent continuity plus context files instead of ACP session persistence. Integrates with qmd and smart-agent-memory when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyound87](https://clawhub.ai/user/beyound87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and implementation-focused agents use this skill to classify coding tasks by complexity, choose direct execution or Claude ACP execution paths, preserve task context on disk, and verify coding work before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented direct acpx fallback can run generated prompt text through a shell command.

Mitigation: Review before installing in sensitive workspaces and change the fallback to use structured arguments with an explicit working directory.

Risk: The skill is designed to let agents edit files, run commands, spawn coding agents, and store project context.

Mitigation: Review and scan the skill before deployment, restrict use to intended workspaces, and verify the working directory before writes or spawns.

## Reference(s):

- [Prompt Templates & Examples](references/prompt-templates.md)
- [Complex Tasks - Roles, QA Isolation, Parallel Strategies](references/complex-tasks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or update project context files and implementation prompts.]

## Skill Version(s):

3.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

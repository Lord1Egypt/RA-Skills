## Description:

Builtin Tools provides 16 dependency-free Python scripts that give agents cross-platform file, content search, web, runtime installation, memory, scheduling, and task-management utilities when host tools are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a basic local toolbox when the host agent platform lacks file, search, web, install, memory, scheduling, or task-management tools. It is best suited for trusted workspaces where broad tool access is intentional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad local toolbox powers across shell execution, filesystem changes, network access, runtime installation, memory, and scheduled-task configuration.

Mitigation: Install only in trusted workspaces where this access is intentional, and prefer host-provided tools with approval controls when available.

Risk: Delete, install, shell, network, memory, and automation actions can have lasting local effects.

Mitigation: Review every such action before it runs, avoid custom API endpoints with real keys, and do not create scheduled tasks from untrusted prompts.

## Reference(s):

- [builtin-tools interface protocol](artifact/references/protocol.md)
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/builtin-tools)
- [ClawHub publisher profile](https://clawhub.ai/user/wangjiaocheng)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON script results, text, shell command output, file changes, and configuration records depending on the selected tool.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts use JSON input and JSON status responses; some tools can modify files, access the network, install runtimes, or create scheduled-task configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

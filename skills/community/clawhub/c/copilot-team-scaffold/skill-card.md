## Description:

Initializes a multi-agent AI development framework that scaffolds agent roles, hooks, instructions, prompts, planning files, spec-flow directories, and memory templates for a new project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrh07819](https://clawhub.ai/user/lrh07819)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when starting a project to scaffold a structured AI-assisted workflow with specialized agents, automated hooks, planning files, and task execution prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic hooks can read prior session transcripts and inject recovered or local context into future agent sessions.

Mitigation: Review the installed hooks before enabling them and remove transcript catchup or context injection where project privacy rules do not allow it.

Risk: Global memory creation can affect future projects beyond the repository where the scaffold is installed.

Mitigation: Approve global memory files manually and limit them to non-sensitive workflow rules.

Risk: Validation hooks and AGENTS.md lifecycle gates can block or redirect normal development workflows.

Mitigation: Install the scaffold in a test branch first, audit the hook configuration, and tune or disable gates that do not match the team's workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrh07819/skills/copilot-team-scaffold)
- [Visual Studio Code Copilot hooks documentation](https://code.visualstudio.com/docs/copilot/customization/hooks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files, hook configurations, scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a project scaffold under .github/, docs/sessions/, .spec-flow/, and optional memory files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

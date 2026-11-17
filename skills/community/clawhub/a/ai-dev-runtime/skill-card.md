## Description:

AI Dev Runtime tools for reading, searching, editing, running terminal commands, running tests, and using hybrid semantic and keyword search with learning memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammytan](https://clawhub.ai/user/sammytan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to delegate coding tasks to an AI Dev Runtime server, including repository analysis, file edits, test runs, terminal operations, and bug-fix workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected runtime can edit code and run terminal commands.

Mitigation: Review tasks before invoking edit, batch, bug-fix, terminal, or test workflows, and operate the skill only against repositories where those actions are intended.

Risk: The skill depends on a trusted AI Dev Runtime server and may use configured API keys or development memory.

Mitigation: Connect only to a server you trust, protect AI_DEV_RUNTIME_API_KEY, and avoid passing sensitive memory unless it is needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sammytan/skills/ai-dev-runtime)
- [AI Dev Runtime homepage](https://github.com/your-org/AiDevRuntime)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with code, command, and configuration snippets when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AI_DEV_RUNTIME_URL, optional AI_DEV_RUNTIME_API_KEY, and prior memory snippets supplied by the invoking agent.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

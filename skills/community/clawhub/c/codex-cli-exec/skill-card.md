## Description:

Explain how Openclaw should use Codex CLI as a non-interactive coding engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minchocoin](https://clawhub.ai/user/minchocoin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give concise, command-focused guidance for installing, authenticating, configuring, and running Codex CLI through Openclaw with non-interactive `codex exec` workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or login credentials could be exposed or mishandled when configuring Codex CLI authentication.

Mitigation: Use dedicated workspaces, avoid sharing credentials in prompts or files, and handle `OPENAI_API_KEY` only through appropriate environment-variable workflows.

Risk: Automation settings such as broad additional directories, `--full-auto`, or unsafe sandbox choices could modify unintended files or spend account quota.

Mitigation: Prefer workspace-limited execution, narrow allowed directories, explicit approvals when unsure, and avoid bypassing approvals or sandboxing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for Codex CLI and Openclaw usage.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

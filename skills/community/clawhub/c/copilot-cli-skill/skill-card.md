## Description:

Run GitHub Copilot CLI from OpenClaw for coding tasks in a target project directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwxf](https://clawhub.ai/user/cecwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an OpenClaw agent run GitHub Copilot CLI for implementation, debugging, refactoring, code review, and GitHub-oriented coding workflows in a target repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant Copilot broad autonomous tool access inside a repository.

Mitigation: Prefer explicit --allow-tool permissions and avoid --allow-all-tools unless the workspace is disposable or tightly scoped.

Risk: Background Copilot sessions may continue acting without immediate user attention.

Mitigation: Monitor background sessions through process logs and stop sessions that ask for unexpected input or exceed the intended scope.

Risk: GitHub tokens or repository credentials could be exposed through project files or prompts.

Mitigation: Use least-privilege GitHub tokens and do not store tokens in project files or prompts.

## Reference(s):

- [Copilot CLI documentation summary](references/copilot-doc-summary.md)
- [Copilot CLI usage recipes](references/copilot-usage-recipes.md)
- [About GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli)
- [Install GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- [Use GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub Copilot CLI availability, authentication, and an explicit target repository workdir.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

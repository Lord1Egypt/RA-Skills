## Description:

Configure Claude Code to use OpenAI-compatible custom model providers through a local Anthropic-to-OpenAI API proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-heartflow](https://clawhub.ai/user/mark-heartflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Claude Code with non-Anthropic or OpenAI-compatible model providers, including setting up a local proxy and troubleshooting model validation, streaming, and connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships with a hardcoded third-party upstream endpoint and API key.

Mitigation: Replace the upstream host, model, and credential with trusted configuration before use, and revoke the embedded key if you control it.

Risk: The proxy logs request bodies, which can expose prompts or project content.

Mitigation: Remove or sanitize prompt-body logging before using the skill with confidential work.

Risk: Claude Code traffic can be redirected through persistent local settings.

Mitigation: Prefer temporary environment variables, review Claude Code settings before use, and restrict local proxy access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mark-heartflow/skills/claude-code-custom-model-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on configuring and running a local Python proxy for Claude Code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

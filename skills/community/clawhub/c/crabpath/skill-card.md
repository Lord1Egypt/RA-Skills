## Description:

Memory graph engine with caller-provided embed and LLM callbacks; core is pure, with real-time correction flow and optional OpenAI integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathangu](https://clawhub.ai/user/jonathangu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use CrabPath to build and maintain a local learned retrieval graph over selected workspace files, query it for focused context, and apply feedback or corrections so future retrieval routes improve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace indexing and rebuild flows can expose or overwrite more local data than expected when paths are not tightly controlled.

Mitigation: Use trusted, non-shared workspace directories, avoid indexing untrusted repositories or symlinks, and keep path scope explicit.

Risk: Optional OpenAI embedding or LLM callbacks can transmit indexed text outside the local environment.

Mitigation: Use hash/offline mode for sensitive data, and enable external callbacks only for content that is acceptable to send to the selected provider.

Risk: OpenClaw rebuild scripts may be unsafe to run with elevated privileges until path containment and private cache handling are fixed.

Mitigation: Run rebuild workflows as an unprivileged user and defer privileged deployment until those issues are remediated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jonathangu/skills/crabpath)
- [CrabPath Paper and Results](https://jonathangu.com/crabpath/)
- [CrabPath Architecture](docs/architecture.md)
- [CrabPath Operator Setup Guide](docs/setup-guide.md)
- [REPRODUCE.md](REPRODUCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime workflows may also produce text, JSON responses, and state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.10; supports offline hash embeddings and optional provider callbacks for embeddings or LLM routing.]

## Skill Version(s):

11.2.1 (source: pyproject.toml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

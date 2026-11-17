## Description:

Detect hardcoded secrets such as API keys, tokens, and passwords in text or code using Expanso Edge pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to scan code, configuration, logs, diffs, or HTTP-submitted text for hardcoded credentials during pre-commit, CI/CD, code review, and security audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive scan input may be sent to OpenAI.

Mitigation: Use only approved data, and do not scan production secrets, private code, logs, or regulated data unless the organization explicitly permits sending that content to OpenAI.

Risk: MCP mode exposes an unauthenticated network service.

Mitigation: Bind the service to localhost or place it behind authentication, rate limits, and network controls before use.

Risk: The advertised local or no-key backend is not implemented in the inspected pipelines.

Mitigation: Treat the OpenAI-backed behavior as the operative behavior unless new release evidence proves otherwise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-secrets-scan)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [skill.yaml](skill.yaml)
- [pipeline-cli.yaml](pipeline-cli.yaml)
- [pipeline-mcp.yaml](pipeline-mcp.yaml)
- [Expanso](https://expanso.io)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON object with findings, has_secrets, summary, and metadata fields; usage examples are shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings may include secret type, redacted value, line number, severity, context, and audit metadata.]

## Skill Version(s):

1.0.0 (source: skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

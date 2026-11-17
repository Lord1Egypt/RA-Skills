## Description:

Get China A-share market data (Shanghai/SH and Shenzhen/SZ) via FinanceAgent on OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query China A-share quote data for Shanghai and Shenzhen symbols through FinanceAgent on OneKey Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned npm gateway package.

Mitigation: Install only if the @aiagenta2z/onekey-gateway package and DeepNLP OneKey Gateway service are trusted, and pin or verify the package version where possible.

Risk: Credential-handling examples could expose the OneKey Gateway API key in logs or terminal output.

Mitigation: Avoid running verbose curl examples with a real key, avoid global installation where possible, and rotate the key if it appears in logs or terminal output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/cn-stock-market-shanghai-shenzhen)
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a OneKey Gateway API key and returns stock quote data from the upstream service as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

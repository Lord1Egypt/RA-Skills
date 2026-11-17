## Description:

Smart proxy for external API calls with retry, caching, rate limiting, and fallback providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route outbound API requests through a local gateway with retries, caching, rate-limit tracking, fallback providers, and API key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive request bodies may be persisted in cache keys despite metadata-only cache claims.

Mitigation: Avoid sending secrets or regulated data in request bodies, clear cache after sensitive work, and treat memory/api-gateway as sensitive local storage.

Risk: Plaintext API keys can be stored on disk in keys.json.

Mitigation: Prefer scoped PROVIDER_API_KEY environment variables or a secrets manager, and only use disk-stored keys in workspaces with appropriate local access controls.

Risk: Requests transmit URLs, headers, bodies, and prompts to external provider endpoints selected by the user.

Mitigation: Use only trusted provider endpoints, review allowlists before adding keys, and use dry-run mode before important calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/api-proxy)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)
- [ClawHub manifest](artifact/clawhub.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute outbound HTTPS requests and write local gateway state when invoked by an agent.]

## Skill Version(s):

1.1.8 (source: server release evidence and artifact/clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

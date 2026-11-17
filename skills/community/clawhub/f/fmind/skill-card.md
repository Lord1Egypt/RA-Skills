## Description:

Use FMind as a unified knowledge and external-memory gateway for tenant knowledge-base search and L0-L2 memory, context, and published Memory Wiki access through an Agent Binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure FMind-backed agents that can search authorized knowledge bases and use FMind memory gateway operations without exposing credentials or bypassing server-side authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access FMind knowledge and memory services using configured credentials.

Mitigation: Install only for trusted FMind deployments and provide least-privilege user keys and Agent Binding keys scoped to the intended knowledge bases and memory assets.

Risk: API keys or setup prompts could be exposed if pasted into chat, logs, URLs, source control, or saved files.

Mitigation: Keep credentials in environment variables or a secret manager, never paste them into prompts, and avoid printing response headers, setup prompts, API keys, runtime keys, or signed tokens.

Risk: Knowledge-base mutations could affect the wrong resource if identifiers are guessed or taken from untrusted prompt text.

Mitigation: Select knowledge bases explicitly, respect authorization failures, and require user confirmation before destructive operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justaboyhai-wq/skills/fmind)
- [ClawHub Publisher Profile](https://clawhub.ai/user/justaboyhai-wq)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell, JSON, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FMIND_BASE_URL and FMIND_USER_API_KEY; optionally uses FMIND_AGENT_RUNTIME_KEY and FMIND_AGENT_SETUP_KEY for Agent Binding setup and memory access.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

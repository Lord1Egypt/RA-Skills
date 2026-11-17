## Description:

Enable and configure Moltbot/Clawdbot memory search for persistent context, including MEMORY.md, daily logs, configuration options, and vector search setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up persistent memory search for Moltbot/Clawdbot, configure memory sources and embedding providers, and troubleshoot memory recall behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing long-term memory and past chat transcripts with a remote embedding provider can expose confidential, regulated, personal, or customer data.

Mitigation: Prefer the local provider or memory-only indexing for sensitive work, avoid storing secrets or unnecessary private details in MEMORY.md or logs, and confirm the embedding provider's retention and deletion terms before enabling session indexing.

Risk: Embedding provider API keys may be mishandled during setup.

Mitigation: Store provider keys in a secure environment and avoid writing them into memory files, logs, or shared configuration examples.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration examples, markdown templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes memory directory conventions, provider options, environment variable names, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

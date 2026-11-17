## Description:

Fetches configurable RSS and Atom feeds, deduplicates articles by URL and topic, optionally scores articles with an OpenAI-compatible LLM, and dispatches digests to configured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to gather recent RSS and Atom articles, remove already-seen or duplicate topics, prepare agent-readable digests, and send them to configured notification or storage channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM scoring can send feed-derived article text and an API key to the configured OpenAI-compatible endpoint.

Mitigation: Keep scoring disabled unless needed, store the API key in a dedicated secret file, verify file permissions, and use only trusted HTTPS LLM endpoints.

Risk: Configured outputs or cron can dispatch digests without further user interaction.

Mitigation: Review the configuration before enabling outputs or cron, disable unused outputs, and audit dispatch logs for enabled channels.

Risk: RSS source configuration causes network requests from the user's machine to configured feed URLs.

Mitigation: Only add RSS sources that are trusted for the deployment environment and review custom source files before running fetch jobs.

Risk: SMTP fallback can place mail credentials in the output configuration.

Mitigation: Prefer delegated mail-client handling where possible and avoid storing SMTP passwords in the general skill configuration.

## Reference(s):

- [Fox Veille on ClawHub](https://clawhub.ai/qinthqod/skills/fox-veille)
- [OpenClaw](https://openclaw.ai)
- [Troubleshooting](references/troubleshooting.md)
- [Cron prompt template](references/cron_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON digests, wrapped untrusted-content listings, Markdown or text dispatch payloads, and setup or CLI guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch output includes article metadata, count and skip totals, and an untrusted-content wrapper; optional scoring adds scores, reasons, and ghost picks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

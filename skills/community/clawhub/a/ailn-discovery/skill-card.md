## Description:

Discover AILN tool capabilities through public HTTP endpoints and run an optional sponsored search demonstration without a wallet, API key, signature, or visitor payment. Use for service discovery and response validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numerous4311-design](https://clawhub.ai/user/numerous4311-design)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agents use this skill to inspect AILN's public tool schemas and, when requested, run a sponsored search for a public topic. It helps summarize returned results, sources, and service status while respecting payment and privacy limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topics are sent to ailn.ai and could expose personal or confidential information.

Mitigation: Use public, non-sensitive topics only.

Risk: A remote service response may request payment or fail because sponsorship is unavailable or rate-limited.

Mitigation: Stop if payment, signing, or credentials are requested; report rate limits or unavailable sponsorship without retrying or switching to a paid call.

## Reference(s):

- [AILN service discovery endpoint](https://ailn.ai/mcp)
- [AILN sponsored search endpoint](https://ailn.ai/demo/search)
- [Official AILN skill instructions](https://ailn.ai/SKILL.md)
- [AILN Discovery on ClawHub](https://clawhub.ai/numerous4311-design/skills/ailn-discovery)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API requests and responses with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned sources and status when available; sponsored searches are limited to public topics.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

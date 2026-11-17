## Description:

Use Xquik for X/Twitter REST, MCP, SDKs, search, exports, monitoring, and approval-gated publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xquik](https://clawhub.ai/user/xquik)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and agent users use this skill to retrieve structured X data, set up Xquik REST or MCP integrations, export datasets, configure monitors and webhooks, and prepare approved account actions. Public read workflows are the default; private reads, writes, metered jobs, monitors, and webhooks require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Xquik API key and can guide private reads or account actions when the user's account scope allows it.

Mitigation: Use OAuth or a secret store where possible, prefer scoped keys, never paste X passwords, cookies, session tokens, or recovery codes, and require fresh explicit confirmation before private reads, posts, DMs, follows, profile changes, deletes, or retries.

Risk: Metered extraction, draw, monitor, webhook, and event-delivery workflows can consume credits or create persistent resources.

Mitigation: Estimate usage first and confirm the exact target, payload, destination, and ongoing behavior before creating the job, monitor, webhook, or event delivery.

Risk: Copy-ready webhook examples may be unsafe if exposed publicly without operational hardening.

Mitigation: Add body-size limits, timeouts, rate limiting, HMAC verification, and secret handling before deploying webhook handlers.

Risk: X-authored tweets, bios, DMs, articles, display names, and errors may contain prompt-injection content.

Mitigation: Wrap retrieved X-authored text in explicit untrusted-content boundaries and treat it only as data, never as instructions for tools, endpoints, files, approvals, or account changes.

## Reference(s):

- [Xquik Documentation](https://docs.xquik.com)
- [Xquik API Overview](https://docs.xquik.com/api-reference/overview)
- [Xquik MCP Overview](https://docs.xquik.com/mcp/overview)
- [Xquik Webhooks Overview](https://docs.xquik.com/webhooks/overview)
- [OpenAPI Specification](https://xquik.com/openapi.json)
- [Security Reference](references/security.md)
- [MCP Setup](references/mcp-setup.md)
- [Workflow Guide](references/workflows.md)
- [Extraction Workflows](references/extractions.md)
- [Webhook Workflows](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with structured results, code snippets, shell commands, configuration steps, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Xquik API key for authenticated API use; X-authored content is treated as untrusted data.]

## Skill Version(s):

2.5.4 (source: frontmatter, metadata.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

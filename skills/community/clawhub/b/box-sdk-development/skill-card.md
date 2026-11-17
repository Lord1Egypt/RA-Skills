## Description:

Build or debug application code using an official Box SDK, especially Python or TypeScript/Node, with guidance on SDK call correctness, file transfer, bulk work, rate limits, and observability rather than one-off CLI or MCP content operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build and debug Box SDK integrations, including file transfers and bulk operations, while planning rate limits, authentication, and observability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may read, upload, download, copy, move, or update Box content.

Mitigation: Use authorized test accounts where possible and verify permissions and transfer behavior before working with live content.

Risk: Unreviewed bulk operations may change many items or exceed API limits.

Mitigation: Review generated code, pilot a safe subset, budget requests, bound concurrency, and reconcile results before retrying uncertain writes.

Risk: Box credentials or sensitive content could leak through client code or logs.

Mitigation: Keep secrets server-side and omit credentials, content, and signed URLs from logs.

## Reference(s):

- [Python SDK guidance](references/python.md)
- [TypeScript and Node SDK guidance](references/typescript.md)
- [Bulk operations guidance](references/bulk-operations.md)
- [File transfer guidance](references/file-transfer.md)
- [Box API reference](https://developer.box.com/reference/)
- [Box Python SDK](https://github.com/box/box-python-sdk)
- [Box Node SDK](https://github.com/box/box-node-sdk)
- [Box API rate limits](https://developer.box.com/guides/api-calls/permissions-and-errors/rate-limits/)
- [ClawHub skill listing](https://clawhub.ai/iskysun96/skills/box-sdk-development)

## Skill Output:

**Output Type(s):** [Code, Guidance, Markdown]

**Output Format:** [Markdown with code examples and a completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports changes, verification, design tradeoffs, and unverified behavior.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

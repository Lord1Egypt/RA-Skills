## Description:

Manage Cloudflare Workers, Pages, KV, D1, R2, and secrets using the Wrangler CLI and direct Cloudflare API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itamarcoh3n](https://clawhub.ai/user/itamarcoh3n)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to deploy and operate Cloudflare Workers, Pages, KV, D1, R2, queues, secrets, and related configuration. It provides command and API examples for setup, deployment, storage, database, domain, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudflare API tokens and R2 credentials could be exposed, printed, logged, or granted broader permissions than needed.

Mitigation: Use least-privilege Cloudflare tokens, keep secrets out of logs and chat output, and verify token scope before running commands.

Risk: Commands in the skill can delete, roll back, or materially change Cloudflare Workers, Pages projects, KV namespaces, D1 databases, R2 buckets, queues, lifecycle rules, domains, and production deployments.

Mitigation: Require explicit user confirmation before deletes, rollbacks, lifecycle changes, domain changes, or production deployments.

Risk: Example account IDs, bucket names, and deployment targets may not match the user's Cloudflare environment.

Mitigation: Replace hard-coded examples with verified user-specific account IDs, bucket names, project names, and resource identifiers before execution.

Risk: Wrangler behavior and authentication requirements can vary by version and token scope.

Mitigation: Pin the Wrangler version where reproducibility matters and verify authentication with `wrangler whoami` before making changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itamarcoh3n/skills/cloudflare-wrangler)
- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with inline bash, JSON, TOML, JavaScript, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-specific Cloudflare account IDs, tokens, project names, bucket names, and confirmation before production-impacting actions.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

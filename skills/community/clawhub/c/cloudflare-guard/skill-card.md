## Description:

Configures and manages Cloudflare DNS, caching, security rules, rate limiting, and Workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to plan, apply, and verify Cloudflare DNS, SSL/TLS, caching, rate limiting, and edge security changes for web applications, especially Vercel-backed sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses powerful Cloudflare credentials that can change DNS, SSL/TLS, caching, rate limiting, and security settings for a zone.

Mitigation: Use narrowly scoped Cloudflare API tokens, review the proposed plan before execution, and verify each change after one sequential API call.

Risk: Broad preflight reads can expose more Cloudflare zone configuration than a narrow task requires.

Mitigation: Ask the agent to query only the records and settings needed for the specific task.

Risk: The optional npx json fallback may introduce unnecessary package-execution risk.

Mitigation: Prefer jq, python3 -m json.tool, or PowerShell ConvertFrom-Json, and avoid the npx json fallback.

## Reference(s):

- [Cloudflare Guard on ClawHub](https://clawhub.ai/guifav/skills/cloudflare-guard)
- [Cloudflare API v4 endpoint](https://api.cloudflare.com/client/v4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans changes before execution, performs sequential API calls, and summarizes resulting Cloudflare state.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

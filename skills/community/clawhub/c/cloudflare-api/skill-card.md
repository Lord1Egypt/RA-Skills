## Description:

Connect to Cloudflare API for DNS management, tunnels, and zone administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucassynnott](https://clawhub.ai/user/lucassynnott)

### License/Terms of Use:


## Use Case:

Developers, operators, and site administrators use this skill to manage Cloudflare zones, DNS records, and tunnels from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Cloudflare DNS records and tunnel resources.

Mitigation: Use a narrowly scoped Cloudflare API token and verify zone names, DNS record names, tunnel names, and IDs before create, update, or delete commands.

Risk: The skill handles Cloudflare API tokens and can print tunnel run tokens to standard output.

Mitigation: Store tokens with restrictive permissions, avoid token-printing commands in CI or transcript-recorded sessions, and rotate any exposed tokens.

## Reference(s):

- [Cloudflare](https://cloudflare.com)
- [Cloudflare API token dashboard](https://dash.cloudflare.com/profile/api-tokens)
- [Cloudflare API endpoint](https://api.cloudflare.com/client/v4)
- [ClawHub skill page](https://clawhub.ai/lucassynnott/skills/cloudflare-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports table, quiet, and raw JSON command output; requires curl and jq.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

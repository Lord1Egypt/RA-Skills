## Description:

3-layer site launcher: tunnel any HTML instantly, deploy to Cloudflare Pages permanently, then buy a domain and link it via DNS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wohaoshuai](https://clawhub.ai/user/wohaoshuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to expose a local HTML page or server through a temporary Cloudflare tunnel, deploy static content to Cloudflare Pages, and connect a purchased custom domain through DNS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requests an unrelated NETA_TOKEN credential that is not needed for the Cloudflare publishing workflow.

Mitigation: Remove the NETA_TOKEN requirement before release and do not provide unrelated credentials during installation or use.

Risk: Cloudflare tokens may be exposed if pasted into command lines, logs, terminal history, or chat transcripts.

Mitigation: Use least-privilege Cloudflare tokens, prefer environment variables or a secret manager, and rotate any token that may have been exposed.

Risk: Tunnel and deployment commands can make local directories or sites public.

Mitigation: Confirm the exact directory, project, domain, and DNS change before execution, and publish only content intended for public access.

Risk: Deployment, package fetching, and system installation paths require review before use with real Cloudflare credentials.

Mitigation: Pin or bundle required tooling where possible, review command construction before deployment, and test with limited-scope credentials first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wohaoshuai/skills/buy-domain-helper)
- [Publisher profile](https://clawhub.ai/user/wohaoshuai)
- [Project homepage](https://github.com/wohaoshuai/buy-domain-helper)
- [Cloudflare API tokens](https://dash.cloudflare.com/profile/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Cloudflare tunnel URLs, Pages deployment URLs, domain status checks, DNS configuration steps, and command-line instructions.]

## Skill Version(s):

1.5.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

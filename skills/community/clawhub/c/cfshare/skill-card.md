## Description:

Use the cfshare CLI to expose local ports and files as temporary Cloudflare Quick Tunnel URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ystemsrx](https://clawhub.ai/user/ystemsrx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs to create a temporary public URL for a local service, share selected local files or directories, or inspect cfshare audit and policy state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish local services or files to the internet through temporary public tunnel URLs.

Mitigation: Use it only for content intended to be externally reachable, review the exact port or files first, and prefer token or basic access over unauthenticated access.

Risk: The documented setup includes system-level installation steps for network-downloaded tools.

Mitigation: Install cfshare and cloudflared from trusted, pinned, verified sources before agent use instead of allowing automatic sudo or global install steps.

## Reference(s):

- [CF Share skill page](https://clawhub.ai/ystemsrx/skills/cfshare)
- [cloudflared Linux binary download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64)
- [Cloudflare package signing key](https://pkg.cloudflare.com/cloudflare-main.gpg)
- [Cloudflare cloudflared package repository](https://pkg.cloudflare.com/cloudflared)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public_url and expires_at for created exposures; credentials are masked in CLI output.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

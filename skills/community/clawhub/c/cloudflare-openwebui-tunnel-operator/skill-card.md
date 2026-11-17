## Description:

Create and maintain a Cloudflare Tunnel for Open WebUI using a 1Password-managed API token, Docker runtime, and optional systemd persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grey0758](https://clawhub.ai/user/grey0758)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when local Open WebUI is already running and needs a stable public HTTPS hostname through Cloudflare Tunnel. It guides use of a 1Password-managed Cloudflare API token, Docker-based cloudflared runtime, DNS setup, verification checks, and optional systemd persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles persistent Cloudflare and 1Password credentials.

Mitigation: Use a narrowly scoped Cloudflare API token, a dedicated 1Password service account, and owner-only permissions for runtime env files kept out of source control and backups.

Risk: The workflow can change DNS records, tunnels, systemd services, and 1Password metadata.

Mitigation: Require explicit confirmation before account, DNS, tunnel, systemd, or 1Password changes, and verify local and public URLs after each change.

Risk: Machine-specific tokens or raw transcripts could expose sensitive deployment details.

Mitigation: Do not publish secrets, runtime env files, machine-specific tokens, or raw command transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/grey0758/skills/cloudflare-openwebui-tunnel-operator)
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub)
- [README](artifact/README.md)
- [Workflow](artifact/WORKFLOW.md)
- [FAQ](artifact/FAQ.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and ordered workflow status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to include current workflow status, missing artifacts, the next single best action, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

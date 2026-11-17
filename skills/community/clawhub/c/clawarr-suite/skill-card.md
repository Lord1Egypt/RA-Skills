## Description:

Comprehensive management for self-hosted media stacks including Sonarr, Radarr, Lidarr, Readarr, Prowlarr, Bazarr, Overseerr, Plex, Tautulli, SABnzbd, companion services, dashboard generation, and media tracker integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omiron33](https://clawhub.ai/user/omiron33)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators use this skill to let an agent inspect, configure, and operate self-hosted media automation stacks across local services, companion containers, request workflows, dashboards, and media tracker sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent operational control over media-stack services through powerful service keys.

Mitigation: Use least-privilege service keys where possible and review agent actions before approving changes to libraries, requests, or service configuration.

Risk: Local browser storage or shared browser origins can expose pasted service secrets.

Mitigation: Avoid pasting secrets into the browser UI on shared origins and prefer environment variables or user-owned configuration files.

Risk: Package installation and companion-service commands can affect the host environment.

Mitigation: Avoid the sudo curl installer unless reviewed, avoid unpinned pip installs unless trusted, and review Docker or SSH environment values before running companion-service commands.

Risk: Network operations target local LAN and user-configured hosts that may expose unsecured media services.

Mitigation: Prefer HTTPS or a trusted management LAN and verify hostnames, ports, and API keys before running setup or management commands.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/omiron33/skills/clawarr-suite)
- [API Endpoints Reference](references/api-endpoints.md)
- [Setup Guide](references/setup-guide.md)
- [Common Issues & Troubleshooting](references/common-issues.md)
- [Companion Services Reference](references/companion-services.md)
- [Media Tracker API Reference](references/tracker-apis.md)
- [Traktarr & Retraktarr Guide](references/traktarr-retraktarr.md)
- [Suggested Agent Prompts](references/prompts.md)
- [Dashboard Templates](references/dashboard-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands, configuration snippets, JSON, CSV, and generated HTML dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reflect user-configured local media services and can include operational status, library analytics, request decisions, sync commands, and dashboard files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

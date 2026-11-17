## Description:

Manage a Jellyfin/Plex and *Arr media server stack by checking status, adding content, monitoring downloads, diagnosing issues, and restarting services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxtechera](https://clawhub.ai/user/maxtechera)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-hosting operators use Admirarr to inspect, troubleshoot, and manage Jellyfin or Plex media stacks with Radarr, Sonarr, Prowlarr, qBittorrent, and related services. The skill helps agents present status, health, library, download, indexer, setup, migration, and service-management workflows in a user-facing way.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path runs a remote script from the Admirarr distribution endpoint with the user's privileges.

Mitigation: Install only from a trusted endpoint, prefer version-pinned downloads with checksums or signatures, inspect the installer before running it, and avoid running it as root unless the publisher documents why elevation is required.

Risk: The skill can guide service restarts and other operational actions against a self-hosted media stack.

Mitigation: Confirm with the user before restarts or destructive actions, and do not delete user files or media.

## Reference(s):

- [ClawHub Admirarr Skill Page](https://clawhub.ai/maxtechera/skills/admirarr)
- [Admirarr Installer Endpoint](https://get.admirarr.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and structured operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI commonly supports JSON output for agent parsing; destructive actions and restarts require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

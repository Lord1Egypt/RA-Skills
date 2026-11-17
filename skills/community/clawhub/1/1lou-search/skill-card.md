## Description:

Searches 1lou for movie or TV resources, presents filtered results, retrieves a selected torrent, and adds it to a Synology-hosted qBittorrent instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluepop1991-cloud](https://clawhub.ai/user/bluepop1991-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users trigger the skill with a Chinese media-search command to manually find a movie or TV resource on 1lou, choose a result, and send the selected torrent to a configured qBittorrent downloader.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes qBittorrent credentials.

Mitigation: Rotate the exposed password and require user-supplied secrets instead of embedded credentials.

Risk: The skill uses plaintext HTTP to control a NAS downloader.

Mitigation: Use HTTPS or a trusted private network before sending authentication or torrent-add requests.

Risk: The skill can add torrent files to NAS storage.

Mitigation: Require explicit user confirmation before adding torrents and verify the selected result before download.

Risk: Temporary cookie files may expose authenticated downloader sessions.

Mitigation: Store cookies in a secure temporary location and remove them after the qBittorrent operation completes.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bluepop1991-cloud/skills/1lou-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with search results, confirmation prompts, and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create torrent files, temporary cookie files, and a local drama watchlist when executed with filesystem and network access.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

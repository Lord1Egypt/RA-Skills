## Description:

Gequhai Music helps agents search Gequhai for songs, retrieve standard or high-quality download links, show music rankings, and download selected tracks to a Synology NAS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anlinxi](https://clawhub.ai/user/anlinxi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search songs by title or artist, review rankings, retrieve download links, and send selected tracks to a configured Synology NAS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded NAS credentials could expose real storage access.

Mitigation: Remove embedded credentials, rotate the exposed NAS password, and load credentials from a protected secret store before use.

Risk: Unauthenticated service controls can trigger downloads and file changes on a Synology NAS.

Mitigation: Require authentication, bind the service to localhost or a protected interface, and use HTTPS for NAS access.

Risk: Download, rename, move, or overwrite operations can change files without sufficient confirmation.

Mitigation: Require explicit user confirmation before any download, rename, move, or overwrite operation.

Risk: Wildcard CORS can increase exposure of the service to unauthorized browser-based requests.

Mitigation: Disable wildcard CORS and restrict allowed origins to trusted clients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anlinxi/skills/gequhai-music)
- [Gequhai website](https://www.gequhai.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON responses with optional shell and Python command examples, download links, rankings, and download status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external music links, ranking entries, Synology NAS destination details, and file-operation status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Dygod Movies helps agents search recent and high-scoring movies or TV shows from dygod.net and prepare Synology NAS download actions.

This skill is for research and development only.

## Publisher:

[anlinxi](https://clawhub.ai/user/anlinxi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and media-library operators can use this skill to retrieve DYGod movie and TV metadata, filter high-score results, search titles, and prepare Synology DownloadStation tasks. Download actions should be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships real-looking Synology NAS credentials.

Mitigation: Do not install or run the package as published with those credentials; rotate the password if it is real and move secrets into protected configuration.

Risk: The service exposes privileged download actions without adequate protection.

Mitigation: Restrict the service to trusted hosts, add authentication, require explicit confirmation for downloads and deletions, and constrain allowed destinations.

Risk: NAS actions use HTTP endpoints in the provided examples and implementation.

Mitigation: Use HTTPS or a trusted private network and avoid exposing NAS APIs to untrusted networks.

## Reference(s):

- [Dygod Movies on ClawHub](https://clawhub.ai/anlinxi/skills/dygod-movies)
- [anlinxi publisher profile](https://clawhub.ai/user/anlinxi)
- [DYGod movie index](https://dygod.net/html/gndy/dyzz/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-compatible movie and TV result objects, Python examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include movie metadata, TV metadata, magnet or FTP download links, and Synology DownloadStation task results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

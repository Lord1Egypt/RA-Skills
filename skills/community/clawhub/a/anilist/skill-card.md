## Description:

CLI for searching, retrieving anime and manga information, interacting with user profile and lists on Anilist, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsku](https://clawhub.ai/user/mtsku)

### License/Terms of Use:


## Use Case:

Agents use this skill to run AniList CLI workflows for anime and manga discovery, airing lookups, media search, profile and social queries, and user list management. Authenticated write actions can update the user's AniList account when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the third-party npm package can introduce supply-chain risk.

Mitigation: Confirm the package is trusted before installation and consider pinning the CLI version.

Risk: AniList tokens grant account access and may be exposed through shared chats, logs, commits, or visible terminal history.

Mitigation: Treat the token like a password and avoid pasting it into shared or persistent locations.

Risk: Authenticated list-management commands can modify the user's AniList account.

Mitigation: Use dry-run behavior before mutations unless the user explicitly requests write execution.

## Reference(s):

- [AniList CLI skill page](https://clawhub.ai/mtsku/skills/anilist)
- [mtsku ClawHub publisher profile](https://clawhub.ai/user/mtsku)
- [@mtsku/anilist-cli npm package](https://www.npmjs.com/package/@mtsku/anilist-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses anilistcli commands; public read endpoints can run without auth, while authenticated mutations should be dry-run first unless write execution is explicitly requested.]

## Skill Version(s):

0.3.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

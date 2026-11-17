## Description:

Unified command-line interface for Radarr, Sonarr, and Lidarr. Search, add, and manage movies (Radarr), TV shows (Sonarr), and music (Lidarr) with calendar view and health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rappo](https://clawhub.ai/user/rappo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent search, add, remove, monitor, and check status for media libraries managed by Radarr, Sonarr, and Lidarr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remove commands can delete media library entries and may delete underlying files when delete-files options are used.

Mitigation: Require human review before remove operations, avoid delete-files unless intentional, and test commands against non-critical libraries first.

Risk: The skill uses API keys for Radarr, Sonarr, and Lidarr and reads them from local configuration files.

Mitigation: Store API-key configuration files with restrictive permissions and avoid sharing logs or command output that might expose local service details.

Risk: Running the skill with elevated permissions could increase the impact of command or configuration mistakes.

Mitigation: Run the skill as a normal user with only the access needed to reach the configured media services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rappo/skills/arr-all)
- [Publisher profile](https://clawhub.ai/user/rappo)
- [MusicBrainz artist pages](https://musicbrainz.org/artist)
- [The Movie Database movie pages](https://themoviedb.org/movie)
- [TheTVDB series pages](https://thetvdb.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; optionally uses column when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

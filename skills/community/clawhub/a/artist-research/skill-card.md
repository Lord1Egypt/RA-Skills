## Description:

Performs in-depth artist analysis combining Spotify API and external web data to report streaming stats, market position, and monetization potential.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pozmac](https://clawhub.ai/user/pozmac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, music industry analysts, managers, and collaborators use this skill to research an artist's Spotify profile, discography, streaming indicators, market position, and monetization potential. It is intended for artist evaluation, comparison, and report generation using Spotify API data and external web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill uses under-disclosed external authentication code and account-level Spotify credentials that are broader than needed for public artist reporting.

Mitigation: Review or replace the external authentication helper before installation; prefer a skill-local, read-only Spotify client credentials flow that reads only the required Spotify variables.

Risk: The security guidance flags playlist, library, playback, and other account-mutating Spotify actions as outside the needs of artist research.

Mitigation: Clearly forbid account-mutating Spotify actions and limit the skill to artist metadata, discography lookup, public reporting, and non-mutating external research.

## Reference(s):

- [Spotify Web API Endpoints - Post February 2026 Changes](references/spotify-endpoints-2026.md)
- [Spotify Web API February 2026 changes](https://developer.spotify.com/documentation/web-api/references/changes/february-2026)
- [Artist Research on ClawHub](https://clawhub.ai/pozmac/skills/artist-research)
- [pozmac publisher profile](https://clawhub.ai/user/pozmac)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report text with optional JSON data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports under reports/artist-report-{name}-{date}.md and may save JSON lookup output when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

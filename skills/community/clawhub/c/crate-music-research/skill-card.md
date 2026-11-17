## Description:

AI-powered music research with 92+ tools across 17 sources — MusicBrainz, Bandcamp, Discogs, Genius, Last.fm, Wikipedia, and more. Influence tracing, track verification, playlist building, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmoody1973](https://clawhub.ai/user/tmoody1973)

### License/Terms of Use:


## Use Case:

Developers, researchers, collectors, and music writers use this skill to research artists, releases, influences, tracks, market details, playlists, and publishable music notes with cited source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external npm MCP package with an API key.

Mitigation: Review and pin a specific crate-cli package version before use, and prefer restricted or disposable API keys with usage limits.

Risk: Publishing tools can post research publicly through Telegraph or Tumblr.

Mitigation: Require human review and confirmation before publishing content or updating public pages.

Risk: Collection, playlist, influence cache, and memory features may persist local data.

Mitigation: Confirm where SQLite or memory data is stored and how to delete records before using persistent features.

## Reference(s):

- [Crate CLI homepage](https://github.com/tmoody1973/crate-cli)
- [ClawHub skill page](https://clawhub.ai/tmoody1973/skills/crate-music-research)
- [Publisher profile](https://clawhub.ai/user/tmoody1973)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with cited source links and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include playlist exports, public publishing outputs, and local collection or cache updates when the corresponding MCP tools are configured.]

## Skill Version(s):

0.2.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

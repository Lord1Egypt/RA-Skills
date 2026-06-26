## Description: <br>
Performs in-depth artist analysis combining Spotify API and external web data to report streaming stats, market position, and monetization potential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pozmac](https://clawhub.ai/user/pozmac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Music industry analysts, artist managers, label teams, and agents use this skill to research an artist's streaming footprint, market position, monetization potential, and growth recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on undeclared Spotify authentication code and credentials from a sibling local project. <br>
Mitigation: Review the external auth code and .env before running the skill, and use a dedicated Spotify app with minimal read-only permissions. <br>
Risk: Artist reports may be based on external web sources with varying availability and reliability. <br>
Mitigation: Cross-reference important claims and confirm where generated reports or JSON files will be saved before execution. <br>


## Reference(s): <br>
- [Artist Research on ClawHub](https://clawhub.ai/pozmac/artist-research) <br>
- [Spotify Web API Endpoints - Post February 2026 Changes](references/spotify-endpoints-2026.md) <br>
- [Spotify Web API February 2026 changes](https://developer.spotify.com/documentation/web-api/references/changes/february-2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save artist reports under reports/ and JSON lookup files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

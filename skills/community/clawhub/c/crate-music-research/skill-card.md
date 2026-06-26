## Description: <br>
AI-powered music research with 92+ tools across 17 sources, including MusicBrainz, Bandcamp, Discogs, Genius, Last.fm, Wikipedia, influence tracing, track verification, playlist building, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmoody1973](https://clawhub.ai/user/tmoody1973) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, DJs, collectors, and music writers use this skill to research artists, verify tracks, trace musical influence, manage playlists or collections, and publish cited music research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an unpinned external npm MCP server while using API keys. <br>
Mitigation: Install only if you trust the crate-cli npm package and publisher; pin or verify the package version and provide only the API keys needed for the task. <br>
Risk: The skill includes public publishing and persistent memory features. <br>
Mitigation: Require explicit confirmation before publishing to Telegraph or Tumblr or writing persistent memory, and review generated research and citations before publication. <br>


## Reference(s): <br>
- [Crate CLI homepage](https://github.com/tmoody1973/crate-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include citations, source URLs, playlist exports, collection updates, public publishing instructions, and MCP configuration guidance.] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

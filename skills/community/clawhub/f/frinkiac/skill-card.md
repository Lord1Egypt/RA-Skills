## Description: <br>
Search TV show screenshots and generate memes from The Simpsons, Futurama, Rick and Morty, and 30 Rock. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryantenney](https://clawhub.ai/user/ryantenney) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search dialogue, browse adjacent TV frames, retrieve episode metadata and subtitles, and generate screenshots or memes for supported shows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup runs a third-party npm MCP server. <br>
Mitigation: Review the npm package provenance before installation and pin a trusted package version in MCP configuration. <br>
Risk: Search queries and meme captions may be processed by external services. <br>
Mitigation: Avoid entering private, confidential, or sensitive text into searches or meme captions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryantenney/frinkiac) <br>
- [Publisher profile](https://clawhub.ai/user/ryantenney) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance, image URLs or image data] <br>
**Output Format:** [Markdown text with JSON MCP configuration snippets and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return scene metadata, subtitles, screenshots, nearby-frame results, and generated meme images from supported services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

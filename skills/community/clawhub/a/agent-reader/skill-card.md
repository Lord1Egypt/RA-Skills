## Description: <br>
Document beautifier for AI Agents that converts Markdown to styled webpages, Word, PDF, and image slideshows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebbfijsf](https://clawhub.ai/user/ebbfijsf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Agent Reader to turn Markdown reports, documents, and image sets into delivery-ready webpages, PDF or DOCX files, and slideshow exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup runs an external npm package through npx. <br>
Mitigation: Install only if comfortable running the package and prefer pinning the package version in the MCP configuration. <br>
Risk: Rendered files, inline HTML, and base64 returns may contain the same sensitive information as the source Markdown or images. <br>
Mitigation: Treat generated outputs as sensitive whenever the source content is sensitive and share or store them accordingly. <br>
Risk: Implicit format selection or generated export variants may be less predictable than explicit tool calls. <br>
Mitigation: Use explicit export tools and formats when predictable output is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ebbfijsf/agent-reader) <br>
- [npm Package](https://www.npmjs.com/package/agent-reader) <br>
- [Glama MCP Server Listing](https://glama.ai/mcp/servers/ebbfijsf/agent-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Configuration, HTML, PDF, DOCX] <br>
**Output Format:** [File paths or inline content for rendered HTML, PDF, DOCX, and slideshow exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return inline HTML or base64 file content; file outputs are described as writing under /tmp/agent-reader/ in the artifact.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

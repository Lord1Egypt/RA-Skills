## Description: <br>
Generate and edit images with Google Gemini image models via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and call a Gemini MCP server for image generation, image editing, consistent image sets, and conversational refinement from text, image, URL, clipboard, or video inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gemini API key. <br>
Mitigation: Install only when the user is comfortable granting the MCP server access to that credential, and store the key in the configured MCP environment or local environment file. <br>
Risk: Prompts, images, clipboard images, URLs, and videos may be sent to Gemini or Google services. <br>
Mitigation: Use private media, clipboard capture, URL inputs, and video inputs only when the user intends that content to be processed externally. <br>
Risk: Local file and output directory parameters can read or write user-selected media paths. <br>
Mitigation: Use explicit input file paths and output directories, and avoid broad or unintended folders for media processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gemini-mcp) <br>
- [npm package: @chrischall/gemini-mcp](https://www.npmjs.com/package/@chrischall/gemini-mcp) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides MCP tool calls that may save generated image files or return inline image bytes and metadata.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

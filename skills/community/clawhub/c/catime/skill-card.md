## Description: <br>
Fetch and send AI-generated hourly cat images. Every hour a unique cat artwork is born via Google Gemini. Use when user asks for a cat picture, wants to browse the cat gallery, or requests the latest AI-generated cat image to be sent to them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yazelin](https://clawhub.ai/user/yazelin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent or requested AI-generated cat images, parse the CLI output, and send an image URL with optional caption metadata to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Python package catime and a CLI install step. <br>
Mitigation: Install in an isolated Python environment and invoke the skill only when the user explicitly asks to fetch or send cat images. <br>
Risk: The gallery requires network access to retrieve public GitHub-hosted image metadata and image URLs. <br>
Mitigation: If retrieval fails, tell the user that the gallery requires internet access and retry only when connectivity is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yazelin/catime) <br>
- [Publisher profile](https://clawhub.ai/user/yazelin) <br>
- [catime GitHub repository](https://github.com/yazelin/catime) <br>
- [catime gallery](https://yazelin.github.io/catime/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and message payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public image URLs and optional metadata such as cat number, timestamp, model, prompt, and story when available.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

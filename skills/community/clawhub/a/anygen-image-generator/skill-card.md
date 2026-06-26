## Description: <br>
Generates images, illustrations, and visual assets through the AnyGen CLI and remote AnyGen service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create image assets such as posters, banners, mockups, thumbnails, covers, icons, and other AI-generated visuals. It is intended for workflows where prompts and generation requests can be sent to AnyGen's remote service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation work is sent to a remote AnyGen service. <br>
Mitigation: Use a scoped or revocable AnyGen API key and avoid confidential prompts or private assets unless remote processing is acceptable. <br>
Risk: The skill may install the separate anygen-workflow-generate skill if it is unavailable. <br>
Mitigation: Review the AnyGen CLI and anygen-workflow-generate skill before allowing installation or deployment. <br>
Risk: Server security evidence marks the release as suspicious. <br>
Mitigation: Review the release and security guidance before deployment, and scan any installed workflow dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/logictortoise) <br>
- [AnyGen CLI package](https://www.npmjs.com/package/@anygen/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ANYGEN_API_KEY and the anygen CLI before generation requests can run.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

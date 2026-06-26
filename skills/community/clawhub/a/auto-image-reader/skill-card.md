## Description: <br>
Automatically locates uploaded image files and reads them so an agent can answer questions about image content without relying on relative paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when chats include uploaded images and they want the agent to find the real file path, analyze the image, and answer questions about visible content or image issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically analyze the wrong image when several attachments or recent images are present. <br>
Mitigation: Ask the agent to confirm the exact image before analysis in sensitive or multi-attachment chats. <br>
Risk: Image listing may expose unrelated workspace or cross-conversation images. <br>
Mitigation: Verify that selected image paths belong to the intended conversation or workspace before analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tianheihei002/auto-image-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Natural-language answers with optional extracted text or visual analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uploaded image context and image-understanding tool results when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

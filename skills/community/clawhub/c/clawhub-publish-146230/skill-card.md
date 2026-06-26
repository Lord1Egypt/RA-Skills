## Description: <br>
Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). High quality, native generation without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxw975](https://clawhub.ai/user/gxw975) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate image files from text prompts with configurable output paths and aspect ratios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Google OAuth credentials through a helper script that is not included in the package. <br>
Mitigation: Install only after inspecting the local generate.js script, use a dedicated revocable OAuth profile, and require explicit confirmation before broad image requests invoke the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gxw975/clawhub-publish-146230) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [Image file written to disk with a MEDIA path emitted on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a configured Google Antigravity OAuth profile.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

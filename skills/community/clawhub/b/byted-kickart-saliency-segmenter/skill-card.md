## Description: <br>
Segments subjects from image files and removes backgrounds through the Volcengine Kickart image cutout workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload JPEG, PNG, WEBP, or ZIP image inputs, run subject segmentation, and receive subject and mask outputs for background removal and product imagery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires cloud credentials and may ask users to provide AK/SK secrets in chat. <br>
Mitigation: Use scoped, revocable API tokens where possible and avoid pasting long-lived account secrets into chat. <br>
Risk: The workflow uploads user images to remote services and may log request or task data. <br>
Mitigation: Avoid sensitive images unless remote processing is acceptable, and clean temporary logs and caches after use. <br>
Risk: The version check can return an installation command for upgrades. <br>
Mitigation: Do not approve or run returned upgrade commands until the source and command have been independently verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-kickart-saliency-segmenter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return remote image result URLs, media IDs, task status, error codes, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

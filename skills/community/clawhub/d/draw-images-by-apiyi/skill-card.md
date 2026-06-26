## Description: <br>
Generate images using APIYI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengwuzhi](https://clawhub.ai/user/mengwuzhi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate images from text prompts through APIYI, choosing the output filename and supported resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to the third-party APIYI service. <br>
Mitigation: Do not include secrets, personal data, or confidential business information in prompts. <br>
Risk: The skill writes generated images to user-selected relative or absolute paths. <br>
Mitigation: Prefer workspace-relative filenames and review output paths before execution. <br>
Risk: The skill requires an APIYI API key. <br>
Mitigation: Provide APIYI_API_KEY through the environment or configured skill environment, and avoid embedding secrets in prompts or shared command history. <br>


## Reference(s): <br>
- [APIYI](https://apiyi.com/) <br>
- [Draw Images By Apiyi on ClawHub](https://clawhub.ai/mengwuzhi/draw-images-by-apiyi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and APIYI_API_KEY; supports 1K, 2K, and 4K resolution settings and prints a MEDIA line for generated images.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

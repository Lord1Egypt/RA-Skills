## Description: <br>
Generate images using Cloudflare Workers AI flux-1-schnell model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EXPYSF98](https://clawhub.ai/user/EXPYSF98) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate PNG images from text prompts through Cloudflare Workers AI and return the saved file path for downstream delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes a Cloudflare credential. <br>
Mitigation: Remove the embedded credential, rotate the exposed token, and load a least-privilege credential from a secret store or environment variable. <br>
Risk: Image prompts flow into a shell command. <br>
Mitigation: Replace shell-based curl construction with a safe HTTP client or shell-free subprocess call before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EXPYSF98/cloudflare-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown usage guidance, Python code, shell commands, and PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the generated image file path after writing a PNG file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

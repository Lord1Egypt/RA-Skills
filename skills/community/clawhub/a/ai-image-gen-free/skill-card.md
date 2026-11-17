## Description: <br>
ai-image-gen-free helps agents generate PNG images from text prompts through an ai-model Flash Image API workflow with standard and 2K resolution options across multiple aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to create social avatars, wallpapers, banner images, and lightweight visual drafts from text prompts. It is suited to text-to-image generation where an API key, network access, and local PNG output are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key for image generation. <br>
Mitigation: Keep API keys in environment variables only, avoid pasting them into chat, and do not write them to logs, image metadata, or version control. <br>
Risk: The skill sends requests to an external image generation API endpoint. <br>
Mitigation: Confirm the endpoint and service terms are trusted before installation or use, especially for commercial workflows. <br>
Risk: Generated images are written to local output paths and overwrite behavior is not documented. <br>
Mitigation: Use explicit, non-sensitive output paths and check whether a target file already exists before running generation. <br>
Risk: The artifact is incomplete in places and relies on command execution. <br>
Mitigation: Review commands and configuration before execution and run the skill in an agent environment with appropriate filesystem and network controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-image-gen-free) <br>
- [ai-model Image API endpoint](https://code.newcli.com/ai-model) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and PNG image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY; generated image paths should be explicit and checked before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

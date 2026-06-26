## Description: <br>
Fotor Skills helps agents generate and edit images and videos for photo editing, background removal or replacement, product photos, ad creatives, social media graphics, upscaling, restoration, portrait enhancement, text-to-video, and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fotor-everimaging](https://clawhub.ai/user/fotor-everimaging) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to ask an agent for Fotor-powered image generation, image editing, upscaling, background removal, product and marketing visuals, and video generation. The skill can guide setup, choose task parameters, upload local media, run Fotor API tasks, and return generated result URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Fotor API key and may send prompts and selected media files to Fotor for processing. <br>
Mitigation: Use only approved Fotor credentials, keep keys out of chat and source control, and confirm that prompts and media are appropriate to send to Fotor before execution. <br>
Risk: The skill can create a local Python environment and install or upgrade SDK dependencies using uv. <br>
Mitigation: Review the uv installer and dependency installation steps before use in environments that require pinned or approved software sources. <br>
Risk: Some workflows can consume Fotor credits or initiate recharge guidance. <br>
Mitigation: Check account credit balance before large or batch jobs and review any returned payment links before purchasing credits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fotor-everimaging/fotor-skills) <br>
- [Fotor Skills homepage](https://developers.fotor.com/fotor-skills/) <br>
- [GitHub homepage from metadata](https://github.com/fotor-ai/fotor-skills) <br>
- [Get API Key](references/get_api_key.md) <br>
- [Credits and Recharge](references/credits-and-recharge.md) <br>
- [Image Models](references/image_models.md) <br>
- [Image Generation Scenarios](references/image_scenarios.md) <br>
- [Video Models](references/video_models.md) <br>
- [Video Generation Scenarios](references/video_scenarios.md) <br>
- [Parameter Reference](references/parameter_reference.md) <br>
- [Install or Upgrade](references/install-or-upgrade.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON task specifications, and generated result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local Python environment, install or upgrade the Fotor SDK, send prompts and selected media to Fotor APIs, poll task status, and return result URLs plus task metadata.] <br>

## Skill Version(s): <br>
1.0.20 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

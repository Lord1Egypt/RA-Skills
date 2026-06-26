## Description: <br>
Generates Nano Banana image outputs through the IMA Open API for text-to-image and image-to-image workflows using the allowed gemini-3.1-flash-image and gemini-3-pro-image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images with IMA Nano Banana models from prompts or reference images, choosing budget or premium profiles, output size, and aspect ratio through the bundled script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, selected reference images, generated output metadata, and the IMA API key to IMA endpoints. <br>
Mitigation: Use a scoped or test IMA API key where available, avoid sensitive prompts or images, and install only if IMA Studio is an acceptable processor for the intended data. <br>
Risk: Local image-to-image workflows can upload local files through the disclosed IMA upload flow. <br>
Mitigation: Prefer HTTPS image URLs when practical and do not upload private local images unless the destination and retention expectations are acceptable. <br>
Risk: The skill keeps local preferences and operational logs under ~/.openclaw. <br>
Mitigation: Delete ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ if local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/ai-nano-banana-ima) <br>
- [Publisher profile](https://clawhub.ai/user/allenfancy-gan) <br>
- [IMA Studio](https://imastudio.com/) <br>
- [Security disclosure](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON script output; successful runs return generated image URLs or media attachments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY, uses fixed IMA API endpoints, and may write local preferences and logs under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter and changelog report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

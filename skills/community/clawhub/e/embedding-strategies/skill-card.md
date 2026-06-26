## Description: <br>
Guides agents to generate or edit PNG images with Nano Banana Pro (Gemini 3 Pro Image) through a command-line script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to produce or edit images by invoking a Gemini image-generation script. It supports prompt-driven generation, input-image editing, resolution selection, and draft-to-final iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package includes unrelated workspace files, nested skills, memory/persona files, hooks, and agent behavior instructions outside the visible image-generation skill. <br>
Mitigation: Review before installation and republish as a minimal package containing only the intended SKILL.md and required image-generation script. <br>
Risk: Server security evidence reports hardcoded credentials or exposed credential material in the broader package. <br>
Mitigation: Remove secrets from the package and rotate any exposed credentials before use. <br>
Risk: The skill sends prompts and optional input images to an external Gemini image-generation API. <br>
Mitigation: Use approved API keys through environment or secret management and avoid sending sensitive prompts or images without policy review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/embedding-strategies) <br>
- [Publisher profile](https://clawhub.ai/user/icesumer-lgtm) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Image generation script](artifact/clawhub skills/scripts/generate_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the script produces PNG image files and prints saved paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key supplied by argument or GEMINI_API_KEY; supports 1K, 2K, and 4K output resolutions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Professional image generation assistant for workplace PPT graphics, marketing posters, product photos, and social media content, turning simple descriptions into professional prompts and high-quality images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ximasadila](https://clawhub.ai/user/ximasadila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, creators, and workplace teams use this skill to turn short image requests into polished prompts and generated visuals for presentations, marketing, product imagery, social media, avatars, badges, flowcharts, UI prototypes, and related business assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, private image URLs, and grounded search requests may be sent to external image-generation or search providers. <br>
Mitigation: Use the skill only with acceptable external providers, review the default provider and region, and avoid confidential prompts or private image URLs when grounding or search is enabled. <br>
Risk: API keys and saved prompt preferences may persist locally. <br>
Mitigation: Use a dedicated API key and periodically inspect or clear the local configuration and personal prompt library when they may contain sensitive project details. <br>


## Reference(s): <br>
- [Easy Image ClawHub Release](https://clawhub.ai/ximasadila/easy-image) <br>
- [Skill Instructions](SKILL.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Usage Examples](examples/usage-examples.md) <br>
- [Model Selection](references/model-selection.md) <br>
- [Professional Terminology Glossary](references/glossary.md) <br>
- [Jiekou AI Platform Reference](references/platforms/jiekou.md) <br>
- [Google Imagen Platform Reference](references/platforms/google.md) <br>
- [Novita Platform Reference](references/platforms/novita.md) <br>
- [OpenRouter Platform Reference](references/platforms/openrouter.md) <br>
- [PPIO Platform Reference](references/platforms/ppio.md) <br>
- [WaveSpeed Platform Reference](references/platforms/wavespeed.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, Files] <br>
**Output Format:** [Conversational text with generated image files and local JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save PNG image files to the configured path and maintain a local personal prompt library.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, changelog dated 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

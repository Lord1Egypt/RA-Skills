## Description: <br>
Generate AI professional headshot images via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request professional headshot image generation from text prompts, optionally choosing dimensions or providing a reference image UUID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, user-supplied tokens, and optional reference image identifiers are sent to the external Neta/TalesOfAI service. <br>
Mitigation: Use a scoped or trial token, avoid sensitive personal details or sensitive reference images, and review the provider's privacy terms before use. <br>
Risk: Generated headshots may be used in identity-related contexts where image quality, consent, or policy expectations matter. <br>
Mitigation: Review generated images before publication and ensure the prompt, reference image use, and downstream use comply with applicable consent and platform policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/ai-headshot-skill) <br>
- [Neta AI access page](https://www.neta.art/open/) <br>
- [TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>
- [TalesOfAI task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with Markdown and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied Neta API token; optional size and reference image UUID parameters are supported.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

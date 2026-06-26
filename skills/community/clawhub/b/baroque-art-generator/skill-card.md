## Description: <br>
Generates dramatic baroque-style oil painting images from text prompts, with optional size selection and reference-image style inheritance through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create baroque portrait, print, and historical artwork concepts from text prompts, optionally choosing image dimensions or inheriting style from a reference image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected image size, optional reference image UUID, and the Neta API token are sent to the external Neta image API. <br>
Mitigation: Use a revocable token and avoid confidential, personal, or regulated content in prompts and reference-image identifiers. <br>
Risk: Passing the API token directly on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer an environment variable or other secret-management workflow instead of typing the token directly into reusable shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/baroque-art-generator) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls] <br>
**Output Format:** [Plain text image URL returned after polling the image generation task] <br>
**Output Parameters:** [1D; prompt text, size option, Neta API token, and optional reference image UUID control the request] <br>
**Other Properties Related to Output:** [Requires network access to api.talesofai.com and a valid Neta API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

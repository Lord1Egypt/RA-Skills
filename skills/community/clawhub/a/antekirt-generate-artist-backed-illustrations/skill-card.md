## Description: <br>
Generate illustrations and visuals using Antekirt artists and prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrejdorsian](https://clawhub.ai/user/andrejdorsian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to select Antekirt artists and generate image, SVG, or video assets from prompts. It is useful when visual output needs explicit artist selection and generation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and generation requests to Antekirt, so sensitive prompt content could be exposed to the external service. <br>
Mitigation: Avoid private or confidential information in prompts and use the official Antekirt API host. <br>
Risk: Image, SVG, and video generation can consume Antekirt credits. <br>
Mitigation: Require explicit approval before generation, especially for higher-cost video operations. <br>
Risk: Antekirt API keys are required for use. <br>
Mitigation: Keep ANTEKIRT_API_KEY secret and provide it only through environment variables or an approved secrets mechanism. <br>


## Reference(s): <br>
- [Antekirt API Endpoints](references/api-endpoints.md) <br>
- [Antekirt Documentation](https://antekirt.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/andrejdorsian/antekirt-generate-artist-backed-illustrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text with generated asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return image, SVG, or video URLs after asynchronous generation and polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

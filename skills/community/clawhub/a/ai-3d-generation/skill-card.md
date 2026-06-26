## Description: <br>
Create, convert, and download AI-generated 3D models using Neural4D APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6e6e6e](https://clawhub.ai/user/6e6e6e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and manufacturing engineers use this skill to generate 3D assets from text or images, poll Neural4D jobs, download GLB outputs, and convert models into manufacturing-friendly formats such as STL, FBX, OBJ, or USDZ. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and images selected for generation are sent to Neural4D/DreamTech cloud processing. <br>
Mitigation: Avoid submitting confidential, regulated, personal, or proprietary content unless the provider and retention terms are approved for that use. <br>
Risk: The Neural4D API token could be exposed through logs, shared files, or shell history. <br>
Mitigation: Keep NEURAL4D_API_TOKEN secret, pass it through the environment or a secure secret store, and avoid printing bearer tokens in command output. <br>
Risk: Bulk generation, image generation, chibi-style generation, and format conversion consume API points. <br>
Mitigation: Check the point balance before bulk runs and confirm expected operation counts before starting asynchronous jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/6e6e6e/ai-3d-generation) <br>
- [Neural4D API base endpoint](https://alb.neural4d.com:3000/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API request details and command-oriented steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for command workflows, optional NEURAL4D_API_TOKEN configuration, and user-selected prompts or images for cloud processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

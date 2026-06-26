## Description: <br>
Ccy Txt2img is an offline Pillow-based skill for generating simple PNG/JPEG text images, diagrams, shape drawings, and rule-driven scene renders from prompts or scene JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchongyong](https://clawhub.ai/user/chenchongyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate local text images, simple posters, diagrams, geometry, and scene-based PNG/JPEG graphics without calling external image-generation APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads caller-provided image, scene, and font paths and writes generated image files to caller-selected output locations. <br>
Mitigation: Use a safe output directory, avoid overwriting important files, and pass only image, scene, or font paths that the agent is intended to read. <br>
Risk: The skill depends on Pillow for local image rendering. <br>
Mitigation: Install Pillow from a trusted package source and keep it updated through the deployment's normal dependency process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenchongyong/ccy-txt2img) <br>
- [Font guidance](artifact/assets/fonts/README.md) <br>
- [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration] <br>
**Output Format:** [PNG/JPEG image files, optional JSON scene output, and Python or CLI invocation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Pillow and writes images to caller-selected output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

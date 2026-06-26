## Description: <br>
Generates high-quality cat selfie images with random or selected scenes using a Volcengine Doubao Seedream image model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Romanticjojo](https://clawhub.ai/user/Romanticjojo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to generate cat portrait images for chat, heartbeat messages, or scripted workflows with a random or named scene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editable scene prompts are passed through shell command execution. <br>
Mitigation: Use only trusted scene files and avoid custom prompts containing shell metacharacters until command execution is changed to argument arrays. <br>
Risk: The skill depends on a separate volcengine-image-generate skill and sends prompts to Volcengine, which may create API cost or data handling exposure. <br>
Mitigation: Verify the dependent image-generation skill and confirm Volcengine API usage, cost, and prompt handling before installing or running. <br>


## Reference(s): <br>
- [ClawHub Cat Selfie release page](https://clawhub.ai/Romanticjojo/cat-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/Romanticjojo) <br>
- [README](README.md) <br>
- [Scene configuration](config/scenes.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance, CLI output, JavaScript return objects, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under ~/.openclaw/workspace/images/ with generated_image_<timestamp>_<index> filenames.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

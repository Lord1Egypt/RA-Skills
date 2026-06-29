## Description: <br>
Helps an agent generate text-to-image assets through ai.fun.tv, including project creation, task submission, polling, image URL return, optional downloads, and token handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amireux0013](https://clawhub.ai/user/amireux0013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent create ai.fun.tv text-to-image jobs, monitor completion, return generated image URLs, and optionally save generated image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to ai.fun.tv. <br>
Mitigation: Install and use the skill only when ai.fun.tv is an acceptable image-generation provider for the prompt content. <br>
Risk: A provided authorization token may be saved locally for reuse. <br>
Mitigation: Use the environment variable or no-save option when persistence is not desired, and delete or rotate saved tokens on shared machines or workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amireux0013/ai-fun-tv-image) <br>
- [ai.fun.tv](https://ai.fun.tv) <br>
- [ai.fun.tv OpenClaw token page](https://ai.fun.tv/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands; script output is JSON containing project ID, task ID, image URLs, and optional saved file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are returned as remote URLs and may be downloaded to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

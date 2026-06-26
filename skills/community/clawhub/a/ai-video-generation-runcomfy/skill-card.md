## Description: <br>
Routes video-generation requests to RunComfy text-to-video, image-to-video, and video-extension models, then provides model-specific prompting guidance and minimal `runcomfy run` commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, creators, and agent operators use this skill to choose an appropriate RunComfy video model and invoke it for text-to-video, image-to-video, or video-extension jobs. It is useful for producing prompts, JSON inputs, shell commands, and routing guidance for RunComfy video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced image, audio, or video URLs may be sent to RunComfy for generation. <br>
Mitigation: Confirm user intent before sending media or prompts, and avoid submitting sensitive or unauthorized content. <br>
Risk: The skill requires a RunComfy token or local login for CLI execution. <br>
Mitigation: Keep tokens out of prompts, logs, generated files, and repositories; prefer environment or local CLI credential storage with restricted permissions. <br>
Risk: Ambiguous video requests could select the wrong model, endpoint, cost tier, duration, or media input. <br>
Mitigation: Clarify unclear requests before running the CLI, especially when a request involves paid generation, external media URLs, lip-sync, or video extension. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/ai-video-generation-runcomfy) <br>
- [RunComfy homepage](https://www.runcomfy.com) <br>
- [RunComfy video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>
- [RunComfy Kling model collection](https://www.runcomfy.com/models/collections/kling?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>
- [RunComfy Seedance model collection](https://www.runcomfy.com/models/collections/seedance?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>
- [RunComfy Veo 3 model collection](https://www.runcomfy.com/models/collections/veo-3?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger RunComfy CLI jobs that download generated video files to the requested output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Routes text-to-image and image-to-image requests to suitable RunComfy image models and provides the matching RunComfy CLI command, prompt pattern, and JSON input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, creators, and agents use this skill to generate or edit images through RunComfy by selecting an appropriate model, shaping prompts, and invoking the local RunComfy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source images, and edit requests may contain sensitive or proprietary content that is processed by RunComfy. <br>
Mitigation: Use only images and text that are appropriate to send to RunComfy, and avoid confidential or regulated content unless the user has approved that processing. <br>
Risk: Reference image URLs or web-grounded results can influence generated output in unexpected ways. <br>
Mitigation: Use only user-provided reference URLs for the task, keep web search disabled unless explicitly requested, and review the generated image before use. <br>
Risk: The skill depends on the local RunComfy CLI and account configuration, so commands may fail or write outputs somewhere unexpected if setup values are wrong. <br>
Mitigation: Confirm the CLI is installed, authentication is configured, and the output directory is intentional before running generation jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/ai-image-generation-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy image models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy) <br>
- [RunComfy CLI install](https://docs.runcomfy.com/cli/install?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy) <br>
- [RunComfy CLI authentication](https://docs.runcomfy.com/cli/auth?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-image-generation-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with RunComfy CLI commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, RUNCOMFY_TOKEN or RunComfy login, and local RunComfy configuration; generated image files are downloaded to the requested output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

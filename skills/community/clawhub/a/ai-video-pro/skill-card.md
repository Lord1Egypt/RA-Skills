## Description: <br>
Ai Video Pro converts creative video descriptions into cinematic video-generation prompts and can optionally route confirmed prompts to video providers such as LumaAI, Runway, Replicate, or ComfyUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaalenwow](https://clawhub.ai/user/aaalenwow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and agent users use this skill to turn rough scene ideas into structured cinematic prompts, compare provider-specific prompt formats, and optionally generate or prepare videos for publishing after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes installers and optional dependency setup beyond prompt generation. <br>
Mitigation: Use prompt-only mode by default and require explicit human confirmation before running dependency installation scripts. <br>
Risk: Generation mode may send prompts to external video providers and use paid API credentials. <br>
Mitigation: Confirm the selected provider, estimated cost, and prompt contents before making API calls; configure only the minimum required API key. <br>
Risk: Publishing and cloud-upload paths may use social platform tokens, cookies, or broad cloud credentials. <br>
Mitigation: Avoid setting social cookies or cloud credentials unless publishing is required, and require manual review before uploads or public posts. <br>
Risk: The package was classified as suspicious by the authoritative security evidence. <br>
Mitigation: Review the scripts and security summary before deployment, and restrict execution to the specific mode needed for the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaalenwow/ai-video-pro) <br>
- [Cinematic vocabulary reference](references/cinematic_vocabulary.md) <br>
- [Provider matrix](references/provider_matrix.md) <br>
- [Platform publishing specifications](references/platform_specs.md) <br>
- [LumaAI Dream Machine API endpoint](https://api.lumalabs.ai/dream-machine/v1/generations) <br>
- [Runway API endpoint](https://api.dev.runwayml.com/v1) <br>
- [Weibo Open API](https://api.weibo.com/2/) <br>
- [Douyin Open Platform](https://open.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style prompt structures with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only mode requires no external service; generation and publishing modes may use local tools, API credentials, cloud uploads, or platform tokens.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

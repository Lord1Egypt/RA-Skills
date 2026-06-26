## Description: <br>
Analyzes video content with Volcengine LAS Doubao vision-language models to answer questions, describe scenes, identify objects and actions, and produce captions or summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to configure Volcengine LAS access, estimate token-based cost, upload or reference video, and request Doubao VLM video understanding. It is suited for video question answering, scene and action description, object recognition, captions, annotations, and summaries. <br>

### Deployment Geography for Use: <br>
China regions supported by Volcengine LAS: cn-beijing and cn-shanghai. <br>

## Known Risks and Mitigations: <br>
Risk: Setup can install or update the Volcengine LAS SDK from a remote wheel without hash verification. <br>
Mitigation: Install only from a trusted network and source, review the SDK source and install command before use, and pin or preinstall an approved SDK version in managed environments. <br>
Risk: The workflow requires sensitive LAS credentials and may upload videos to provider-managed storage for processing. <br>
Mitigation: Use least-privilege credentials, keep secrets out of chat, confirm region and billing settings before execution, and avoid sending sensitive videos unless provider-side upload and processing are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-las-vlm-video) <br>
- [las_vlm_video API reference](references/api.md) <br>
- [Volcengine LAS pricing reference](references/prices.md) <br>
- [Volcengine LAS pricing documentation](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LAS_API_KEY and matching LAS_REGION; results may include local output files, task metadata, and billing disclaimer text.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task detail retrieval, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husu](https://clawhub.ai/user/husu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate AIVideoMaker text-to-video and image-to-video jobs, monitor task status, retrieve completed outputs, and cancel submitted tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image inputs, task IDs, and the AIVIDEO_API_KEY are sent to AIVideoMaker. <br>
Mitigation: Use a dedicated API key, avoid sensitive media, rotate credentials when needed, and monitor provider account usage. <br>
Risk: Video generation requests may consume provider credits or encounter upstream rate limits. <br>
Mitigation: Confirm model and duration choices before execution, monitor credit usage, and use the built-in retry/backoff behavior for idempotent task queries. <br>


## Reference(s): <br>
- [AIVideoMaker API Reference](references/api-reference.md) <br>
- [Usage Examples](references/examples.md) <br>
- [AIVideoMaker](https://aivideomaker.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/husu/ai-video-maker) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses with command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized task results include ok, status, taskId, data, errorCode, errorMessage, and retryAfter when available.] <br>

## Skill Version(s): <br>
1.0.14 (source: server evidence, SKILL.md frontmatter, _meta.json, clawhub.manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

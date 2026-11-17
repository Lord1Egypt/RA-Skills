## Description:

Generate document, outline, and image-text AI notes from a user-provided video URL using Baidu Qianfan video analysis APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiduqianfangroup](https://clawhub.ai/user/baiduqianfangroup)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to submit a video URL to Baidu Qianfan, create an AI-note generation task, and retrieve generated document, outline, or image-text notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs and referenced video content are sent to Baidu Qianfan using the configured BAIDU_API_KEY.

Mitigation: Use only public, approved, or non-sensitive media URLs unless sharing the content with Baidu Qianfan is authorized.

Risk: The skill depends on an external API credential in the runtime environment.

Mitigation: Provide BAIDU_API_KEY through approved secret management and avoid exposing it in prompts, logs, or shared command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiduqianfangroup/skills/ai-notes-of-video)
- [Baidu Qianfan AI note task create API](https://qianfan.baidubce.com/v2/tools/ai_note/task_create)
- [Baidu Qianfan AI note query API](https://qianfan.baidubce.com/v2/tools/ai_note/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [JSON task responses containing generated note content, with note content suitable for text or markdown presentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and a reachable video URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

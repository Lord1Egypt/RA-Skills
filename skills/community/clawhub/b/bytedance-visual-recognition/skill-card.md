## Description:

Multimodal visual recognition via Doubao-Seed and Zhipu GLM for image or video analysis, image or video to code, batch processing, follow-up questions, provider fallback, local media caching, persistent history, and optional IAM usage sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etmnb](https://clawhub.ai/user/etmnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send selected images or videos to configured Doubao or GLM vision models and receive scene descriptions, extracted text, structured Markdown analysis, or generated code. It also supports batch directory processing and follow-up questions over prior recognition context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, videos, screenshots, documents, and prompts may contain private or sensitive information and are sent to third-party cloud vision APIs.

Mitigation: Review media before use, avoid sending regulated or confidential content unless approved, and configure only providers whose data handling terms are acceptable for the deployment.

Risk: API keys and optional IAM credentials are stored in plaintext config.json.

Mitigation: Use least-privileged provider keys, avoid shared or synced folders, rotate exposed keys, and remove unused credentials from config.json.

Risk: Local files such as Temp/, vision_history.json, and .last_response can retain media context or model responses after recognition.

Mitigation: Set the shortest practical retention period, manually delete Temp/, vision_history.json, and .last_response after sensitive sessions, and do not rely on automatic cleanup for GLM follow-up context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etmnb/skills/bytedance-visual-recognition)
- [Volcengine Doubao visual understanding documentation](https://www.volcengine.com/docs/82379/1569618)
- [Zhipu Open Platform](https://open.bigmodel.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text and Markdown-style analysis, with generated code when code output is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image files up to 15 MB, video files up to 50 MB, batch directory processing, follow-up context, local cache files, and persistent history.]

## Skill Version(s):

5.0.1 (source: server release metadata; artifact script and skill tags agree)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

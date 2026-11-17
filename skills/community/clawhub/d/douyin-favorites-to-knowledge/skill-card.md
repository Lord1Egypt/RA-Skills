## Description:

Synchronizes a user's authorized Douyin favorites, or explicitly requested liked videos, into local Markdown or Obsidian notes with optional SiliconFlow or local Whisper transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tars1230](https://clawhub.ai/user/tars1230)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to set up and run authorized Douyin collection, transcription, and synchronization into a local Markdown or Obsidian knowledge base while keeping favorites and liked-list sources separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a dedicated persistent Douyin browser profile for authorized collection.

Mitigation: Use only an app-owned profile, avoid shared or repository paths for DOUYIN_FAVORITES_PROFILE_DIR, and clear saved session state with logout when no longer needed.

Risk: Cloud transcription providers may receive media or extracted audio when cloud transcription is selected.

Mitigation: Choose cloud transcription only after user approval, use local or no transcription for sensitive media, and keep API keys in environment variables or a secret manager.

Risk: Daily scheduled sync creates recurring background activity on the user's machine.

Mitigation: Enable the scheduled task only when the user explicitly wants recurring sync, verify the task status and timezone, and avoid passing credentials in scheduler arguments.

Risk: Custom module:function adapters execute local code and can access local data or secrets.

Mitigation: Use only trusted adapters, review adapter behavior before enabling it, and require adapters to obtain secrets from the host environment or secret manager without returning them in item data or errors.

Risk: A custom SILICONFLOW_ASR_URL can redirect transcription traffic to an untrusted endpoint.

Mitigation: Avoid overriding SILICONFLOW_ASR_URL unless the endpoint is trusted and controlled by the user or operator.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tars1230/skills/douyin-favorites-to-knowledge)
- [Gitee installation repository linked by artifact](https://gitee.com/tars123/douyin-favorites-to-knowledge)
- [GitHub project page linked by artifact](https://github.com/tars1230/douyin-favorites-to-knowledge)
- [SiliconFlow pricing](https://siliconflow.cn/pricing)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes and reports with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local knowledge-base files and operational guidance; optional transcription may use cloud APIs or local Whisper depending on user choice.]

## Skill Version(s):

2.2.5 (source: pyproject.toml, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

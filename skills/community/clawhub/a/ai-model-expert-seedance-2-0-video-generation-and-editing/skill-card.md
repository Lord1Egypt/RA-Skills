## Description:

This skill helps agents use AI-HIVE to submit Seedance2.0 text-to-video, image-to-video, and reference-to-video jobs, upload selected media, poll task progress, and download generated video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce teams, marketing teams, and developers use this skill to create or adapt short-form video assets through AI-HIVE without writing the underlying API workflow themselves. Agents can provide prompts and optional reference media, then submit, track, and retrieve generation jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads an AI-HIVE API key locally and can also accept credentials through command-line arguments or environment variables.

Mitigation: Use environment variables or the local config file with restricted permissions, avoid exposing API keys in prompts or logs, and rotate credentials if they are shared accidentally.

Risk: The skill uploads selected image, video, or audio files to AI-HIVE for generation workflows.

Mitigation: Upload only media that the user has approved for the service and avoid sending confidential or restricted assets unless the endpoint and account are trusted.

Risk: A custom AI_HIVE_BASE_URL or --base-url can redirect API requests to a different endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the replacement endpoint is explicitly trusted and reviewed.

Risk: The documented dependency install uses an unpinned requests package.

Mitigation: Prefer a pinned dependency install in managed environments and review dependency provenance before deployment.

Risk: Implicit invocation is enabled for broad video-generation requests, which may start external content-generation workflows unexpectedly.

Mitigation: Disable or avoid implicit invocation for ambiguous requests, and confirm user intent, budget, media rights, and task parameters before submitting jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-seedance-2-0-video-generation-and-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with CLI commands and JSON snippets; executed jobs may download video files and task outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI-HIVE task IDs for polling and can save generated media to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

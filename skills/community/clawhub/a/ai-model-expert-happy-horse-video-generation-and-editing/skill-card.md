## Description:

AI大模型专家｜HappyHorse 视频生成与编辑 helps creators, video teams, advertisers, and ecommerce operators use AI-HIVE to generate or edit HappyHorse videos from text and optional image, video, or audio references, then track tasks and download results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, advertisers, and video production teams use this skill to generate or edit product, social, TVC, short-drama, and marketing videos through AI-HIVE. The skill is useful when a workflow needs prompt guidance, optional media references, task tracking, and downloaded video results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and user-selected media may be sent through AI-HIVE or a user-supplied endpoint.

Mitigation: Use only the default AI-HIVE endpoint unless the endpoint is fully trusted, avoid setting AI_HIVE_BASE_URL or --base-url for normal use, and do not upload sensitive media unless the account and endpoint are appropriate for that data.

Risk: Video generation and repeated task submission may incur cost.

Mitigation: Check the runtime pricing snapshot and budget before large or high-cost jobs, save task IDs, and poll existing tasks instead of resubmitting after local timeouts.

Risk: Generated or edited videos may create privacy, intellectual property, impersonation, or misleading product-claim issues.

Mitigation: Confirm rights to reference media and brand assets, avoid impersonating real people or copying protected material, and verify product facts and claims before publishing.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-happy-horse-video-generation-and-editing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON task responses, and downloaded media files from the CLI workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI can submit AI-HIVE jobs, upload reference media, poll task IDs, and download generated video outputs to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

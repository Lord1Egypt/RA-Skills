## Description:

This skill helps short-drama and comic-drama teams turn character, scene, story, and brand requirements into reusable character-board visual assets and follow-on image or video generation workflows through AI-HIVE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative, production, brand, ecommerce, and short-drama teams use this skill to plan character boards, storyboards, scene boards, prompts, first-frame assets, and acceptance checks. Developers or operators can also use the bundled scripts to create a project blueprint, submit AI-HIVE image or video jobs, upload reference media, poll tasks, and download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and can store local credential configuration.

Mitigation: Use an isolated environment, keep the API key out of public files and screenshots, restrict local config permissions, and rotate or revoke the key when access is no longer needed.

Risk: Reference images, video, audio, or other media may be uploaded to AI-HIVE during generation workflows.

Mitigation: Upload only media that the user is authorized to process and avoid private, sensitive, or unlicensed material unless disclosure to AI-HIVE is acceptable.

Risk: Generation jobs may incur cost, especially if a timed-out task is resubmitted instead of queried.

Mitigation: Track task IDs, query existing tasks after timeouts, and review model, quantity, pricing snapshot, and routing settings before submitting batches.

Risk: Generated character boards or videos can contain inconsistent identities, inaccurate brand facts, unsafe depictions, or rights-sensitive content.

Mitigation: Review outputs for character consistency, source authorization, factual accuracy, trademarks, age-appropriate treatment, subtitles, platform safe areas, and channel requirements before publication.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-character-board)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands plus JSON blueprints and generated media files when scripts are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI-HIVE API credentials and may upload user-provided media or download generated image/video outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

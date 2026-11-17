## Description:

Ai Video Pro converts creative video descriptions into cinematic, provider-adapted prompts and can optionally route approved prompts to video generation providers such as LumaAI, Runway, Replicate, or ComfyUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaalenwow](https://clawhub.ai/user/aaalenwow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use Ai Video Pro to turn rough video ideas into cinematic prompts with shot, motion, lighting, color, and timing structure. With explicit configuration, they can also generate, preview, transcode, or prepare videos for social publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts or videos may be sent to third-party generation providers or publishing destinations.

Mitigation: Use prompt-only mode for sensitive ideas; before generation or publishing, review the selected provider or destination and confirm that external transfer is intended.

Risk: Publishing and cloud upload features can expose videos through user accounts or storage buckets.

Mitigation: Treat these modes as account actions, use draft or manual review flows where available, and publish only with explicit user authorization.

Risk: Provider, social, and cloud credentials are required for optional high-impact modes.

Mitigation: Use scoped throwaway API tokens where possible, provide credentials through environment variables, and revoke tokens after testing or one-time use.

Risk: Dependency installation can modify the local environment and install large video-generation toolchains.

Mitigation: Run install_deps.py only in an isolated environment after reviewing the selected backend and required packages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaalenwow/skills/ai-video-pro)
- [Cinematic Vocabulary](references/cinematic_vocabulary.md)
- [Platform Publishing Specifications](references/platform_specs.md)
- [Video Generation Provider Matrix](references/provider_matrix.md)
- [Douyin Developer Documentation](https://developer.open-douyin.com/)
- [Weibo Open Platform Documentation](https://open.weibo.com/wiki/)
- [LumaAI Dream Machine API Endpoint](https://api.lumalabs.ai/dream-machine/v1/generations)
- [Runway API Endpoint](https://api.dev.runwayml.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON prompt structures and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default prompt mode is zero-dependency; generation and publishing modes may create local video files or upload media through configured providers.]

## Skill Version(s):

0.2.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

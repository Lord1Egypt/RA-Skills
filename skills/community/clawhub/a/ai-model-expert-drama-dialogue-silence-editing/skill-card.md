## Description:

Helps short-drama, comic-drama, advertising, ecommerce, and paid-media teams turn existing media into rough cuts, refined edits, aspect-ratio variants, and authorized reference-based rewrites using local ffmpeg helpers and AI-HIVE generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative, editing, ecommerce, and paid-media teams use this skill to plan and execute short-video dialogue edits, silence removal, noise/loudness handling, format conversion, and original rewrites based on authorized references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and selected media to a configurable endpoint.

Mitigation: Review or remove base-url override paths, confirm the endpoint before upload or generation, and use least-privilege credentials that can be rotated or revoked.

Risk: Generated or edited short-drama outputs can misuse copyrighted references, likenesses, voices, trademarks, or product claims.

Mitigation: Use only authorized source media and references, require user-confirmed facts for people, products, brands, and claims, and review outputs before publication.

Risk: The release is broader than the advertised editing task and includes media upload, generation, polling, and download behavior.

Mitigation: Prefer explicit invocation, review generated commands before execution, and run uploads or generation only after confirming the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-dialogue-silence-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, ffmpeg outputs, uploaded media references, task IDs, and downloaded generation results when invoked with user-provided credentials and media.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

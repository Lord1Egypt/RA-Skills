## Description:

Provides a short-drama and ecommerce video editing workflow for color consistency, shot matching, multi-platform cuts, auditable ffmpeg commands, and AI-HIVE generation guidance from authorized reference materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External short-drama, comic-drama, ecommerce, advertising, and performance marketing teams use this skill to organize source media, plan rough and fine cuts, convert aspect ratios, normalize audio, and create original rewrites from authorized references. Developers and operators can also use the bundled scripts as auditable helpers for ffmpeg edits and AI-HIVE media generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an AI-HIVE API key for generation workflows.

Mitigation: Use a scoped key where available, keep it out of public files and screenshots, store it in the local environment or protected config, and rotate or revoke it when no longer needed.

Risk: Selected media may be uploaded to AI-HIVE during image or video generation tasks.

Mitigation: Upload only media that the user is authorized to process and that is permitted by the applicable AI-HIVE account and data-handling terms.

Risk: Generated ffmpeg and helper commands can modify or create media files.

Mitigation: Review commands before execution, run them on copies or controlled output paths, and keep source media and timecodes for rollback.

Risk: Implicit invocation could apply the skill to unrelated editing discussions.

Mitigation: Confirm the editing goal, platform, source media, and authorization scope before using the workflow.

Risk: Using unlicensed, confidential, or regulated media can create legal, privacy, or contractual exposure.

Mitigation: Do not use the skill with such media unless rights, consent, and platform data-handling terms have been confirmed.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-color-grade-consistency)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project blueprints, prompts, task IDs, media-processing commands, acceptance checks, and AI-HIVE configuration notes.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

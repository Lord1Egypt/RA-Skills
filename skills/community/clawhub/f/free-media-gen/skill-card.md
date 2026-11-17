## Description:

Free Media Gen is a WorkBuddy/OpenClaw skill for text-to-image and text-to-video generation through configured third-party providers including Agnes, SenseNova, and SiliconFlow Kolors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igenomed](https://clawhub.ai/user/igenomed)

### License/Terms of Use:

MIT

## Use Case:

External WorkBuddy/OpenClaw users use this skill to list configured free media models, generate images or videos through selected third-party providers, and optionally audit the media model registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and configured API keys are used with third-party media providers.

Mitigation: Install only when those providers are intended, avoid sensitive prompts, limit access to models.json, and rotate provider keys as needed.

Risk: External media downloads and provider URLs have weak safeguards in the supplied security evidence.

Mitigation: Review and harden URL allowlisting plus download size and type checks before use with sensitive prompts or valuable API keys.

Risk: Watermark-free media output can create attribution and misuse concerns.

Mitigation: Add confirmation prompts or local usage checks for sensitive requests and label generated media according to the deployment policy.

Risk: Free model availability, pricing, rate limits, and account balance behavior may change.

Mitigation: Run the included model audit flow and confirm provider pricing or quota status before relying on a listed model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igenomed/skills/free-media-gen)
- [WorkBuddy homepage](https://www.workbuddy.cn)
- [Known free media model catalog](artifact/references/model_catalog.md)
- [Media model platform reference](artifact/references/platforms.md)
- [Agnes](https://agnes-ai.cn)
- [SenseNova](https://www.sensenova.cn)
- [SiliconFlow](https://cloud.siliconflow.cn)
- [SiliconFlow pricing](https://www.siliconflow.cn/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON script responses, generated image/video files, and Markdown audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local WorkBuddy model registry credentials and writes generated media or audit reports into the active workspace.]

## Skill Version(s):

1.1.0 (source: frontmatter, README metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

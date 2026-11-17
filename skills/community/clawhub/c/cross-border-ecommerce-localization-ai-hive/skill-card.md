## Description:

This skill helps Amazon, TikTok Shop, independent-store, and global brand teams turn cross-border ecommerce localization needs into localized selling points, platform titles, image copy, video scripts, cultural risk checks, runnable AI-HIVE commands, and reviewable production plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, advertising, and marketing teams use this skill to localize product narratives for target countries, languages, and platforms while preserving factual claims, authorized source materials, brand voice, and platform constraints. Developers can also use the bundled scripts to create project blueprints and submit AI-HIVE image or video generation jobs after reviewing parameters and likely billing impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys for paid media generation workflows.

Mitigation: Use a dedicated revocable API key, keep it out of source files and logs, and review final generation parameters before submitting tasks.

Risk: The skill can upload reference media and download generated image or video files.

Mitigation: Use only authorized input assets, run from an isolated working directory, and review upload and download destinations before execution.

Risk: Custom base URLs and remote downloads increase exposure if endpoint or path handling is misconfigured.

Mitigation: Use the default AI-HIVE endpoint unless there is a reviewed operational need, and inspect generated files before reuse or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/cross-border-ecommerce-localization-ai-hive)
- [AI-HIVE chat and API key access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Chinese workflow sections, inline shell commands, JSON task records, and generated media file paths when tools are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and download generated image or video files after API-backed tasks complete.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

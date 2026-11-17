## Description:

Helps short-drama and manhua production teams plan, generate, and manage reusable cover, poster, title-logo, key visual, thumbnail, and video-ready visual assets through AI-HIVE workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative, brand, ecommerce, acquisition, and localization teams use this skill to turn short-drama cover, poster, title-logo, thumbnail, and video-asset briefs into production blueprints, prompts, generation commands, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or generated requests may be exposed or misdirected if credentials are broad or the AI-HIVE base URL is changed to an untrusted host.

Mitigation: Use a scoped, revocable AI-HIVE API key; keep secrets in local configuration or environment variables; and do not set --base-url or AI_HIVE_BASE_URL to an untrusted host.

Risk: Downloaded generation results may overwrite unintended local paths or place files outside the intended workspace.

Mitigation: Use a dedicated output directory, review output paths before downloading, and prefer --no-download until path handling is fixed.

Risk: Automatic media upload or generation can expose sensitive assets or incur model-generation costs.

Mitigation: Review and confirm each invocation that uploads media or starts generation, verify media rights and budgets first, and retain task IDs for follow-up instead of duplicating jobs.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-cover-poster-logo)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON or media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE image or video generation tasks, upload reference media, query task status, and download generated results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Turns audience comments for serial short dramas, AI comics, ecommerce, advertising, and community campaigns into reviewable story proposals, continuity plans, storyboards, generation tasks, and runnable AI-HIVE helper commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content, ecommerce, marketing, short-drama, AI-comic, and community teams use this skill to transform prior episodes, character and scene bibles, real audience comments, platform constraints, and runtime targets into the next production-ready episode plan. Developers and operators can also use the bundled scripts to create a deterministic project blueprint, call AI-HIVE image or video generation APIs, poll tasks, download outputs, and perform ffmpeg-based video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using real AI-HIVE credentials or sensitive media with the helper clients can expose private keys or files to external services, especially when custom base URLs are allowed.

Mitigation: Use only the official HTTPS AI-HIVE endpoint unless you control the custom endpoint, keep API keys in environment variables or protected config, avoid logging secrets, and upload only media you are willing to send to the provider.

Risk: Generated media calls may incur cost and downloaded outputs may land in unintended locations while destination and filename validation remain limited.

Mitigation: Review prompts, models, routing, and pricing snapshots before execution, use small samples before batch jobs, and prefer --no-download or a dedicated output directory until URL and filename validation are tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/comment-driven-short-drama-ai-hive)
- [AI-HIVE chat and API key entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, inline shell commands, JSON task records, and optional generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing modes, model identifiers, pricing snapshots, task IDs, status records, output paths, and continuity or acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

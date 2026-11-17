## Description:

把汽车功能演示视频需求变成可执行工作流、可运行代码与可交付内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External automotive brands, dealers, media teams, and training teams use this skill to plan Chinese automotive feature demo videos from authorized vehicle assets, official feature facts, channel constraints, and review requirements. It produces reviewable scripts, shot prompts, AI-HIVE generation commands, task records, and acceptance checks before potentially billable generation runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API key can be sent to arbitrary configured endpoints if a custom base URL is used.

Mitigation: Use the default AI-HIVE endpoint or an endpoint you control, and review ~/.ai-hive/config.json before authenticated runs.

Risk: Generated task downloads can write remote result files into a local output directory.

Mitigation: Use --no-download for initial tests or choose a disposable output directory before downloading task results.

Risk: API keys can be exposed through command history, logs, screenshots, or repository files.

Mitigation: Prefer environment or local config storage, keep keys out of prompts and logs, and verify local config file permissions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/automotive-feature-demo-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown responses with inline bash commands and generated JSON task or blueprint files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON files and downloaded media files when the provided scripts are executed; AI-HIVE generation calls may incur cost after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

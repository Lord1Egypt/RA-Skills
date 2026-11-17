## Description:

电商TVC广告片工作室｜AI-HIVE helps brand marketing, ecommerce campaign, and advertising production teams turn product goals, authorized assets, channels, timing, and budget into creative concepts, storyboards, AI-HIVE generation tasks, runnable commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, and advertising teams use this skill to plan Chinese ecommerce TVC and short-form commercial video workflows, including briefs, scripts, shot lists, prompts, AI-HIVE generation commands, task records, and acceptance checks. Developers and operators can also use the included scripts to prepare blueprints, submit AI-HIVE media generation jobs, poll/download results, and perform deterministic ffmpeg edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API bearer key can be sent to any configured base URL.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is fully trusted, and protect API keys in environment variables or the local config file.

Risk: Local media files passed to generation commands may be read and uploaded.

Mitigation: Upload only files the user explicitly selected and has rights to use, especially for reference videos, images, logos, people, and brand assets.

Risk: Image or video generation can incur cost and create repeated charges in batch workflows.

Mitigation: Review prompts, mode, routing, model configuration, and pricing snapshot before submission, then run a small sample before batch generation.

Risk: Generated commercial claims, testimonials, or platform guidance may be misleading if unsupported.

Mitigation: Require source-backed product facts, avoid promised rankings or returns, and review all claims before publication.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/ecommerce-tvc-studio-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, model/routing choices, pricing snapshots, local file paths, and acceptance checklists when generation or editing commands are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

This skill helps short-video advertising teams turn product facts, audience pain points, platform constraints, historical hooks, and banned expressions into Chinese ad-hook matrices, storyboard prompts, AI-HIVE video tasks, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, short-video media buyers, creative directors, and commerce content teams use this skill to generate, test, and review batches of opening-hook variants while keeping the core product claim unchanged. Developers can also run the included scripts to create project blueprints, submit AI-HIVE video generation jobs, and perform deterministic local video checks or aspect-ratio edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real AI-HIVE API keys, prompts, and uploaded media may be sent to an untrusted service if the API base URL is changed.

Mitigation: Use only the official HTTPS AI-HIVE endpoint unless a custom server is fully trusted, run scripts in an isolated environment, and avoid exposing API keys in files, logs, screenshots, or version control.

Risk: Paid image or video generation can be triggered with incorrect parameters or repeated batch submissions.

Mitigation: Review final prompts, mode, routing, model configuration, and price snapshots before execution; start with a small sample and keep task records for deduplication and audit.

Risk: Ad-hook variants can become misleading through unsupported product claims, copied protected material, fake testimonials, or platform-rule evasion.

Mitigation: Use only authorized reference assets, keep factual claims tied to supplied evidence, mark uncertain facts for human review, and do not promise traffic, sales, approval, ranking, or ROI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ad-hook-variant-generator-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with runnable bash examples and optional JSON or media-file outputs when scripts are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project blueprints, storyboard prompts, AI-HIVE task records, price snapshots, task IDs, downloaded files, and validation checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

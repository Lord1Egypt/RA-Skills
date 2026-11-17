## Description:

广告首帧动态化｜AI-HIVE helps ad buyers, short-video directors, and merchants turn a static ad first frame into a reviewable workflow with diagnostics, motion concepts, image-to-video prompts, runnable AI-HIVE commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, ad buyers, short-video directors, and merchants use this skill to convert authorized static ad images or posters into first-frame diagnostics, a focused motion plan, prompts, runnable AI-HIVE generation commands, task records, and platform-oriented acceptance checks. Developers can also use the bundled scripts to create deterministic production briefs, submit AI-HIVE media-generation jobs, poll results, and run local ffmpeg-based video checks or edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be exposed if the API endpoint is overridden or misconfigured.

Mitigation: Use a revocable AI-HIVE API key and keep AI_HIVE_BASE_URL or base_url pinned to the official HTTPS endpoint before running commands.

Risk: Media uploads and generation jobs may trigger paid AI-HIVE activity.

Mitigation: Confirm final prompts, routing mode, uploaded assets, and expected generation steps before each upload or task submission.

Risk: The bundled AI-HIVE helper code is broader than the advertised ad-first-frame workflow.

Mitigation: Review intended subcommands before execution and avoid unrelated chat, image, video, upload, or polling operations unless they are required for the approved task.

Risk: Generated ad content can misstate product facts, authorization, platform rules, or performance expectations.

Mitigation: Require source facts, authorized assets, platform checks, and human review for claims, likenesses, trademarks, AI labels, and acceptance criteria before publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/ad-first-frame-animation-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON-oriented task records, and checklist content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose AI-HIVE API calls, media uploads, asynchronous task polling, downloads, and local ffmpeg operations; generation steps should be reviewed before execution because they may use paid services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

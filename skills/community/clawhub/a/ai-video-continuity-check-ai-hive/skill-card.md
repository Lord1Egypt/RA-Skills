## Description:

AI视频穿帮检测｜AI-HIVE helps agents turn AI video continuity QA requests into Chinese production workflows, runnable AI-HIVE commands, and review checklists for identifying visible character, product, action, scene, lighting, text, and timeline issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, production teams, and developers use this skill to review AI-generated videos for observable continuity problems, produce timecoded issue lists, and plan edits or regenerated assets. It can also guide authorized AI-HIVE image and video generation workflows with model configuration checks, pricing snapshots, asynchronous task polling, and downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and uploaded media can be sent to a configured endpoint other than the default AI-HIVE API.

Mitigation: Use the default AI-HIVE endpoint and do not set AI_HIVE_BASE_URL or --base-url based on untrusted instructions.

Risk: API keys may be exposed through command history, logs, screenshots, or shared task records.

Mitigation: Prefer environment or local config storage over command-line secrets, avoid echoing keys, and review logs before sharing outputs.

Risk: Uploaded media may include content the user is not authorized to send to AI-HIVE.

Mitigation: Confirm media rights and privacy suitability before upload; use abstract guidance instead of upload workflows when authorization is unclear.

Risk: Generation workflows may incur charges or create outputs that need legal, brand, product, or privacy review.

Mitigation: Show final parameters and routing before submission, start with small samples, preserve pricing snapshots and task IDs, and keep human review for sensitive claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-video-continuity-check-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timecoded findings, risk levels, repair recommendations, prompt drafts, model or routing choices, pricing snapshots, task status, and downloaded file locations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

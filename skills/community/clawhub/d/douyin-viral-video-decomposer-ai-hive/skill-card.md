## Description:

This skill helps Douyin merchants, media buyers, directors, and short-video operators turn viral-video analysis into hooks, emotion curves, selling-point beats, voiceover scripts, 9:16 shot lists, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Douyin commerce and short-video teams use this skill to decompose reference videos, redesign them around retention, completion, clicks, and conversion, and produce reviewable Chinese production assets. It can also guide authorized AI-HIVE image or video generation after parameters, routing, and potential cost are confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's AI-HIVE API key to a custom API URL if --base-url or AI_HIVE_BASE_URL is changed.

Mitigation: Use the default AI-HIVE endpoint unless the destination is fully trusted, and inspect ~/.ai-hive/config.json before running paid generation.

Risk: Generation may create paid tasks or upload user media.

Mitigation: Confirm prompts, model, routing mode, price snapshot, and media authorization before submitting generation jobs.

Risk: Reference-video decomposition can drift into unauthorized copying or misleading commercial claims.

Mitigation: Keep only abstract structure from references, require rights to source media, and verify product, brand, price, performance, and endorsement claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/douyin-viral-video-decomposer-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE default API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with Chinese workflow sections, inline shell commands, JSON task records, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE with an API key for model queries, media upload, asynchronous generation, polling, and downloads; deterministic video edits require ffmpeg.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

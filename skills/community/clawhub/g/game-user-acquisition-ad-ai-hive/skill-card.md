## Description:

This skill helps mobile game publishing and user acquisition creative teams turn gameplay evidence, campaign constraints, authorized assets, platform targets, duration, and KPIs into ad concepts, gameplay anchors, hooks, story packaging, video variants, AI-HIVE generation commands, and disclosure checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External game studios, publishers, and user acquisition creative teams use this skill to plan and produce Chinese mobile game ad creative workflows, including reviewable briefs, scripts, shot prompts, AI-HIVE task commands, and acceptance checks. The skill is intended for campaigns grounded in real gameplay, authorized characters or IP, and platform-specific delivery constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied or environment-provided AI-HIVE base URL can receive the bearer API key.

Mitigation: Use only the official AI-HIVE endpoint, avoid untrusted --base-url or AI_HIVE_BASE_URL values, and inspect ~/.ai-hive/config.json before running API commands.

Risk: Image or video generation tasks may incur cost once submitted.

Mitigation: Review final prompts, model choices, routing mode, pricing snapshot, and task parameters before submitting generation jobs; run small samples before batch work.

Risk: Ad creative can mislead users if generated scenes imply gameplay, endorsements, ratings, or IP rights that are not real.

Mitigation: Ground claims in real gameplay and authorized assets, mark unverified facts for review, and keep generated content from impersonating official endorsements or user testimony.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/game-user-acquisition-ad-ai-hive)
- [AI-HIVE Web Console](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections, JSON task records, and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and downloaded media files when the user explicitly runs the bundled scripts with valid AI-HIVE credentials.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps merchants, knowledge accounts, and enterprise content teams plan digital-human talking-video production for AI-HIVE, including scripts, shot and background plans, subtitle highlights, batch variables, and optional video generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, marketing teams, and enterprise content teams use this skill to turn a video topic, factual source material, authorized digital-human assets, platform constraints, and budget posture into a reviewable production workflow and AI-HIVE task plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed to an arbitrary configured server if the base URL is changed.

Mitigation: Use the default AI-HIVE endpoint, avoid --base-url and AI_HIVE_BASE_URL unless the endpoint is fully trusted, and prefer a limited or throwaway API key.

Risk: Downloaded generation results may write outside the intended folder if a malicious API response is involved.

Mitigation: Run downloads in a controlled directory and review commands before execution.

Risk: Video generation can create billable AI-HIVE tasks.

Mitigation: Review final prompts, model mode, routing, and price snapshot before submission; run a small sample before batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/digital-human-talking-video-studio-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown response with optional JSON files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default workflow produces a reviewable plan before any potentially billable generation task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

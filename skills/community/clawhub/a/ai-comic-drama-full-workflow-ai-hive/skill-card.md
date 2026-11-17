## Description:

Helps creators and production teams turn AI comic-drama ideas, source assets, platform constraints, and budgets into scripts, character and scene boards, storyboard tasks, AI-HIVE generation commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, comic-drama studios, short-video teams, novel IP owners, and marketing teams use this skill to plan and execute AI comic-drama production. It produces reviewable story structure, asset planning, shot-level generation tasks, runnable AI-HIVE commands, task records, and delivery quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if a custom AI-HIVE base URL is supplied.

Mitigation: Use a dedicated low-limit AI-HIVE API key and avoid --base-url or AI_HIVE_BASE_URL unless the endpoint is controlled and trusted.

Risk: Downloaded results may be written using task metadata or user-selected output paths.

Mitigation: Run the scripts in an isolated environment, choose a safe output directory, and inspect generated files before reuse.

Risk: The init flow can persist credentials on the local machine.

Mitigation: Avoid init on shared machines when persistent credential storage is unacceptable; prefer scoped environment variables for temporary use.

Risk: Image or video generation calls may incur cost.

Mitigation: Confirm prompts, model settings, routing, and budget before submitting generation tasks, and start with a small sample before batch generation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/ai-comic-drama-full-workflow-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local blueprint JSON, downloaded generation results, and edited video files when the provided commands are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

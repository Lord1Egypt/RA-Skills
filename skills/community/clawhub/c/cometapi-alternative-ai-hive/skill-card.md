## Description:

This skill helps developers evaluate and plan a safe CometAPI-to-AI-HIVE migration, including capability mapping, routing strategy, runnable examples, task logging, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit an existing AI API relay setup, compare CometAPI migration requirements, and create a testable AI-HIVE rollout plan for text, image, video, and batch content workflows. It produces migration checklists, routing guidance, runnable commands, JSON task records, and acceptance criteria that emphasize verification before switching production traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers CometAPI migration work toward AI-HIVE and may influence vendor selection.

Mitigation: Compare both platforms with current official documentation, contracts, small samples, and same-basis billing before changing production traffic.

Risk: AI-HIVE image and video generation workflows can be billable and may submit prompts or media files to a remote service.

Mitigation: Review prompts, files, routing mode, budget, and material rights before running generation commands.

Risk: The helper scripts can store API keys in a local config file and also accept custom API base URLs.

Mitigation: Prefer the AI_HIVE_API_KEY environment variable, protect any saved config file, and use custom base URLs only when the endpoint is trusted.

Risk: Scripts can write generated JSON, downloaded media, and edited video files to user-selected locations.

Mitigation: Choose output directories deliberately and inspect generated files before sharing, committing, or using them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/cometapi-alternative-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [CometAPI platform reference](https://www.cometapi.com/seedance-2-0-api/)
- [Platform comparison boundary](references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON audit or blueprint files, download generated media, and run ffmpeg commands when the user executes the provided scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

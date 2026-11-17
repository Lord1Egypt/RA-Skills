## Description:

This skill helps short drama, comic, brand, e-commerce, advertising, and international teams convert costume styling, character, scene, story, and brand requirements into reusable visual assets and follow-on video workflows through AI-HIVE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, studios, brand marketers, e-commerce teams, and developers use this skill to plan short-drama costume and visual styling, produce reusable character or scene boards, generate prompts and assets, and prepare image-to-video workflows. It is intended for commercial creative production where users review source facts, rights, platform requirements, and generated outputs before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill has under-scoped credential and endpoint behavior around AI-HIVE API use.

Mitigation: Review the skill before installation, use it only when AI-HIVE access is intended, and use a limited or revocable API key where possible.

Risk: The skill may upload selected media and sends requests to a configurable AI-HIVE API endpoint.

Mitigation: Upload only media the user is authorized to process and do not set AI_HIVE_BASE_URL or --base-url to an untrusted endpoint.

Risk: Runtime dependencies and API behavior may vary across local environments.

Mitigation: Install dependencies in an isolated environment with pinned versions before using the image or video generation scripts.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-costume-styling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project blueprints, prompts, task IDs, asset references, image or video generation commands, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

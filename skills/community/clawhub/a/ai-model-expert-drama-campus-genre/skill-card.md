## Description:

This skill helps short-drama and comic-drama teams turn campus drama ideas, scripts, character images, or reference videos into production briefs, storyboard assets, generation commands, and AI-HIVE media outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama studios, brand teams, e-commerce teams, and developers use this skill to plan campus-themed short drama or comic-drama projects and generate structured AI-HIVE commands, assets, and delivery checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and uploaded media may be sent to an unintended or weakly scoped endpoint.

Mitigation: Review commands before execution, use only the official AI-HIVE endpoint unless another deployment is intentionally trusted, and avoid accepting --base-url or AI_HIVE_BASE_URL values from untrusted sources.

Risk: Generated workflows may store a local API key and download generated files to the configured output directory.

Mitigation: Use a revocable low-limit API key, protect the local configuration file, and upload only media that is appropriate to send to the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-campus-genre)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project blueprints, prompts, task IDs, model or route selections, pricing snapshots, and generated media file references.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

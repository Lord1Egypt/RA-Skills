## Description:

AI大模型专家｜短剧BGM智能配乐 helps short-drama, comic-drama, advertising, e-commerce, campaign, and multi-platform operations teams turn existing media into rough cuts, refined edits, vertical variants, campaign versions, and original rewrites based on authorized reference structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, studios, advertisers, e-commerce teams, and developers use this skill to plan short-drama BGM/editing workflows, inspect source media, generate production blueprints, prepare ffmpeg edit commands, and call AI-HIVE image/video generation for authorized media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an AI-HIVE API key and upload selected media to AI-HIVE.

Mitigation: Use only media you are authorized to upload, prefer environment variables for credentials, and review upload targets before running generation commands.

Risk: The skill supports a configurable API base URL.

Mitigation: Keep the default AI-HIVE endpoint unless you fully trust the replacement endpoint.

Risk: Generated tasks may create cost-bearing outputs or download generated media.

Mitigation: Review model, routing mode, pricing snapshot, output directory, and download behavior before submitting or polling tasks.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-bgm-smart-scoring)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON blueprints, inline shell commands, and generated media task metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local edit commands, project blueprint files, AI-HIVE task IDs, and downloaded media outputs when the user runs the provided scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

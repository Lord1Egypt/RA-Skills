## Description:

短剧剧本创作技能。多代理流水线从创意到完整短剧剧本（立项→人物小传→故事概要→逐集概要→逐集剧本），支持子代理/主代理直出双模式、断点续跑与修改。当用户需要创建、修改或续跑短剧项目时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and writing teams use this skill to plan, draft, revise, and resume Chinese short-drama projects from an initial idea through character profiles, story outlines, episode outlines, and screenplay files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow scans the active workspace for existing drama projects and drafts.

Mitigation: Run it in a dedicated workspace when existing project files should not be inspected.

Risk: The workflow creates, updates, and manages local project files.

Mitigation: Review generated files before reuse and keep project work in a workspace where these file changes are expected.

Risk: Character guidance includes a rigid binary gender-balance rule.

Mitigation: Review character outputs for inclusivity and adjust gender representation requirements to fit the project.

## Reference(s):

- [Drama Script Skill Page](https://clawhub.ai/linhongbijkm-dot/skills/drama-script)
- [Master Setup Manual](references/master-setup.md)
- [Common Agent Rules](references/common-agent-rules.md)
- [Checkpoint Resume](references/checkpoint-resume.md)
- [Character Profile Agent Manual](references/agents/agent-character-profile.md)
- [Story Bible Agent Manual](references/agents/agent-story-bible.md)
- [Episode Outline Agent Manual](references/agents/agent-episode-outline.md)
- [Screenplay Agent Manual](references/agents/agent-screenplay.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown project files and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local short-drama project files in the active workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

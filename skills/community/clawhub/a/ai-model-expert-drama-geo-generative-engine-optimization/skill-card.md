## Description:

Helps drama, manga, brand, e-commerce, marketing, and AI search teams turn GEO work into executable planning, evidence fields, structured content, and AI-HIVE image and video generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, e-commerce teams, marketers, and AI search operators use this skill to plan GEO-oriented content, build verifiable answer and source structures, create project blueprints, and run AI-HIVE image or video generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the AI-HIVE generation scripts can send selected prompts and media files to AI-HIVE.

Mitigation: Avoid uploading sensitive or unlicensed media, and confirm authorization for people, brands, products, source materials, voices, and music before generation.

Risk: The init flow can store an AI-HIVE API key locally for later API calls.

Mitigation: Use a scoped and revocable API key, keep the local config file private, and rotate the key if it is exposed.

Risk: Image and video generation tasks can incur costs or create duplicate work if tasks are resubmitted after timeouts.

Mitigation: Review pricing snapshots before submitting jobs, retain task IDs, and query existing tasks before retrying.

Risk: GEO and AI search outputs may contain stale or unsupported claims, and the skill does not guarantee model indexing, ranking, or citation.

Mitigation: Use confirmed facts and source timestamps, mark unknowns clearly, and review generated answers, media, subtitles, and evidence fields before publication.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-geo-generative-engine-optimization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs, upload selected media, poll task status, and download generated assets when configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

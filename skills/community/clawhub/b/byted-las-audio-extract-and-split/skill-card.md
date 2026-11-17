## Description:

Extracts audio tracks from supported video files and splits long audio into timed segments using Volcengine LAS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to extract audio from local or TOS-hosted media files, convert output formats, and split recordings such as lectures or podcasts into fixed-duration clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or upgrade remote SDK code during use.

Mitigation: Run it in an isolated workspace and pin or pre-review the SDK wheel before processing user media.

Risk: The skill handles LAS and TOS credentials for cloud media processing.

Mitigation: Use least-privilege, revocable credentials and avoid storing live keys in project-local files unless permissions and source-control exclusions are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-audio-extract-and-split)
- [LAS audio extract and split API reference](references/api.md)
- [Skill pricing reference](references/prices.md)
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces TOS output paths for generated audio segments and requires price-estimate disclosure before execution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

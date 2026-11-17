## Description:

Byted Las Video Edit helps agents use Volcengine LAS to extract and trim video clips from long videos based on natural-language descriptions and optional reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run Volcengine LAS video-edit jobs that find scenes, people, objects, or actions in video and return clipped segments.

### Deployment Geography for Use:

China LAS regions cn-beijing and cn-shanghai

## Known Risks and Mitigations:

Risk: Normal setup can install mutable remote SDK code from the Volcengine-hosted update path.

Mitigation: Install only if the publisher and SDK source are trusted, review or disable automatic SDK updates, and run the skill in an isolated workspace.

Risk: A background polling helper executes the project-root .env file as shell.

Mitigation: Keep the project .env file trusted and controlled, prevent untrusted content from writing to it, and use narrowly scoped LAS/TOS credentials.

Risk: The workflow uses LAS and TOS credentials and writes clip outputs to a user-provided TOS path.

Mitigation: Use least-privilege credentials, verify that LAS_REGION matches the API key and bucket region, and provide only a user-controlled writable TOS output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-video-edit)
- [las_video_edit API quick reference](references/api.md)
- [Volcengine las_video_edit API documentation](https://www.volcengine.com/docs/6492/2221469?lang=zh)
- [Volcengine LAS pricing reference](references/prices.md)
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets; completed jobs produce JSON, CSV, and clip URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LAS_API_KEY, LAS_REGION, and a user-writable TOS output path; asks for billing confirmation before job submission.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

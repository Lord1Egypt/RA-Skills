## Description:

AI Video Creator helps an agent plan short-form video topics, create Jimeng AI video prompts, assemble vertical clips with overlay text and background music, and optionally publish the result to Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameswangchen](https://clawhub.ai/user/jameswangchen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social-media operators use this skill to generate short vertical video concepts, captions, tags, and assembled video files for Xiaohongshu posting. Developers can also run the included Python and ffmpeg pipeline directly when the required Volcengine credentials, BGM assets, and publishing service are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses Volcengine API credentials and a logged-in Xiaohongshu publishing service.

Mitigation: Install and run it only in environments where those credentials and publishing permissions are intended for use.

Risk: Generated titles, captions, tags, and videos can be posted publicly to Xiaohongshu.

Mitigation: Review generated content before publishing and use private, draft, or limited visibility during testing.

Risk: The setup depends on an external Xiaohongshu MCP binary and Python dependencies.

Mitigation: Verify or pin the MCP binary and Python dependency versions before deployment.

Risk: Some documented shell snippets interpolate generated text into commands.

Mitigation: Prefer structured JSON writing and argument-array execution for untrusted generated content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jameswangchen/skills/ai-video-creator)
- [Setup Guide](references/setup.md)
- [Volcengine Jimeng API Documentation](https://www.volcengine.com/docs/85621/1544715)
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance, JSON content plans, shell commands, and generated MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include prompt JSON, generated video clips, a final MP4, local metadata, Xiaohongshu title/caption/tag text, and publish status.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

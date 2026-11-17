## Description:

Publishes trusted HTML or Markdown content to Bilibili article or Tribee targets with login checks, title handling, editor insertion, and publishing steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zangzhicong](https://clawhub.ai/user/zangzhicong)

### License/Terms of Use:

MIT-0

## Use Case:

Content publishers and operators use this skill to publish trusted HTML or Markdown files to Bilibili articles or Tribee posts from an authenticated OpenClaw browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly from an authenticated Bilibili account.

Mitigation: Manually verify the account, target, visibility, title, body, and publish settings before allowing the final publish action.

Risk: Referenced local images can be read from disk and embedded into the published post.

Mitigation: Use only trusted input files and review embedded images in the processed output before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zangzhicong/skills/bili-sunflower-publish)
- [Publisher profile](https://clawhub.ai/user/zangzhicong)
- [Bilibili article editor](https://member.bilibili.com/york/read-editor)
- [Bilibili Tribee publish URL pattern](https://www.bilibili.com/bubble/publish?tribee_id={id}&tribee_name={name})

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create preprocessed temporary HTML or Markdown files before browser-based publishing]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

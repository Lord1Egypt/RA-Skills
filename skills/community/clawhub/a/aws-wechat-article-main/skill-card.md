## Description:

Orchestrates a WeChat Official Account content workflow from topic selection through drafting, review, formatting, images, and draft or publication handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

Content editors, self-media operators, and brand teams use this skill as the entry point for a multi-skill WeChat article pipeline. It coordinates environment checks, article setup, drafting, review, formatting, image handling, and publishing posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default WeChat API base can send credential-backed publishing traffic through a third-party proxy.

Mitigation: Set wechat_api_base to the official WeChat endpoint, or use a proxy only after explicitly trusting its operator and accepting that credentials, tokens, unpublished article content, and publishing requests may pass through it.

Risk: The workflow depends on secrets for writing, image generation, and WeChat publishing.

Mitigation: Store secrets only in aws.env, do not paste them into chat, and use publish_method: none when only local drafting is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-main)
- [Publisher profile](https://clawhub.ai/user/aiworkskills)
- [Project homepage](https://aiworkskills.cn)
- [First-time setup](references/first-time-setup.md)
- [Configuration field schema](references/articlescreening-schema.md)
- [Configuration example](references/config.example.yaml)
- [Environment example](references/env.example.yaml)
- [Writing specification example](references/writing-spec.example.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates local draft files, article metadata, generated HTML, image assets, and publishing state through companion skills when installed.]

## Skill Version(s):

1.0.27 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

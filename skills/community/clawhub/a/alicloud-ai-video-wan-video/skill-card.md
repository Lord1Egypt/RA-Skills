## Description:

Generate videos with Model Studio DashScope SDK using Wan i2v models (wan2.6-i2v-flash, wan2.6-i2v, wan2.6-i2v-us).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement or document Alibaba Cloud DashScope Wan video generation flows, including normalized video.generate requests, SDK setup, polling, and response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DashScope prompts, reference images, generated image URLs, and video URLs may be transmitted to or received from Alibaba Cloud services.

Mitigation: Use the skill only for content appropriate for Alibaba Cloud DashScope, and review prompts and reference media before execution.

Risk: API keys can be read from environment variables, .env files, or ~/.alibabacloud/credentials.

Mitigation: Use a dedicated DashScope API key, keep credential files private, and avoid checking local secrets into source control.

Risk: The dancing video helper includes opinionated default prompt expansion when no separate image prompt is supplied.

Mitigation: Review or override the generated image prompt before running that helper in user-facing workflows.

## Reference(s):

- [DashScope SDK Reference (Wan Video)](artifact/references/api_reference.md)
- [Source List](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash snippets, JSON request and response shapes, and optional generated media files when helper scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DashScope credentials and may send prompts, reference images, and generated media URLs to or from Alibaba Cloud services.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

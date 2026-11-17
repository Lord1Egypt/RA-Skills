## Description:

AI-powered content creation suite for generating slides, documents, diagrams, websites, data visualizations, reports, financial analysis, images, and related assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertilico2001](https://clawhub.ai/user/supertilico2001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Anygen CLI workflows for generating and modifying content assets such as presentations, documents, diagrams, websites, analyses, and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference files may be sent to Anygen during task preparation and generation.

Mitigation: Use only prompts and files approved for Anygen processing, and avoid submitting confidential material unless the environment and service terms allow it.

Risk: The Feishu/Lark delivery path may read local app credentials and use API calls to upload and send files.

Mitigation: Run only where those credentials are intended for agent use, protect logs, and confirm recipient and file scope before delivery.

Risk: The release depends on the external @anygen/cli package and an ANYGEN_API_KEY.

Mitigation: Review the CLI package source and version before installation, and scope the API key to the minimum permissions needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supertilico2001/skills/anygen-workflow-generate)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Anygen task download related skill](../anygen-task-download/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloadable generated files, thumbnail previews, task URLs, and modification guidance through the Anygen CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

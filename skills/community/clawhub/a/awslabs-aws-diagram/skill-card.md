## Description:

Helps agents generate AWS architecture diagrams and related diagram assets by routing diagram code, examples, and icon-list requests to a configured XiaoBenYang API service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud architects use this skill to generate PNG architecture diagrams, retrieve diagram examples, and list available diagram icons from an external API-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends diagram requests and workspace path metadata to an external XiaoBenYang API service.

Mitigation: Use only in workspaces where that metadata is acceptable to disclose, and review request content before invoking remote tools.

Risk: The skill stores the XiaoBenYang API key in a local .env file as plaintext.

Mitigation: Avoid committing .env, restrict file access, and prefer safer secret storage before production use.

Risk: The evidence reports a mismatch between the AWS diagram purpose and Gaokao/XiaoBenYang configuration details.

Mitigation: Review the service configuration and publisher intent before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/awslabs-aws-diagram)
- [ClawHub publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries with JSON-backed tool results and generated diagram file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagram generation can produce PNG files in a workspace directory when the external API succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Generates PPT presentation content from a user's requirements or uploaded-document content, helps select a template, and returns a jcppt preview/download link through the AIPPT service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skeyjia6](https://clawhub.ai/user/skeyjia6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to turn topic requests or parsed document content into a structured Markdown outline, choose a presentation template, and generate a PPT preview/download link from the AIPPT service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown, including content derived from user documents, is sent to the third-party jcppt/7niuai PPT service.

Mitigation: Use the skill only with content approved for that service and avoid sensitive or confidential inputs unless the service is trusted for the use case.

Risk: The skill requires AIPPT_ACCESS_TOKEN for authenticated generation requests.

Mitigation: Store the token only in the environment, do not commit or paste it into chats or screenshots, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skeyjia6/skills/aippt)
- [Publisher profile](https://clawhub.ai/user/skeyjia6)
- [AIPPT official site](https://www.jcppt.com/)
- [AIPPT API documentation](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PPT preview/download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AIPPT_ACCESS_TOKEN; generated Markdown and any document-derived content are sent to the third-party AIPPT/jcppt service.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

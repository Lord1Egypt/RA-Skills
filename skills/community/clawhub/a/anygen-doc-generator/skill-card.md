## Description:

Use this skill when a user wants to create, draft, or generate a structured written document or report through the AnyGen CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route document and report generation requests to AnyGen, including market research reports, technical design documents, PRDs, proposals, meeting summaries, white papers, and executive summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document prompts and generated content may be sent to AnyGen for server-side processing.

Mitigation: Use only with data your organization permits to be processed by AnyGen; avoid confidential, regulated, or customer data unless approved.

Risk: The skill can install or rely on additional tooling, including the AnyGen CLI and anygen-workflow-generate skill.

Mitigation: Review and pin the CLI package and dependent skill before allowing automatic installation in managed environments.

Risk: Generated documents may contain incorrect, incomplete, or unsupported claims.

Mitigation: Have a human reviewer verify factual, legal, financial, technical, and business-critical content before use.

## Reference(s):

- [Doc Generator on ClawHub](https://clawhub.ai/logictortoise/skills/anygen-doc-generator)
- [logictortoise ClawHub profile](https://clawhub.ai/user/logictortoise)
- [AnyGen service](https://www.anygen.io)
- [AnyGen CLI package](npm:@anygen/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text documents, with inline shell commands and configuration guidance when setup is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the AnyGen CLI and an ANYGEN_API_KEY or AnyGen CLI browser login.]

## Skill Version(s):

3.0.0 (source: server release evidence, released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

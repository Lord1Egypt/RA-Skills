## Description:

Guides agents through 2Ryun domestic-site REST API workflows for importing documents, managing knowledge bases, searching structured knowledge, generating and publishing web pages, taking notes, and uploading assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iguoguo](https://clawhub.ai/user/iguoguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent operate 2Ryun's domestic REST API for document import, knowledge-base search, page generation and publishing, notes, and asset uploads while applying the documented API-key, extraction, and retry rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad access to a user's 2Ryun account, including upload, publish, update, delete, and extraction operations.

Mitigation: Use a narrowly scoped, revocable API key and require explicit confirmation of files, titles, IDs, and visibility before state-changing actions.

Risk: Returned attachment URLs and published-page URLs may be publicly accessible.

Mitigation: Confirm publication intent and visibility before publishing or sharing returned URLs.

Risk: Long-lived API keys could be exposed if pasted into ordinary chat.

Mitigation: Use a safer secret mechanism when available and avoid placing persistent credentials directly in prompts.

## Reference(s):

- [2Ryun REST API technical specification (Chinese)](artifact/2ryun-api-spec-cn.md)
- [ClawHub skill page](https://clawhub.ai/iguoguo/skills/2ryun-skill-cn)
- [Server-resolved source repository](https://github.com/iguoguo/2Ryun-skill-cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with REST API examples, curl commands, and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce 2Ryun document IDs, generation IDs, and public URLs returned by the service.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

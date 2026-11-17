## Description:

Manage Felo LiveDocs (knowledge bases) and their resources. Use when users want to create, manage, or query knowledge bases, upload documents, add URLs, or perform semantic retrieval over a knowledge base. Explicit commands: /felo-livedoc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage Felo LiveDoc knowledge bases from an agent workflow, including creating LiveDocs, adding documents or URLs, retrieving relevant content, and managing resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete LiveDocs and LiveDoc resources.

Mitigation: Require explicit user confirmation before delete and remove-resource commands, and verify the short_id and resource_id before execution.

Risk: The skill can upload files, URLs, and text into a Felo knowledge base.

Mitigation: Avoid uploading secrets, credentials, regulated data, or unapproved third-party content unless the user confirms the destination and data handling are acceptable.

Risk: An API-base override could send the Felo API key and uploaded content to an unintended server.

Mitigation: Keep FELO_API_BASE unset or confirm it points only to the legitimate Felo API before running the skill.

Risk: The skill needs Felo API authority through FELO_API_KEY.

Mitigation: Use a scoped or revocable API key where available and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/felo-livedoc)
- [Publisher Profile](https://clawhub.ai/user/wangzhiming1999)
- [Felo](https://felo.ai)
- [Felo Skills Repository](https://github.com/Felo-Inc/felo-skills)
- [Felo Skills Issues](https://github.com/Felo-Inc/felo-skills/issues)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown summaries or raw JSON from Felo API responses, with shell commands for execution and setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY; supports optional JSON output and request timeout settings.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

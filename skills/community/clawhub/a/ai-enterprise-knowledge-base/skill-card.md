## Description:

AI Enterprise Knowledge Base helps agents guide setup of an internal enterprise question-answering knowledge base with document upload, semantic retrieval, access control, and multi-channel integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IT teams use this skill to set up or evaluate an internal enterprise knowledge-base Q&A service for company documents, including retrieval, permissions, and chat-platform access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive company documents and credentials, while storage, retention, sharing, and data-flow details are under-specified.

Mitigation: Confirm where documents, embeddings, prompts, answers, and chat messages are stored, retained, and shared before uploading private business data.

Risk: The setup flow depends on installing OpenClaw source code and configuring API tokens or Feishu secrets.

Mitigation: Use an isolated, unprivileged install environment, pin or verify the OpenClaw source revision, and protect tokens and chat-platform secrets with least-privilege access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-enterprise-knowledge-base)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, YAML, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, configuration examples, and API request examples for an enterprise knowledge-base workflow.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/package.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

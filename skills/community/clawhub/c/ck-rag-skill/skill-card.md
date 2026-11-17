## Description:

Queries a RAGFlow knowledge base to answer technical, troubleshooting, operations, Docker/container, and development questions, then summarizes actionable guidance from the returned sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenkun-nuaa](https://clawhub.ai/user/chenkun-nuaa)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to query a RAGFlow knowledge base for technical Q&A, fault diagnosis, and operational guidance, especially for container, Docker, system administration, and development scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships reusable session credentials.

Mitigation: Rotate the exposed token and session cookie, then move credentials to secure per-user configuration before installation.

Risk: User questions are sent over plaintext HTTP to a fixed internal endpoint.

Mitigation: Use the skill only in a trusted internal environment and switch the endpoint to HTTPS before sending secrets or sensitive operational details.

Risk: A shared conversation ID can retain or mix context across users or sessions.

Mitigation: Use per-user or per-session conversation IDs and avoid sending sensitive operational details until session handling is isolated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenkun-nuaa/skills/ck-rag-skill)
- [RAGFlow Skill Troubleshooting Guide](TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with summarized answers, optional inline shell commands, source document names, and query status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses streaming responses and may take 5-10 seconds for typical answers, with longer timeouts for complex questions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

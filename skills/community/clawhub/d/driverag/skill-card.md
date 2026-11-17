## Description:

Use the Google Drive RAG CLI to search your synced personal documents, add tracking folders, or check the service account status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query, sync, and inspect a Google Drive backed RAG index of their personal documents through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles JWT credentials and personal document queries for a Google Drive RAG service.

Mitigation: Use only a trusted HTTPS API endpoint, treat the JWT as a secret, and restrict permissions on the local .env file.

Risk: Indexed personal documents may be processed by the RAG API.

Mitigation: Avoid indexing highly sensitive documents unless the user is comfortable with the service processing them.

Risk: Token renewal and sync operations can affect access credentials or re-index document content.

Mitigation: Require explicit confirmation before token renewal or sync operations, and review forced re-indexing before use.

Risk: Unpinned dependencies and local environment setup can change runtime behavior over time.

Mitigation: Pin dependencies before deployment and review the installed packages in the virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/driverag)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses should include citations and source documents exactly as returned by the CLI.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Search, retrieve, log, and manage past conversations, research, tasks, files, and delegated jobs in a persistent Second Brain knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeangraves](https://clawhub.ai/user/ryandeangraves)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query and update a personal knowledge base, manage Kanban tasks and files, and delegate jobs to sub-agents through HTTP API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published skill includes a reusable API key for a personal remote knowledge base.

Mitigation: Rotate or revoke the shared key before use, and require per-user least-privilege credentials.

Risk: The skill can read, write, upload, delete, and delegate work through remote API calls.

Mitigation: Require explicit user approval for uploads, deletes, and delegation, and limit allowed operations to the task at hand.

Risk: The skill may send local files or conversation context to the remote service.

Mitigation: Define clear limits on what files and context may be transmitted, and redact sensitive information before any upload or logging action.

## Reference(s):

- [Brain Search on ClawHub](https://clawhub.ai/ryandeangraves/skills/brain-search)
- [Publisher profile](https://clawhub.ai/user/ryandeangraves)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and remote API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live HTTP responses, task identifiers, file identifiers, and entries returned by the remote service.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Semantic code caching for AI agents. Cache, retrieve, and reuse code from prior agent executions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryx2](https://clawhub.ai/user/ryx2)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to search for, retrieve, upload, and vote on reusable code snippets through the Raysurfer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved code may be written into the local filesystem and could overwrite existing files.

Mitigation: Use a constrained workspace and review retrieved files before running or merging them.

Risk: Uploaded files are sent to Raysurfer and may contain secrets or proprietary code.

Mitigation: Upload only files intentionally approved for sharing with Raysurfer and remove secrets before upload.

Risk: Server-provided prompt text may influence an agent if treated as instructions.

Mitigation: Treat downloaded prompts and code as untrusted evidence until inspected by the user or agent policy.

## Reference(s):

- [Code Cache ClawHub Page](https://clawhub.ai/ryx2/skills/code-cache)
- [Raysurfer](https://raysurfer.com)
- [Raysurfer Documentation](https://docs.raysurfer.com)
- [Raysurfer API Keys](https://raysurfer.com/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration]

**Output Format:** [Markdown and CLI text with code snippets, file paths, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAYSURFER_API_KEY and may write retrieved code files to a local cache directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

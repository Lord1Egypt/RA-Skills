## Description:

Semantic code caching for AI agents. Cache, retrieve, and reuse code from prior agent executions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryx2](https://clawhub.ai/user/ryx2)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to search, retrieve, upload, and vote on reusable code snippets through the Raysurfer API so similar agent coding tasks can reuse prior execution artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved code may come from third-party cache content and may be unsafe to run directly.

Mitigation: Use disposable or tightly sandboxed environments and inspect every retrieved file before execution.

Risk: API-provided prompt additions may include untrusted instructions.

Mitigation: Review prompt additions as data and do not paste them into an agent as instructions without approval.

Risk: Uploading files can expose local source code, secrets, or proprietary data to an external service.

Mitigation: Avoid uploading confidential repositories, redact sensitive content, and confirm file paths before upload.

## Reference(s):

- [ClawHub Code Reputation skill page](https://clawhub.ai/ryx2/skills/code-reputation)
- [Raysurfer homepage](https://raysurfer.com)
- [Raysurfer documentation](https://docs.raysurfer.com)
- [Raysurfer API reference](https://docs.raysurfer.com/api-reference)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown command output, with retrieved code files optionally written to disk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAYSURFER_API_KEY and access to the Raysurfer API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

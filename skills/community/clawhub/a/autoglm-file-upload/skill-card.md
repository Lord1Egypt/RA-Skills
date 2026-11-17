## Description:

Use the AutoGLM Upload Mix API to upload local files such as images and documents, then obtain a file URL or resource ID for downstream API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khurramjamil12](https://clawhub.ai/user/khurramjamil12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload an intended local image or document to AutoGLM and reuse the returned URL or resource information in downstream API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local files to AutoGLM using a local bearer token.

Mitigation: Use it only for files intentionally selected for AutoGLM upload, and avoid sensitive documents unless the service and storage behavior are trusted.

Risk: Returned file URLs may make uploaded content accessible to downstream workflows.

Mitigation: Pass returned URLs only to tools and workflows that are allowed to access the uploaded content.

Risk: The release security summary notes a hard-coded signing key and limited scoping or consent controls.

Mitigation: Review before installing; prefer releases that add explicit consent checks, tighter file and path scoping, and remove or rotate the embedded signing key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khurramjamil12/skills/autoglm-file-upload)
- [AutoGLM Upload Mix API endpoint](https://autoglm-api.autoglm.ai/agentdr/v1/assistant/upload-mix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns AutoGLM upload response data, including file URL or resource identifiers when the upload succeeds.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

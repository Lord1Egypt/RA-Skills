# Artifact Acceptance and Handoff

Load this reference for image, video, audio, file, webpage, data, or report outputs.

## Principle

A generated result is useful when the calling agent can consume it. Response prose is not an Artifact.

The agent should normally use the Artifact in the user's requested workflow rather than merely report a path.

Examples:

- insert the image into a document or website;
- replace the old asset in an app;
- attach the video to the project;
- use the audio file in the requested edit;
- read a research report and cite it;
- pass a generated file to another tool.

## Minimum Structured Contract

```text
artifact_id
kind
state
uri or local_path
mime_type
size_bytes
width / height when relevant
duration_seconds when relevant
source_chat_id when available
requested_backend
effective_backend
observed_backend
verification.status
```

Keep requested, routed/effective, and observed backend evidence separate.

## State Semantics

- `local` — a local file is available.
- `remote` — a usable remote URI is available but is not automatically a local file.
- `queued` — generation has started; no completed Artifact exists yet.
- `partial` — an upstream result exists but local save or verification is incomplete.
- `empty` — no usable Artifact was observed.
- `failed` — the operation failed.

Do not convert `queued`, `partial`, or `empty` into completed success.

## Local File Verification

Before treating a local Artifact as complete:

1. resolve the path;
2. confirm it exists;
3. confirm it is a regular non-empty file;
4. confirm it is inside the requested destination when a destination was specified;
5. inspect MIME/type;
6. inspect dimensions for images;
7. inspect duration when available for audio/video;
8. preserve the structured verification result.

## Resource Links

When the MCP client supports resource links or embedded resources, prefer returning them alongside structured metadata. The local path remains a practical fallback for local stdio agents.

Do not base workflow completion on whether a particular chat UI renders the preview. The Artifact contract is the source of truth.

## Agent Handoff

### Search and Understanding

These normally return information to the calling agent. Synthesize it and continue the task. A file is optional unless the user asked for a durable deliverable.

### Image, Video, and Music

These normally return files or resource links. Use them in the next step. Do not end with only “saved to …” when the user's request includes a downstream use.

### Deep Research

Prefer a Markdown report Artifact plus structured operation/source metadata. The calling agent should read the report, extract conclusions and sources, and create the user's requested deliverable.

## Failure Handoff

When the Artifact is unavailable, return:

```text
state
error code
retryability
observed upstream identifiers
what evidence exists
the next recovery action
```

Do not invent a local file, MIME type, duration, dimensions, or backend identity.

## Description:

Upload or download Agentcadia agent drafts through deterministic command-style workflows for syncing local OpenClaw-style workspaces, writing back metadata, or pulling remote agent packages into a local workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ideaforceai-sys](https://clawhub.ai/user/ideaforceai-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to move Agentcadia agent workspaces between a local OpenClaw-style workspace and Agentcadia. It supports upload tasks that require metadata writeback and download tasks that place or extract a remote agent package locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads can send unintended workspace content to Agentcadia if the local workspace contains secrets or unrelated files.

Mitigation: Run uploads from a clean workspace that contains only intended files, and remove secrets from root markdown files and skill directories before use.

Risk: Downloads place remote content and filenames into the local workspace, and overwrite mode can replace existing files.

Mitigation: Use downloads only from a trusted Agentcadia origin and task, inspect the destination first, and enable overwrite only after reviewing the files that may be replaced.

Risk: Share images, captions, links, and runtime actions returned by the remote service may be untrusted remote content.

Mitigation: Review remote owner-facing content before relaying it, expose only public detail links or public share image URLs, and avoid leaking upload tokens or internal upload URLs.

## Reference(s):

- [OpenClaw Runtime Integration](references/openclaw-runtime.md)
- [Agentcadia](https://agentcadia.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Upload reports include metadata writeback status, uploaded files, share-image delivery requirements, and owner-facing message guidance; download reports include placed files, skipped conflicts, payload type, and overwrite status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

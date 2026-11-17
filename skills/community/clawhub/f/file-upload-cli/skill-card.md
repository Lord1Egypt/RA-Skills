## Description:

Upload files to the litterbox.catbox.moe file sharing service and get shareable URLs (72h expiry). Use when the user wants to share a file temporarily or needs a quick file hosting solution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raphacastelloes](https://clawhub.ai/user/raphacastelloes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to upload a specified local file to a temporary public file-hosting service and return a shareable URL. It is suited for short-lived file sharing when the user has confirmed the file is appropriate for public-link access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-specified local files to a public temporary host, and anyone with the resulting URL can access the file.

Mitigation: Use it only for files intended for public-link sharing; avoid private, confidential, regulated, credential-containing, or otherwise sensitive content.

Risk: An agent-accessible command can read and upload a local file path supplied at runtime.

Mitigation: Require explicit confirmation of the exact file path and sharing intent before running the upload command.

Risk: Some artifact documentation mentions 0x0.st even though the code uploads to litterbox.catbox.moe.

Mitigation: Treat litterbox.catbox.moe as the actual upload destination for this release and disclose that destination before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raphacastelloes/skills/file-upload-cli)
- [litterbox.catbox.moe upload service](https://litterbox.catbox.moe)
- [Catbox service status](https://catbox.moe)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a public 72-hour URL for one uploaded file per command; failed uploads require manual retry.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

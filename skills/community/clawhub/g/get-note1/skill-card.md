## Description:

GetNote lets an agent save, retrieve, organize, and semantically search a user's GetNote notes, links, images, and knowledge-base content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deuscx](https://clawhub.ai/user/deuscx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to capture personal notes, save links and images for processing, manage tags and knowledge bases, and retrieve relevant private notes when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, modify, and delete private notes while owner identity checking is optional in shared or group-chat contexts.

Mitigation: Configure GETNOTE_OWNER_ID, use the skill only where requester identity is reliable, and confirm deletes, tag changes, and knowledge-base changes before execution.

Risk: Saved links, uploaded images, OCR text, and note contents are sent to GetNote for processing and storage.

Mitigation: Tell users before sending sensitive content and avoid saving secrets or regulated data unless the user has approved that use.

Risk: Image uploads trust a server-provided destination.

Mitigation: Use the upload destination returned by GetNote only for the intended image workflow and avoid uploading unrelated local files.

## Reference(s):

- [GetNote API details](references/api-details.md)
- [GetNote homepage](https://biji.com)
- [GetNote open platform](https://www.biji.com/openapi)
- [ClawHub skill page](https://clawhub.ai/deuscx/skills/get-note1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GETNOTE_API_KEY and may use GETNOTE_CLIENT_ID and GETNOTE_OWNER_ID for authenticated requests and requester checks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

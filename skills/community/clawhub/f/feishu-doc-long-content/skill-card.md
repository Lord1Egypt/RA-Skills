## Description:

Guides agents to create Feishu Docs by creating an empty document first, then writing content in chunks under 800 bytes to avoid truncation or errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents working with Feishu Docs use this guide to avoid content-size failures when creating or updating long documents. It describes splitting content, writing in smaller chunks, and verifying document contents after each write.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Markdown fallback can leave a persistent copy of document contents.

Mitigation: For sensitive content, split writes into smaller Feishu updates when possible; if a local file is necessary, use a temporary protected location and delete it afterward.

Risk: Long Feishu write payloads can fail, truncate content, or create blank documents.

Mitigation: Create the document first, write content in chunks under 800 bytes, and verify the result with a read after writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/feishu-doc-long-content)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with JSON examples and a troubleshooting table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; recommends small Feishu write payloads and read-after-write verification.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

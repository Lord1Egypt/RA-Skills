## Description:

Ami helps agents manage IMA notes and knowledge bases, including note search, note creation, note updates, knowledge-base browsing, URL import, and file upload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aishaoqing](https://clawhub.ai/user/aishaoqing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent work with IMA personal notes and knowledge bases through credentialed IMA OpenAPI calls. It is useful for searching private knowledge, creating or appending notes, importing URLs, and uploading supported files after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private notes, knowledge-base content, file uploads, and credentials.

Mitigation: Review before installing, use a secure credential store or tightly permissioned files, and confirm each note write, URL import, or file upload before execution.

Risk: Untrusted or internal URLs could be imported into IMA or used as upload sources.

Mitigation: Validate URLs, avoid untrusted or internal targets, and require explicit upload consent before importing external content.

Risk: Existing notes can be modified by append operations, and incorrectly encoded text can corrupt note content.

Mitigation: Confirm the target note before appending and perform UTF-8 validation before note write operations.

## Reference(s):

- [IMA Home](https://ima.qq.com)
- [IMA Agent Interface](https://ima.qq.com/agent-interface)
- [Knowledge Base API Reference](artifact/knowledge-base/references/api.md)
- [Notes API Reference](artifact/notes/references/api.md)
- [Tencent COS Signature Documentation](https://cloud.tencent.com/document/product/436/7778)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provisioned IMA OpenAPI Client ID and API Key; file upload workflows may send selected private content to IMA and Tencent COS.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

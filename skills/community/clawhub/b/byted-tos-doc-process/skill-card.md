## Description:

Generates pre-signed URLs for Bytedance TOS `doc-preview` processing to preview and convert documents to PDF, images (PNG/JPG), or HTML, and to export page ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate TOS document-preview URLs, convert stored office documents to PDF, image, or HTML previews, read page-count metadata, and batch export page ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary signed preview URLs and decoded HTML preview tokens can grant document access if shared or logged.

Mitigation: Use short-lived, least-privilege TOS credentials and avoid pasting signed URLs or tokens into chats, tickets, logs, or CI output.

Risk: The direct URL mode can fetch an arbitrary URL supplied to the script.

Mitigation: Use `--direct-url` only with trusted TOS preview URLs and restrict outbound network access where possible.

Risk: The `tos` dependency is not pinned in the artifact requirements.

Mitigation: Pin `tos` to a reviewed version before installing in shared, production, or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-tos-doc-process)
- [README.md](artifact/README.md)
- [REFERENCE.md](artifact/REFERENCE.md)
- [WORKFLOWS.md](artifact/WORKFLOWS.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python examples, shell commands, generated URLs, and local output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce signed preview URLs, decoded HTML preview URLs, converted PDF/image files, page-count text, or batch-export JSON depending on the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manages files in a Cargo workspace by uploading and organizing documents, building searchable libraries, and storing files at paths with shareable links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload, organize, search, and store workspace files, then retrieve or share them by path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment example could replace existing agent settings without adequate review.

Mitigation: Preserve current settings, inspect the proposed changes, and explicitly authorize deployment.

Risk: Uploads may send documents to OpenAI and commit copies to the context repository.

Mitigation: When those copies are unwanted, use a new private path with indexing and context mirroring disabled.

Risk: Anyone holding a signed or public sharing link can access its file.

Mitigation: Create or share links only when requested, and do not use them for files containing record-level personal data.

Risk: The installation guidance uses the latest CLI package, and external CLI code is outside this inspection.

Mitigation: Pin a reviewed CLI version.

## Reference(s):

- [File and library examples](references/examples/files.md)
- [Files as storage: paths and links](references/objects.md)
- [Content response shapes](references/response-shapes.md)
- [Content troubleshooting](references/troubleshooting.md)
- [Cargo skills project homepage (listed in skill metadata)](https://github.com/getcargohq/cargo-skills)
- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/cargo-content)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell command examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover CLI, HTTP, worker, workflow node, and agent usage.]

## Skill Version(s):

1.3.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

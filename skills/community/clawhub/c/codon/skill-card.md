## Description:

Organize agent memory as a navigable filesystem where each memory receives a numbered address, with zero dependencies and human-readable markdown storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldub](https://clawhub.ai/user/pauldub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Codon to initialize and maintain a local markdown memory system with stable numbered locations for people, projects, resources, and work notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable markdown memory files under MEMORY may contain private notes or client information.

Mitigation: Install only in protected workspaces, review MEMORY contents, consider adding MEMORY to .gitignore for private notes, and avoid storing secrets or sensitive client data.

Risk: Initialization writes local directories and index files into the workspace.

Mitigation: Run initialization only in workspaces where Codon's memory taxonomy is desired and review the generated files before committing them.

## Reference(s):

- [Codon homepage](https://github.com/pauldub/codon)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and local markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local MEMORY directories and index files; no network access, API keys, databases, or embeddings are required.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

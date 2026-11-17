## Description:

Use the Archiver library for streaming archive packaging in Node.js. Supports creating ZIP/TAR archives, appending content from streams, strings, buffers, file paths, directories, and glob patterns, as well as registering custom formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create ZIP and TAR archives in Node.js, including streaming HTTP responses, in-memory archives, directory packaging, glob-based file selection, and custom archive formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad directory packaging can unintentionally include private files such as .git, .env, credentials, node_modules, or generated build output.

Mitigation: Specify exact source and output paths, prefer glob allowlists or explicit ignore patterns, and review archive contents before sharing.

Risk: Using archive.directory() for bulk packaging does not provide ignore or filter patterns.

Mitigation: Use archive.glob() with ignore patterns or a reviewed file list when exclusions are required.

## Reference(s):

- [Archiver API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/archiver)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance on path selection, glob filtering, archive options, and error handling.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

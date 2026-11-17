## Description:

Use when the user wants to convert local PDF, DOCX, or PPTX files into Markdown with the packaged doc2md CLI, especially for batch conversion, recursive folder processing, or Windows and Linux command-line usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yance-dev](https://clawhub.ai/user/yance-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run a command-line workflow for converting PDF, DOCX, and PPTX files into Markdown through the doc2md platform API, including batch and recursive folder conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs document conversion traffic and bearer-token authentication toward a plaintext HTTP endpoint.

Mitigation: Use only a trusted HTTPS doc2md endpoint and verify the service's retention and privacy posture before sending sensitive documents.

Risk: The artifact claims packaged Windows and Linux CLI binaries, but the server security summary reports that those binaries are not present.

Mitigation: Verify the missing CLI binaries or source before running installation or conversion commands.

Risk: Bearer tokens may be exposed if stored in plaintext configuration.

Mitigation: Prefer environment variables or a secure secret store over plaintext config files for authentication secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yance-dev/skills/doc2mdyc)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described CLI writes one output subdirectory per input document, prints progress and status to stdout, and exits non-zero if any conversion fails.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

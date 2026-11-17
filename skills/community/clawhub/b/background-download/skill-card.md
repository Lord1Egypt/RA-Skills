## Description:

Asynchronous background download with retry, status tracking via Ontology, notifications to original channel. Supports resume on broken connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansponddg](https://clawhub.ai/user/hansponddg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to start, monitor, and maintain background file downloads with retries, resume support, ontology-backed status, and notifications to the originating channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation can run attacker-controlled shell commands.

Mitigation: Use only in a tightly controlled environment with trusted inputs, and replace shell=True command construction with argument lists before broader use.

Risk: Downloads can be written to arbitrary local paths.

Mitigation: Restrict downloads to approved HTTPS URLs and a dedicated download directory with path validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hansponddg/skills/background-download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets, plus JSON task and status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates DownloadTask records and may emit completion or failure notifications to the original channel.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

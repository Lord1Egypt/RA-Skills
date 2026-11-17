## Description:

Packages workspace files into ZIP archives, writes a companion description, and notifies the Manager service for user delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to package generated workspace deliverables and make them available to the user with a short human-readable description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can package and deliver workspace files without a direct user request.

Mitigation: Require explicit confirmation of the exact source path and description before running the delivery script.

Risk: Path boundary weaknesses could send more workspace content than intended.

Mitigation: Fix the workspace boundary check and review resolved paths before delivery.

Risk: Predictable temporary response-file handling could affect notification behavior.

Mitigation: Use a unique temporary response file and clean it up after each Manager notification attempt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whyhit2005/skills/file-sender)

## Skill Output:

**Output Type(s):** [files, text, shell commands]

**Output Format:** [ZIP archive, plain-text description file, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, zip, and Manager-provided OpenClaw environment variables; generated ZIP files are capped at 500MB and retained in .file-outbox.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

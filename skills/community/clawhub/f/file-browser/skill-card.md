## Description:

Read-only file browsing and text-file reading in the OpenClaw workspace, with relative-path-only access intended for listing directories and reading files up to 10k characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nagilem](https://clawhub.ai/user/nagilem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect an OpenClaw workspace by listing directories and reading bounded text file contents without write, delete, or arbitrary execution operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a containment flaw that can expose files outside the intended workspace through symlinks.

Mitigation: Review before installing, avoid browsing untrusted workspace symlinks, and require canonical path containment checks before trusting the skill as workspace-only.

Risk: The security guidance notes that JSON output is not produced with a real encoder.

Mitigation: Treat script output as untrusted until JSON encoding is hardened and downstream agents parse errors defensively.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nagilem/skills/file-browser)
- [Publisher Profile](https://clawhub.ai/user/nagilem)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown responses based on JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directory listings and file reads are returned by helper scripts as JSON; file content is limited to 10k characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

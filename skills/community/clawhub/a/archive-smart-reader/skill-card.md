## Description:

Archive Smart Reader helps an agent list, preview, search, and extract files from common archive formats including zip, tar, gz, tgz, bz2, xz, 7z, and rar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to inspect archive contents, preview text files, find matching entries, or extract selected files without first unpacking the whole archive manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the skill can extract archive contents, install dependencies, discover helper executables, and persist usage memory.

Mitigation: Review before installing, run only in a trusted or disposable workspace, and approve archive extraction destinations and dependency changes explicitly.

Risk: RAR preview and extraction depend on an external unrar or 7-Zip helper executable.

Mitigation: Use RAR handling only when the helper executable path is explicitly trusted, or restrict use to archive listing.

Risk: Persistent learning records usage patterns under the user's home directory.

Mitigation: Disable or clear the learning file when usage history should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/archive-smart-reader)
- [ClawHub publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and file summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce archive listings, previews capped to manageable text snippets, extraction paths, and operational guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

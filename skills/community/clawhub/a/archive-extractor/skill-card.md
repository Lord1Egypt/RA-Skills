## Description:

Recursively extracts archive files from a file or directory, supporting zip, tar variants, rar, 7z, and single-file compressed formats on Python 3.8+ across Windows, Linux, and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiliangzhao20241028](https://clawhub.ai/user/qiliangzhao20241028)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to unpack individual archives, bulk archive directories, nested archives, and common compressed file formats while keeping repeated extraction runs idempotent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extractor can automatically install unpinned Python packages for rar and 7z support.

Mitigation: Preinstall reviewed dependencies in an isolated environment and avoid automatic package installation in sensitive environments.

Risk: Archive extraction can expose unsafe archive contents or path behaviors.

Mitigation: Use the skill only on trusted archives, extract in a sandbox or dedicated destination directory, and inspect outputs before further use.

Risk: The force option can delete an existing extraction output directory before re-extracting.

Mitigation: Avoid using --force near valuable folders and do not run the extractor with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiliangzhao20241028/skills/archive-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct execution of a local Python extraction script that writes extracted files and log output.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

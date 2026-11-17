## Description:

Scan your machine for large directories, duplicate files, and stale resume files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malavyaraval](https://clawhub.ai/user/malavyaraval)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan a local filesystem for large directories, duplicate files, and stale resume-related files, then generate a local cleanup report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan target is hard-coded to /mnt/c/Users/malav and may collect file paths, duplicate metadata, and resume-related file names from an unintended local account.

Mitigation: Use only when /mnt/c/Users/malav is the intended scan scope; prefer a version that asks for and confirms the scan directory before each run.

Risk: Generated reports and duplicate-scan output persist local file metadata in ~/reports and /tmp/duplicates.txt.

Mitigation: Keep generated outputs private, review them before sharing, and delete reports or temporary files when they are no longer needed.

## Reference(s):

- [Cleanup Reporter ClawHub Page](https://clawhub.ai/malavyaraval/skills/cleanup-reporter)
- [Declared Homepage](https://github.com/MalavyaRaval/cleanup-reporter)

## Skill Output:

**Output Type(s):** [markdown, shell commands, text]

**Output Format:** [Markdown report file with shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated cleanup report under ~/reports and duplicate-scan output under /tmp/duplicates.txt.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

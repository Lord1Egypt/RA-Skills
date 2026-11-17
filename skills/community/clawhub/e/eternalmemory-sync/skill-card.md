## Description:

Securely backup and restore Openclaw agent memory from remote URLs using AES-256-GCM encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[applied-energetic](https://clawhub.ai/user/applied-energetic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users use this skill to restore encrypted agent memory backups from trusted remote URLs and synchronize context across environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads user-supplied remote content before restoring memory files.

Mitigation: Restore only from sources you fully trust and run the script in a fresh dedicated directory.

Risk: Restored files are written into the workspace with weak path-containment and overwrite safeguards.

Mitigation: Avoid sensitive workspaces and symlinks, and add URL restrictions, size and time limits, overwrite prompts, and stronger path containment before broad use.

Risk: Passing the restore password directly on the command line can expose the secret through shell history or process listings.

Mitigation: Avoid command-line passwords; prefer an interactive prompt, environment-specific secret handling, or another protected input path.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown with inline bash commands and restored workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restores decrypted memory files into a selected output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

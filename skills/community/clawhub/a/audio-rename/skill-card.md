## Description:

Rename audio files with Chinese/special characters to simple English names for mlx-stt compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audio-processing users use this skill to rename local audio files with Chinese or special-character filenames into simple ASCII-style names before passing them to tools such as mlx-stt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode can rename multiple local audio files in the selected directory.

Mitigation: Confirm the target directory before running batch mode and keep backups or versioned copies for important files.

Risk: Custom output names containing path separators or parent-directory segments could place renamed files somewhere unexpected.

Mitigation: Use simple basename-only custom names and avoid slashes, backslashes, or '..' in the requested name.

Risk: The generic trigger phrase "fix filename" may invoke the skill for files outside the intended audio-renaming workflow.

Mitigation: Prefer audio-specific prompts such as "rename audio" when asking an agent to use this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The suggested commands operate on local files and may rename one file or a batch of audio files when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

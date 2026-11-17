## Description:

Downloads Douyin videos, transcribes them with faster-whisper, and saves transcript notes to an Obsidian knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn a Douyin video URL into local transcript files and an Obsidian note with metadata and an AI-generated summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags unsafe code templating.

Mitigation: Review generated commands before execution and pass video metadata through JSON or command arguments instead of interpolating it into Python code.

Risk: The release security summary flags silent writes to an Obsidian vault.

Mitigation: Confirm the destination vault and note path before writing, and avoid overwriting existing notes.

Risk: The release security guidance limits use to trusted videos and metadata.

Mitigation: Run the workflow only for Douyin URLs and metadata sources the user trusts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/douyin-video-to-txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python code blocks; produced artifacts include transcript text files and an Obsidian Markdown note.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local temporary media and transcript files, then writes a note under the configured Obsidian vault path.]

## Skill Version(s):

2.0.3 (source: server release metadata; artifact frontmatter says 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Track, analyze, and manage music and audio files from the command line. Use when organizing playlists, converting formats, or analyzing metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users can use Beat to log music and audio-related workflow activity, inspect recent activity, search entries, and export local records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as a music and audio management tool, but security evidence says the bundled script is mostly a generic local activity logger with no real audio processing.

Mitigation: Treat Beat as a local text logging utility, verify expected behavior before relying on it for audio workflows, and do not assume it converts or analyzes media content.

Risk: Commands can record user-provided text and export local records under ~/.local/share/beat/.

Mitigation: Avoid entering secrets, tokens, private paths, or sensitive playlist and media details, and remove ~/.local/share/beat/ after testing if the records are not needed.

## Reference(s):

- [Beat Skill Page](https://clawhub.ai/bytesagain3/skills/beat)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local activity logs and export files under ~/.local/share/beat/.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

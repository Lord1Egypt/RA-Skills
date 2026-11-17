## Description:

Generate narrative chronicles of developer work from git history, session transcripts, and memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sssamuelll](https://clawhub.ai/user/sssamuelll)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn local git history, memory notes, and session metadata into daily chronicles, weekly recaps, standup notes, or portfolio narratives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pull private developer history, memory notes, and session metadata into agent context.

Mitigation: Review config.json before use, restrict projectDirs, memoryDir, and sessionsDir to intended locations, and avoid auto-detected memory or session sources unless they are explicitly needed.

Risk: The security scan reports unsafe configurable path handling in the bundled gather.sh script.

Mitigation: Review and fix scripts/gather.sh before use in shared or untrusted environments, and run it only with reviewed paths in a trusted workspace.

## Reference(s):

- [Voice Profile Template](artifact/references/voice-profile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown narrative prose with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce daily, weekly, standup, or portfolio narrative formats from gathered local development history.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

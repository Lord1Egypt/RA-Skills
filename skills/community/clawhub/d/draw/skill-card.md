## Description:

Draw records design notes such as palettes, swatches, gradients, contrast checks, and exports local logs, despite being advertised as SVG diagram generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and front-end developers can use this skill as a command-line design journal for palettes, swatches, gradients, contrast notes, and exports. Review before installation because server security evidence says it does not clearly match its advertised SVG drawing purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is flagged suspicious because it does not clearly match its advertised SVG drawing purpose.

Mitigation: Review the artifact before installing and do not rely on it as an SVG diagram generator unless the behavior is manually verified.

Risk: User-provided design text is persisted locally under ~/.local/share/draw without a documented purge or retention control.

Mitigation: Do not enter secrets, proprietary prompts, or sensitive project details; manually inspect and delete local stored data when needed.

## Reference(s):

- [Draw skill page](https://clawhub.ai/bytesagain3/skills/draw)
- [bytesagain3 publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled command writes plain-text logs and JSON, CSV, or text exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries under ~/.local/share/draw when executed; no API keys or external dependencies are documented.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

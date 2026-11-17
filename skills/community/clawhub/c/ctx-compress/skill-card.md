## Description:

Intelligently compress context - conversations, code, logs. Preserve key information while reducing token usage. Auto-detects content type and applies optimal compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity agents use this skill to compress conversations, code, logs, and text into compact summaries that preserve decisions, issues, key code, and statistics for context-window management and cross-session handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed summaries are lossy and may omit details needed for later reasoning or replacement of original context.

Mitigation: Review compressed text before using it to replace original conversation history or source material.

Risk: Input files may contain secrets, sensitive logs, URLs, paths, or snippets that can appear in terminal output.

Mitigation: Run the skill only on files intentionally selected for compression or analysis, and avoid highly sensitive inputs unless that output exposure is acceptable.

Risk: Code compression can remove comments or docstrings that carry important operational or safety context.

Mitigation: Use light mode for code when comments may be significant, and inspect the compressed result before relying on it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown sections, and JSON for structured extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports light, medium, and aggressive compression levels; reads user-selected files, inline text, or stdin.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

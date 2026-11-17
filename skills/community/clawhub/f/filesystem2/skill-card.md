## Description:

Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq258067284](https://clawhub.ai/user/qq258067284)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to list, search, copy, visualize, and analyze local filesystem content with filtering and safety-oriented options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad local filesystem listing, searching, analysis, and copying.

Mitigation: Use dry-run for batch copy operations, verify source and destination paths, and avoid overwrite operations unless replacement is intended.

Risk: The package snapshot did not include the executable implementation, so claimed safeguards could not be independently verified from code.

Mitigation: Review the installed executable and run it in a constrained workspace before granting access to sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq258067284/skills/filesystem2)
- [Node.js runtime](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filesystem listings, search results, directory trees, copy-operation previews, and analysis summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

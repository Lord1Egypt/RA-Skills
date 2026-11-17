## Description:

Use this skill when the user wants to record, view, update, complete, cancel, or review a personal bucket list / wish list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanguangzhe-collab](https://clawhub.ai/user/yanguangzhe-collab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to maintain a local personal bucket list: adding wishes, viewing pending, completed, and cancelled items, marking outcomes, reviewing achievements, and using a localhost GUI over the same JSON data file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports an import-related script injection risk in the browser GUI.

Mitigation: Import bucket-list JSON only from trusted sources, and review imported entries before continued use.

Risk: The authoritative security summary reports under-disclosed local persistence of personal fields and a browser file handle.

Mitigation: Avoid entering sensitive birth-year or life-progress values on shared browsers, and unlink the retained file handle when it is no longer needed.

Risk: The authoritative security guidance notes that the GUI can retain life-progress values locally across sessions.

Mitigation: Clear the browser's local site data after use on shared or temporary machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yanguangzhe-collab/skills/bucket-list)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-backed local records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates a local bucket-list JSON file; the GUI can export and import JSON.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

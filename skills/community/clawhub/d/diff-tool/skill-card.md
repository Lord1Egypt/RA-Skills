## Description: <br>
Compares two text strings or files and highlights added, removed, and changed lines for code review, document comparison, and version comparison workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and reviewers use this skill to compare text snippets or files, inspect highlighted line-level differences, and optionally receive concise or JSON-formatted diff output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic requests containing "diff" may route to this skill even when the user intended a broader comparison task. <br>
Mitigation: Use the skill for explicit text or file comparison requests, and confirm any file reads before comparing local paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/diff-tool) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text, ANSI-colored terminal output, or JSON diff summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports standard, simple, and JSON formats; can ignore whitespace and show added or removed line counts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

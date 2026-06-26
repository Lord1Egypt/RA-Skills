## Description: <br>
Compare two files and display their differences in a human-readable markdown format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super9du](https://clawhub.ai/user/super9du) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare two local files and turn unified diff output into a concise Markdown summary of additions, deletions, and modifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-specified local files, so sensitive file contents may be exposed in the conversation or generated Markdown. <br>
Mitigation: Use explicit file paths only for files that are appropriate to inspect and share in the agent session. <br>
Risk: Generated Markdown can contain untrusted text from compared files or filenames. <br>
Mitigation: Review generated Markdown before reusing or publishing it, especially when inputs come from external sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/super9du/file-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with diff-style code blocks and file path headings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-specified local file paths and preserves additions, deletions, modifications, and context lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

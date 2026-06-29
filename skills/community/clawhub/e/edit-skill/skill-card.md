## Description: <br>
Edit Skill helps agents review and tighten existing skill files while preserving behavior, trigger intent, safety boundaries, and host-compatible frontmatter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review or edit existing agent skills, remove duplicated or vague instructions, and preserve safety boundaries and host-specific frontmatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Edits to skill instructions can change safety behavior, tool permissions, routing, or installation metadata. <br>
Mitigation: Use review-only mode for security-sensitive skills and inspect diffs carefully before relying on edited skill files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review notes, patch summaries, file edits, and validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply edits in repository files when the user asks for an edit-in-repo workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
